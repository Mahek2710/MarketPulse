import time
import logging
from config.feeds import FEEDS
from ingestion.feed_fetcher import fetch_feed
from processing.validator import ArticleValidator
from processing.ner_extractor import extract_companies
from processing.sector_classifier import classify_companies
from processing.sentiment_analyzer import score_article
from storage import repository as repo
from storage.models import Article, SentimentScore

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)
validator = ArticleValidator()


def run_full_pipeline():
    logger.info('=== MarketPulse Pipeline Starting ===')
    for feed_config in FEEDS:
        if not feed_config.get('is_active', True):
            logger.info(f'Skipping inactive feed: {feed_config["name"]}')
            continue
        _run_one_feed(feed_config)
    logger.info('=== Pipeline Complete ===')


def _run_one_feed(feed_config: dict):
    start = time.time()
    counters = {
        'fetched': 0,
        'inserted': 0,
        'skipped': 0,
        'failed': 0,
        'errors': 0
    }

    source_id = repo.get_or_create_source(feed_config['name'])
    raw_articles = fetch_feed(feed_config)
    counters['fetched'] = len(raw_articles)

    for raw in raw_articles:
        try:
            # Step 1 — Validate
            errors = validator.validate(raw)
            if errors:
                repo.insert_failed(raw, ' | '.join(errors), source_id)
                counters['failed'] += 1
                continue

            # Step 2 — Insert article (dedup via url_hash)
            article = Article(
                headline=raw['headline'],
                summary=raw.get('summary', ''),
                url=raw['url'],
                url_hash=raw['url_hash'],
                published_at=raw['published_at'],
                source_name=feed_config['name'],
            )
            article_id = repo.insert_article(article, source_id)

            if article_id is None:
                counters['skipped'] += 1
                continue

            # Step 3 — NER + sector classification
            ner_entities = extract_companies(
                raw['headline'],
                raw.get('summary', '')
            )
            classified = classify_companies(ner_entities)
            for company_name, ticker, sector in classified:
                cid = repo.get_or_create_company(company_name, ticker, sector)
                repo.insert_article_company(article_id, cid)

            # Step 4 — Sentiment
            sent = score_article(raw['headline'], raw.get('summary', ''))
            score_obj = SentimentScore(article_id=article_id, **sent)
            repo.insert_sentiment(score_obj)

            counters['inserted'] += 1

        except Exception as e:
            logger.exception(
                f'Error processing: {raw.get("headline", "?")[:60]}'
            )
            counters['errors'] += 1

    duration = round(time.time() - start, 2)

    if counters['errors'] > 5:
        status = 'failed'
    elif counters['errors'] > 0:
        status = 'partial'
    else:
        status = 'success'

    repo.log_run({
        **counters,
        'source_id': source_id,
        'duration': duration,
        'status': status
    })

    logger.info(
        f'{feed_config["name"]} done — '
        f'fetched={counters["fetched"]} '
        f'inserted={counters["inserted"]} '
        f'skipped={counters["skipped"]} '
        f'failed={counters["failed"]} '
        f'errors={counters["errors"]} '
        f'({duration}s)'
    )


if __name__ == '__main__':
    run_full_pipeline()