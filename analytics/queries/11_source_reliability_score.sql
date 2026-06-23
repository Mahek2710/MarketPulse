SELECT
    src.name                                         AS source,
    SUM(il.articles_fetched)                         AS total_fetched,
    SUM(il.articles_inserted)                        AS total_inserted,
    SUM(il.articles_failed)                          AS total_failed,
    SUM(il.errors)                                   AS total_errors,
    ROUND(
        100.0 * SUM(il.articles_inserted)
        / NULLIF(SUM(il.articles_fetched), 0), 2
    )                                                AS success_rate_pct,
    ROUND(AVG(il.duration_seconds)::numeric, 2)      AS avg_duration_seconds
FROM ingestion_logs il
JOIN sources src ON il.source_id = src.id
GROUP BY src.name
ORDER BY success_rate_pct DESC;