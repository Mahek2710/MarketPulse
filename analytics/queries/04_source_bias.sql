SELECT
    src.name                                         AS source,
    ROUND(AVG(s.score)::numeric, 4)                  AS avg_sentiment,
    COUNT(*)                                         AS total_articles,
    SUM(CASE WHEN s.label = 'positive' THEN 1 ELSE 0 END) AS positive_count,
    SUM(CASE WHEN s.label = 'negative' THEN 1 ELSE 0 END) AS negative_count,
    SUM(CASE WHEN s.label = 'neutral'  THEN 1 ELSE 0 END) AS neutral_count,
    RANK() OVER (ORDER BY AVG(s.score) ASC)          AS negativity_rank
FROM sentiment_scores s
JOIN articles a  ON s.article_id = a.id
JOIN sources src ON a.source_id = src.id
WHERE a.published_at >= NOW() - INTERVAL '30 days'
GROUP BY src.name
ORDER BY avg_sentiment ASC;