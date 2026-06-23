import json
from storage.db import get_cursor
from storage.models import Article, SentimentScore


def get_or_create_source(name: str) -> int:
    with get_cursor() as cur:
        cur.execute('SELECT id FROM sources WHERE name = %s', (name,))
        row = cur.fetchone()
        if row:
            return row[0]
        cur.execute(
            'INSERT INTO sources (name, feed_url) VALUES (%s, %s) RETURNING id',
            (name, '')
        )
        return cur.fetchone()[0]


def insert_article(article: Article, source_id: int) -> int:
    """Returns article_id on success, None if duplicate."""
    try:
        with get_cursor() as cur:
            cur.execute('''
                INSERT INTO articles
                    (headline, summary, url, url_hash, source_id, published_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (
                article.headline,
                article.summary,
                article.url,
                article.url_hash,
                source_id,
                article.published_at
            ))
            return cur.fetchone()[0]
    except Exception as e:
        if 'unique' in str(e).lower():
            return None
        raise


def insert_sentiment(score: SentimentScore):
    with get_cursor() as cur:
        cur.execute('''
            INSERT INTO sentiment_scores
                (article_id, score, magnitude, label, model_used)
            VALUES (%s, %s, %s, %s, %s)
        ''', (
            score.article_id,
            score.score,
            score.magnitude,
            score.label,
            score.model_used
        ))


def insert_article_company(article_id: int, company_id: int):
    with get_cursor() as cur:
        cur.execute('''
            INSERT INTO article_companies (article_id, company_id)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        ''', (article_id, company_id))


def get_or_create_company(name: str, ticker: str, sector: str) -> int:
    with get_cursor() as cur:
        cur.execute('SELECT id FROM companies WHERE name = %s', (name,))
        row = cur.fetchone()
        if row:
            return row[0]
        cur.execute('''
            INSERT INTO companies (name, ticker, sector)
            VALUES (%s, %s, %s)
            RETURNING id
        ''', (name, ticker, sector))
        return cur.fetchone()[0]


def insert_failed(raw_data: dict, reason: str, source_id: int):
    with get_cursor() as cur:
        cur.execute('''
            INSERT INTO failed_ingestion (raw_data, failure_reason, source_id)
            VALUES (%s, %s, %s)
        ''', (json.dumps(raw_data, default=str), reason, source_id))


def log_run(log_data: dict):
    with get_cursor() as cur:
        cur.execute('''
            INSERT INTO ingestion_logs
                (source_id, articles_fetched, articles_inserted,
                 articles_skipped, articles_failed, errors,
                 duration_seconds, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            log_data['source_id'],
            log_data['fetched'],
            log_data['inserted'],
            log_data['skipped'],
            log_data['failed'],
            log_data['errors'],
            log_data['duration'],
            log_data['status']
        ))


def fetch_company_summary(company: str, days: int) -> list:
    with get_cursor() as cur:
        cur.execute('''
            SELECT
                a.headline,
                s.score,
                s.label,
                a.published_at::date,
                src.name
            FROM articles a
            JOIN sentiment_scores s   ON a.id = s.article_id
            JOIN article_companies ac ON a.id = ac.article_id
            JOIN companies c          ON ac.company_id = c.id
            JOIN sources src          ON a.source_id = src.id
            WHERE c.name ILIKE %s
            AND a.published_at >= NOW() - (%s || ' days')::INTERVAL
            ORDER BY a.published_at DESC
        ''', (f'%{company}%', str(days)))
        return cur.fetchall()


def fetch_sector_summary(sector: str, days: int) -> list:
    with get_cursor() as cur:
        cur.execute('''
            SELECT
                c.name,
                ROUND(AVG(s.score)::numeric, 4),
                COUNT(DISTINCT a.id),
                s.label
            FROM articles a
            JOIN sentiment_scores s   ON a.id = s.article_id
            JOIN article_companies ac ON a.id = ac.article_id
            JOIN companies c          ON ac.company_id = c.id
            WHERE c.sector ILIKE %s
            AND a.published_at >= NOW() - (%s || ' days')::INTERVAL
            GROUP BY c.name, s.label
            ORDER BY c.name
        ''', (f'%{sector}%', str(days)))
        return cur.fetchall()


def fetch_anomalies(days: int) -> list:
    with get_cursor() as cur:
        cur.execute('''
            WITH company_stats AS (
                SELECT
                    ac.company_id,
                    AVG(s.score)    AS mean_s,
                    STDDEV(s.score) AS std_s
                FROM sentiment_scores s
                JOIN article_companies ac ON s.article_id = ac.article_id
                GROUP BY ac.company_id
                HAVING COUNT(*) >= 10
            )
            SELECT
                c.name,
                LEFT(a.headline, 80),
                a.published_at::date,
                s.score,
                ROUND(((s.score - cs.mean_s) / NULLIF(cs.std_s, 0))::numeric, 2)
            FROM sentiment_scores s
            JOIN article_companies ac ON s.article_id = ac.article_id
            JOIN companies c          ON ac.company_id = c.id
            JOIN company_stats cs     ON ac.company_id = cs.company_id
            JOIN articles a           ON s.article_id = a.id
            WHERE ((s.score - cs.mean_s) / NULLIF(cs.std_s, 0)) < -2
            AND a.published_at >= NOW() - (%s || ' days')::INTERVAL
            ORDER BY 5 ASC
        ''', (str(days),))
        return cur.fetchall()


def fetch_pipeline_health(days: int) -> list:
    with get_cursor() as cur:
        cur.execute('''
            SELECT
                DATE_TRUNC('day', run_at)::date,
                src.name,
                SUM(articles_fetched),
                SUM(articles_inserted),
                SUM(articles_failed),
                ROUND(
                    100.0 * SUM(articles_inserted)
                    / NULLIF(SUM(articles_fetched), 0), 1
                )
            FROM ingestion_logs il
            JOIN sources src ON il.source_id = src.id
            WHERE run_at >= NOW() - (%s || ' days')::INTERVAL
            GROUP BY 1, 2
            ORDER BY 1 DESC
        ''', (str(days),))
        return cur.fetchall()