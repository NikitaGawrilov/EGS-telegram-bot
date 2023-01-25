from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime as dt
import datetime

def create_scheduler(job):
    notify_dt = datetime.time(hour=21, minute=5, second=0)
    scheduler = AsyncIOScheduler(timezone="Asia/Yekaterinburg")
    scheduler.add_job(job, trigger='cron', hour=notify_dt.hour,
                      minute=notify_dt.minute, start_date=dt.now())
    scheduler.start()