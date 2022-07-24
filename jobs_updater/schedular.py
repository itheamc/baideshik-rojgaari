from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore

from .handlers import JobHandler


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    job_handler = JobHandler()
    scheduler.add_job(func=job_handler.male_jobs, trigger=CronTrigger(minute="*/2"), id="male_jobs_001",
                      max_instances=1,
                      replace_existing=True)
    scheduler.add_job(func=job_handler.female_jobs, trigger=CronTrigger(minute="*/3"), id="female_jobs_001",
                      max_instances=1,
                      replace_existing=True)
    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()


def _logger():
    print("Auto task completed")
