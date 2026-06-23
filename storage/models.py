from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Article:
    headline: str
    url: str
    url_hash: str
    source_name: str
    published_at: datetime
    summary: str = ''
    scraped_at: datetime = field(default_factory=datetime.utcnow)
    id: int = None


@dataclass
class SentimentScore:
    article_id: int
    score: float
    magnitude: float
    label: str
    model_used: str = 'vader'


@dataclass
class IngestionLog:
    source_id: int
    articles_fetched: int = 0
    articles_inserted: int = 0
    articles_skipped: int = 0
    articles_failed: int = 0
    errors: int = 0
    duration_seconds: float = 0.0
    status: str = 'success'