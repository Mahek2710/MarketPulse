SELECT
    c.name                                           AS company,
    c.sector,
    COUNT(DISTINCT a.id)                             AS total_mentions,
    ROUND(AVG(s.score)::numeric, 4)                  AS avg_sentiment,
    SUM(CASE WHEN s.label = 'positive' THEN 1 ELSE 0 END) AS positive,
    SUM(CASE WHEN s.label = 'negative' THEN 1 ELSE 0 END) AS negative
FROM article_companies ac
JOIN companies c          ON ac.company_id = c.id
JOIN articles a           ON ac.article_id = a.id
JOIN sentiment_scores s   ON a.id = s.article_id
WHERE a.published_at >= NOW() - INTERVAL '7 days'
GROUP BY c.name, c.sector
ORDER BY total_mentions DESC
LIMIT 15;