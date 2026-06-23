SELECT
    src.name                                         AS source,
    MAX(a.published_at)                              AS latest_article,
    NOW() - MAX(a.published_at)                      AS age,
    CASE
        WHEN NOW() - MAX(a.published_at) > INTERVAL '8 hours'
        THEN 'STALE ⚠'
        ELSE 'FRESH ✓'
    END                                              AS freshness_status
FROM articles a
JOIN sources src ON a.source_id = src.id
GROUP BY src.name
ORDER BY latest_article DESC;