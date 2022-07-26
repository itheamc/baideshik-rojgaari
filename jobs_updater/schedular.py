from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

from .handlers import JobHandler


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    job_handler = JobHandler()
    # scheduler.add_job(func=job_handler.male_jobs, trigger='interval', seconds=180, id="male_jobs_001",
    #                   replace_existing=False)
    scheduler.add_job(func=job_handler.female_jobs, trigger='interval', seconds=90, id="female_jobs_001",
                      replace_existing=False)
    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()


def print_this():
    print("Worked Done!!")
