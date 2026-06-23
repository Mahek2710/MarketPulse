SELECT
    c.sector,
    DATE_TRUNC('week', a.published_at)               AS week,
    ROUND(AVG(s.score)::numeric, 4)                  AS avg_sentiment,
    COUNT(DISTINCT a.id)                             AS article_count,
    COUNT(DISTINCT c.id)                             AS companies_covered,
    SUM(CASE WHEN s.label = 'negative' THEN 1 ELSE 0 END) AS negative_articles,
    ROUND((
        100.0 * SUM(CASE WHEN s.label = 'negative' THEN 1 ELSE 0 END)
        / COUNT(*)
    )::numeric, 2)                                   AS negative_pct
FROM sentiment_scores s
JOIN article_companies ac ON s.article_id = ac.article_id
JOIN companies c          ON ac.company_id = c.id
JOIN articles a           ON s.article_id = a.id
WHERE a.published_at >= NOW() - INTERVAL '90 days'
GROUP BY c.sector, DATE_TRUNC('week', a.published_at)
ORDER BY week DESC, avg_sentiment ASC;