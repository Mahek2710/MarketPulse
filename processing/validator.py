import re
from datetime import datetime


class ArticleValidator:
    MIN_HEADLINE_LEN = 10
    MAX_HEADLINE_LEN = 500
    MAX_SUMMARY_LEN = 5000
    URL_PATTERN = re.compile(r'^https?://.+')

    def validate(self, article: dict) -> list:
        errors = []

        headline = article.get('headline', '')
        if not headline:
            errors.append('headline: missing or empty')
        elif len(headline) < self.MIN_HEADLINE_LEN:
            errors.append(f'headline: too short ({len(headline)} chars)')
        elif len(headline) > self.MAX_HEADLINE_LEN:
            errors.append(f'headline: too long ({len(headline)} chars)')

        url = article.get('url', '')
        if not url:
            errors.append('url: missing')
        elif not self.URL_PATTERN.match(url):
            errors.append(f'url: invalid format — {url[:50]}')

        url_hash = article.get('url_hash', '')
        if not url_hash or len(url_hash) != 32:
            errors.append(f'url_hash: invalid (got: {url_hash!r})')

        published_at = article.get('published_at')
        if not published_at:
            errors.append('published_at: missing')
        elif not isinstance(published_at, datetime):
            errors.append(f'published_at: not a datetime (got {type(published_at).__name__})')

        if not article.get('source'):
            errors.append('source: missing')

        summary = article.get('summary', '')
        if summary and len(summary) > self.MAX_SUMMARY_LEN:
            errors.append(f'summary: too long ({len(summary)} chars)')

        return errors