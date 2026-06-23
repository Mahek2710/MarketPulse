WITH company_stats AS (
    SELECT
        ac.company_id,
        AVG(s.score)    AS mean_sentiment,
        STDDEV(s.score) AS stddev_sentiment
    FROM sentiment_scores s
    JOIN article_companies ac ON s.article_id = ac.article_id
    GROUP BY ac.company_id
    HAVING COUNT(*) >= 5
),
scored AS (
    SELECT
        c.name                                          AS company,
        a.headline,
        a.published_at,
        s.score,
        cs.mean_sentiment,
        ROUND((
            (s.score - cs.mean_sentiment)
            / NULLIF(cs.stddev_sentiment, 0)
        )::numeric, 2)                                  AS z_score
    FROM sentiment_scores s
    JOIN article_companies ac ON s.article_id = ac.article_id
    JOIN companies c          ON ac.company_id = c.id
    JOIN company_stats cs     ON ac.company_id = cs.company_id
    JOIN articles a           ON s.article_id = a.id
)
SELECT * FROM scored
WHERE z_score < -2
ORDER BY z_score ASC;