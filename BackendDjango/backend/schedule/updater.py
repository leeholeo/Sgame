from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import schedule_api
import apscheduler


def start():
    print("jobs.updater.jobs")
    sched = BackgroundScheduler()
    sched.add_job(schedule_api, 'interval', seconds=3)
    sched.start()