from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import schedule_api


def start():
    """
    This function initializes the scheduler and schedules the API job to run every period of time.

    Args:
        None

    Returns:
        None

    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_api, 'interval', seconds=60)
    scheduler.start()
