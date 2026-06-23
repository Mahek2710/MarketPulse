WITH weekly_coverage AS (
    SELECT
        c.id                                          AS company_id,
        c.name                                        AS company,
        DATE_TRUNC('week', a.published_at)            AS week,
        COUNT(DISTINCT a.id)                          AS article_count
    FROM articles a
    JOIN article_companies ac ON a.id = ac.article_id
    JOIN companies c          ON ac.company_id = c.id
    WHERE a.published_at >= NOW() - INTERVAL '60 days'
    GROUP BY c.id, c.name, DATE_TRUNC('week', a.published_at)
)
SELECT
    company,
    week,
    article_count,
    LAG(article_count) OVER (
        PARTITION BY company_id ORDER BY week
    )                                                 AS prev_week_count,
    article_count - LAG(article_count) OVER (
        PARTITION BY company_id ORDER BY week
    )                                                 AS coverage_change
FROM weekly_coverage
ORDER BY coverage_change ASC NULLS LAST;