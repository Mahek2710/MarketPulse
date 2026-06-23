SELECT
    c.name                                           AS company,
    c.sector,
    COUNT(*)                                         AS article_count,
    ROUND(AVG(s.score)::numeric, 4)                  AS avg_sentiment,
    ROUND(STDDEV(s.score)::numeric, 4)               AS sentiment_volatility,
    ROUND(MIN(s.score)::numeric, 4)                  AS worst_score,
    ROUND(MAX(s.score)::numeric, 4)                  AS best_score
FROM sentiment_scores s
JOIN article_companies ac ON s.article_id = ac.article_id
JOIN companies c          ON ac.company_id = c.id
JOIN articles a           ON s.article_id = a.id
WHERE a.published_at >= NOW() - INTERVAL '30 days'
GROUP BY c.name, c.sector
HAVING COUNT(*) >= 3
ORDER BY sentiment_volatility DESC NULLS LAST;