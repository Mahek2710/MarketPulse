SELECT
    failure_reason,
    COUNT(*)                                         AS occurrence_count,
    MAX(attempted_at)                                AS last_seen,
    src.name                                         AS source
FROM failed_ingestion fi
LEFT JOIN sources src ON fi.source_id = src.id
WHERE resolved = FALSE
GROUP BY failure_reason, src.name
ORDER BY occurrence_count DESC;