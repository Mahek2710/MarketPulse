SELECT
    DATE_TRUNC('day', il.run_at)                     AS day,
    src.name                                          AS source,
    SUM(il.articles_fetched)                         AS total_fetched,
    SUM(il.articles_inserted)                        AS total_inserted,
    SUM(il.articles_skipped)                         AS total_skipped,
    SUM(il.articles_failed)                          AS total_failed,
    SUM(il.errors)                                   AS total_errors,
    ROUND(
        100.0 * SUM(il.articles_inserted)
        / NULLIF(SUM(il.articles_fetched), 0), 2
    )                                                AS insert_rate_pct,
    ROUND(AVG(il.duration_seconds)::numeric, 2)      AS avg_run_seconds
FROM ingestion_logs il
JOIN sources src ON il.source_id = src.id
WHERE il.run_at >= NOW() - INTERVAL '7 days'
GROUP BY DATE_TRUNC('day', il.run_at), src.name
ORDER BY day DESC, source;