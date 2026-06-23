SELECT
    CASE
        WHEN EXTRACT(DOW FROM a.published_at) IN (0, 6)
        THEN 'weekend'
        ELSE 'weekday'
    END                                              AS day_type,
    COUNT(*)                                         AS article_count,
    ROUND(AVG(s.score)::numeric, 4)                  AS avg_sentiment,
    ROUND(STDDEV(s.score)::numeric, 4)               AS sentiment_stddev
FROM sentiment_scores s
JOIN articles a ON s.article_id = a.id
WHERE a.published_at >= NOW() - INTERVAL '30 days'
GROUP BY day_type
ORDER BY day_type;