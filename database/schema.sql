CREATE TABLE IF NOT EXISTS sources (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    url         VARCHAR(500),
    feed_url    VARCHAR(500) NOT NULL,
    is_active   BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS companies (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(200) NOT NULL UNIQUE,
    ticker      VARCHAR(20),
    sector      VARCHAR(100),
    aliases     TEXT[],
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS articles (
    id              SERIAL PRIMARY KEY,
    headline        TEXT NOT NULL,
    summary         TEXT,
    url             VARCHAR(1000),
    url_hash        CHAR(32) UNIQUE NOT NULL,
    source_id       INTEGER REFERENCES sources(id) ON DELETE SET NULL,
    published_at    TIMESTAMP NOT NULL,
    scraped_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS article_companies (
    article_id      INTEGER REFERENCES articles(id) ON DELETE CASCADE,
    company_id      INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    PRIMARY KEY (article_id, company_id)
);

CREATE TABLE IF NOT EXISTS sentiment_scores (
    id          SERIAL PRIMARY KEY,
    article_id  INTEGER REFERENCES articles(id) ON DELETE CASCADE UNIQUE,
    score       DECIMAL(5,4) NOT NULL,
    magnitude   DECIMAL(5,4),
    label       VARCHAR(20) CHECK (label IN ('positive','negative','neutral')),
    model_used  VARCHAR(50) DEFAULT 'vader',
    scored_at   TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ingestion_logs (
    id                  SERIAL PRIMARY KEY,
    run_at              TIMESTAMP DEFAULT NOW(),
    source_id           INTEGER REFERENCES sources(id),
    articles_fetched    INTEGER DEFAULT 0,
    articles_inserted   INTEGER DEFAULT 0,
    articles_skipped    INTEGER DEFAULT 0,
    articles_failed     INTEGER DEFAULT 0,
    errors              INTEGER DEFAULT 0,
    duration_seconds    DECIMAL(8,2),
    status              VARCHAR(20) DEFAULT 'success'
                        CHECK (status IN ('success','partial','failed'))
);

CREATE TABLE IF NOT EXISTS failed_ingestion (
    id              SERIAL PRIMARY KEY,
    raw_data        JSONB,
    failure_reason  TEXT NOT NULL,
    source_id       INTEGER REFERENCES sources(id),
    attempted_at    TIMESTAMP DEFAULT NOW(),
    resolved        BOOLEAN DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_articles_published ON articles(published_at DESC);
CREATE INDEX IF NOT EXISTS idx_sentiment_article ON sentiment_scores(article_id);
CREATE INDEX IF NOT EXISTS idx_sentiment_score ON sentiment_scores(score);
CREATE INDEX IF NOT EXISTS idx_articles_source ON articles(source_id);
CREATE INDEX IF NOT EXISTS idx_ac_company ON article_companies(company_id);
CREATE INDEX IF NOT EXISTS idx_logs_run_at ON ingestion_logs(run_at DESC);
CREATE INDEX IF NOT EXISTS idx_failed_resolved ON failed_ingestion(resolved) WHERE resolved = FALSE;