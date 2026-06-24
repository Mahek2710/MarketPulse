# MarketPulse

Financial news sentiment tracker for Indian equity markets. Scrapes articles from MoneyControl and Economic Times, tags them by company, scores sentiment, and surfaces trends through a React dashboard and REST API.

---

## Tech Stack

- **Frontend** — React, Recharts, Axios
- **Backend** — Node.js, Express
- **Database** — MongoDB (Mongoose)
- **Scraping & NLP** — Python (feedparser, VADER), called from Node via child_process
- **Scheduling** — node-cron

---

## Features

- Pulls from MoneyControl Markets and Economic Times Markets RSS feeds every 6 hours
- Tags each article with the company it mentions (matched against a list of NSE-listed stocks)
- Scores sentiment using VADER — compound score from -1.0 to +1.0
- Deduplicates using URL hashing so the same article from two sources is stored once
- Invalid articles (missing headline, bad URL, unparseable timestamp) are written to a separate collection with the failure reason rather than silently dropped
- Logs every scraper run — articles fetched, inserted, skipped, errors, duration
- React dashboard with company search, date filters, sentiment trend charts, and a paginated article table

---

## Project Structure

```
marketpulse/
├── client/
│   └── src/
│       ├── components/
│       │   ├── Dashboard.jsx
│       │   ├── SentimentChart.jsx
│       │   ├── ArticleTable.jsx
│       │   └── CompanySearch.jsx
│       └── App.jsx
│
├── server/
│   ├── models/
│   │   ├── Article.js
│   │   ├── IngestionLog.js
│   │   └── FailedArticle.js
│   ├── routes/
│   │   ├── articles.js
│   │   ├── sentiment.js
│   │   └── pipeline.js
│   ├── scheduler.js
│   └── index.js
│
├── scraper/
│   ├── scraper.py
│   ├── sentiment.py
│   └── requirements.txt
│
└── analytics/
    ├── rolling_sentiment.js
    ├── anomaly_detection.js
    ├── sector_heatmap.js
    └── pipeline_health.js
```

---

## API

```
GET  /api/articles                    paginated article feed
GET  /api/articles?company=Infosys    filter by company
GET  /api/articles?from=2026-06-01    filter by date
GET  /api/sentiment/:company          sentiment trend for a company
GET  /api/sentiment/anomalies         companies with unusual sentiment drops
GET  /api/pipeline/health             scraper run history and stats
```

---

## Analytics

MongoDB aggregation pipelines in `/analytics`:

- **Rolling sentiment** — 7-day moving average per company
- **Anomaly detection** — flags companies whose recent sentiment is significantly below their 30-day average
- **Sector heatmap** — week-on-week sentiment by sector (Banking, IT, Energy, etc.)
- **Pipeline health** — tracks ingestion success rate over time

---

## Setup

```bash
# Backend
cd server
npm install
cp .env.example .env        # add MONGO_URI and PORT
npm start

# Frontend
cd client
npm install
npm start

# Python scraper (auto-triggered by scheduler, or run manually)
cd scraper
pip install -r requirements.txt
python scraper.py
```

---

## Environment Variables

```
MONGO_URI=mongodb://localhost:27017/marketpulse
PORT=5000
SCRAPE_INTERVAL_HOURS=6
```
