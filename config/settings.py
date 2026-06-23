import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/marketpulse')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
PIPELINE_INTERVAL_HOURS = int(os.getenv('PIPELINE_INTERVAL_HOURS', '6'))
DATA_FRESHNESS_SLA_HOURS = int(os.getenv('DATA_FRESHNESS_SLA_HOURS', '8'))

SENTIMENT_POSITIVE_THRESHOLD = 0.05
SENTIMENT_NEGATIVE_THRESHOLD = -0.05
ANOMALY_Z_SCORE_THRESHOLD = -2.0
MIN_ENTITY_LENGTH = 2
DASHBOARD_OUTPUT_PATH = os.getenv('DASHBOARD_OUTPUT_PATH', 'dashboard.html')