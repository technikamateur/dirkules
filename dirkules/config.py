import os
from dirkules.telegram_config import *
import datetime
from logging.config import dictConfig
from apscheduler.jobstores.base import ConflictingIdError
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

# from apscheduler.jobstores.memory import MemoryJobStore

baseDir = os.path.abspath(os.path.dirname(__file__))
staticDir = os.path.join(baseDir, 'static')

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(baseDir, 'dirkules.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False


# The SCHEDULER_JOB_DEFAULTS configuration is per job, that means each job can execute at most 3 threads at the same time.
# The SCHEDULER_EXECUTORS is a global configuration, in this case, only 1 thread will be used for all the jobs.
# I believe the best way for you is to use max_workers: 1 when running locally

class SQLJobStore(SQLAlchemyJobStore):
    def add_job(self, job):
        try:
            super().add_job(job)
        except ConflictingIdError:
            pass


SCHEDULER_JOBSTORES = {'default': SQLJobStore(url='sqlite:///' + os.path.join(baseDir, 'dirkules_tasks.db'))}
# SCHEDULER_JOBSTORES = {'default': MemoryJobStore()}

SCHEDULER_EXECUTORS = {'default': {'type': 'threadpool', 'max_workers': 3}}

SCHEDULER_JOB_DEFAULTS = {'coalesce': True, 'max_instances': 1}

SCHEDULER_API_ENABLED = True

# should not be here in final version
SECRET_KEY = b'gf3iz3V!R3@Ny!ri'

JOBS = [
    {
        'id': 'refresh_disks',
        'func': 'dirkules.tasks:refresh_disks',
        'trigger': 'interval',
        'next_run_time': datetime.datetime.now(),
        'replace_existing': True,
        'seconds': 3600
    },
    {
        'id': 'cleaning',
        'func': 'dirkules.tasks:cleaning',
        'trigger': 'cron',
        'replace_existing': False,
        'hour': 12
    }
]

# Logging testing
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        },
        'telegram': {
            'format': '%(levelname)s#%(module)s#%(message)s',
        }},
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'default',
            'filename': 'dirkules.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 90,
        },
        'telegram': {
            'class': 'dirkules.TelegramLogging.TelegramHandler',
            'formatter': 'telegram',
            'token': TOKEN,
            'chat_id': CHAT_ID,
            'level': 'WARNING',
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi', 'file', 'telegram']
    }
})

# every handler can have it's own level. root level means global level if none is defined for handler.
# handler will be called on every logging event.
