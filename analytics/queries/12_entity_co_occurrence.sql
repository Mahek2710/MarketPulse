SELECT
    c1.name                                          AS company_a,
    c2.name                                          AS company_b,
    COUNT(*)                                         AS co_mentions
FROM article_companies ac1
JOIN article_companies ac2 ON ac1.article_id = ac2.article_id
    AND ac1.company_id < ac2.company_id
JOIN companies c1 ON ac1.company_id = c1.id
JOIN companies c2 ON ac2.company_id = c2.id
JOIN articles a   ON ac1.article_id = a.id
WHERE a.published_at >= NOW() - INTERVAL '30 days'
GROUP BY c1.name, c2.name
ORDER BY co_mentions DESC
LIMIT 20;