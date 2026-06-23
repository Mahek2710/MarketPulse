from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import logging

from ingestion.run_pipeline import run_full_pipeline
from config.settings import PIPELINE_INTERVAL_HOURS

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)


def start_scheduler():
    scheduler = BlockingScheduler(timezone='Asia/Kolkata')

    scheduler.add_job(
        func=run_full_pipeline,
        trigger=IntervalTrigger(hours=PIPELINE_INTERVAL_HOURS),
        id='marketpulse_ingestion',
        name='MarketPulse Full Pipeline',
        replace_existing=True,
        next_run_time=datetime.now()
    )

    logger.info(f'Scheduler started — runs every {PIPELINE_INTERVAL_HOURS} hours.')
    logger.info('Press Ctrl+C to stop.')

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info('Scheduler stopped cleanly.')


if __name__ == '__main__':
    start_scheduler()