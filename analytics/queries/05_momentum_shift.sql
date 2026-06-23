WITH weekly AS (
    SELECT
        c.id                                          AS company_id,
        c.name                                        AS company,
        DATE_TRUNC('week', a.published_at)            AS week,
        ROUND(AVG(s.score)::numeric, 4)               AS avg_sentiment
    FROM sentiment_scores s
    JOIN article_companies ac ON s.article_id = ac.article_id
    JOIN companies c          ON ac.company_id = c.id
    JOIN articles a           ON s.article_id = a.id
    GROUP BY c.id, c.name, DATE_TRUNC('week', a.published_at)
)
SELECT
    company,
    week,
    avg_sentiment                                     AS this_week,
    LAG(avg_sentiment) OVER (
        PARTITION BY company_id ORDER BY week
    )                                                 AS last_week,
    ROUND((
        avg_sentiment
        - LAG(avg_sentiment) OVER (PARTITION BY company_id ORDER BY week)
    )::numeric, 4)                                    AS sentiment_delta
FROM weekly
ORDER BY sentiment_delta DESC NULLS LAST;