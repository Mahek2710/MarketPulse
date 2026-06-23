import feedparser
import hashlib
import logging
from datetime import datetime, timezone
from dateutil import parser as dateparser

logger = logging.getLogger(__name__)


def fetch_feed(feed_config: dict) -> list:
    articles = []
    feed_name = feed_config['name']

    try:
        parsed = feedparser.parse(feed_config['feed_url'])

        if parsed.bozo and parsed.bozo_exception:
            logger.warning(f'{feed_name}: malformed feed — {parsed.bozo_exception}')

        for entry in parsed.entries:
            article = _normalize_entry(entry, feed_name)
            if article:
                articles.append(article)

    except Exception as e:
        logger.error(f'{feed_name}: fetch failed — {e}')

    logger.info(f'{feed_name}: fetched {len(articles)} raw articles')
    return articles


def _normalize_entry(entry, source_name: str) -> dict:
    url = getattr(entry, 'link', None) or getattr(entry, 'id', None)
    if not url:
        return None

    headline = getattr(entry, 'title', '') or ''
    summary = (
        getattr(entry, 'summary', '') or
        getattr(entry, 'description', '') or
        ''
    )

    published_str = (
        getattr(entry, 'published', None) or
        getattr(entry, 'updated', None)
    )
    try:
        published_at = dateparser.parse(published_str).astimezone(timezone.utc)
    except Exception:
        published_at = datetime.now(timezone.utc)

    return {
        'headline': headline.strip(),
        'summary': summary.strip(),
        'url': url.strip(),
        'url_hash': hashlib.md5(url.strip().encode()).hexdigest(),
        'source': source_name,
        'published_at': published_at,
        'scraped_at': datetime.now(timezone.utc),
    }