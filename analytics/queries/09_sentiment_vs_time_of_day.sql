SELECT
    EXTRACT(HOUR FROM a.published_at AT TIME ZONE 'Asia/Kolkata') AS hour_ist,
    COUNT(*)                                         AS article_count,
    ROUND(AVG(s.score)::numeric, 4)                  AS avg_sentiment,
    SUM(CASE WHEN s.label = 'positive' THEN 1 ELSE 0 END) AS positive,
    SUM(CASE WHEN s.label = 'negative' THEN 1 ELSE 0 END) AS negative
FROM sentiment_scores s
JOIN articles a ON s.article_id = a.id
WHERE a.published_at >= NOW() - INTERVAL '30 days'
GROUP BY EXTRACT(HOUR FROM a.published_at AT TIME ZONE 'Asia/Kolkata')
ORDER BY hour_ist;