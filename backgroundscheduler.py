from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
import logging

executors = {
    'default': {'type': 'threadpool', 'max_workers': 20},
    'processpool': ProcessPoolExecutor(max_workers=5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}


class BackgroundSchedulerConfigure:
    scheduler = None
    list_jobs = list()

    @staticmethod
    def configure():
        try:
            BackgroundSchedulerConfigure.scheduler = BackgroundScheduler()
            BackgroundSchedulerConfigure.scheduler.configure(
                executors=executors, job_defaults=job_defaults, timezone=utc)
            BackgroundSchedulerConfigure.scheduler.remove_all_jobs()
        except Exception as ex:
            logging.critical('Exception Background: {}'.format(ex))

    @staticmethod
    def add_job(func, interval_secs, id_job) -> bool:
        try:
            new_job = BackgroundSchedulerConfigure.scheduler.add_job(func,
                                                                     'interval',
                                                                     seconds=interval_secs,
                                                                     id=id_job,
                                                                     replace_existing=True)
            BackgroundSchedulerConfigure.list_jobs.append(new_job)
            logging.info('Background Launched Interval: {}'.format(interval_secs))
            return True
        except Exception as ex:
            logging.critical('Exception Background: {}'.format(ex))
            return False

    @staticmethod
    def start():
        try:
            BackgroundSchedulerConfigure.scheduler.start()
        except Exception as ex:
            logging.critical('Exception Background: {}'.format(ex))

    @staticmethod
    def stop():
        try:
            BackgroundSchedulerConfigure.scheduler.remove_all_jobs()
            BackgroundSchedulerConfigure.scheduler.shutdown()
        except Exception as ex:
            logging.error('Exception Background: {}'.format(ex))
