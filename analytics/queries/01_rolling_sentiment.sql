SELECT
    c.name                                AS company,
    a.published_at::date                  AS date,
    ROUND(AVG(s.score) OVER (
        PARTITION BY c.id
        ORDER BY a.published_at::date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    )::numeric, 4)                        AS rolling_7day_sentiment,
    COUNT(*) OVER (
        PARTITION BY c.id
        ORDER BY a.published_at::date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    )                                     AS article_count_7d,
    s.score                               AS daily_score
FROM sentiment_scores s
JOIN article_companies ac ON s.article_id = ac.article_id
JOIN companies c          ON ac.company_id = c.id
JOIN articles a           ON s.article_id = a.id
WHERE a.published_at >= NOW() - INTERVAL '30 days'
ORDER BY c.name, date;