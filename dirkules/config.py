import os
#from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.memory import MemoryJobStore

baseDir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(baseDir, 'dirkules.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# The SCHEDULER_JOB_DEFAULTS configuration is per job, that means each job can execute at most 3 threads at the same time.
# The SCHEDULER_EXECUTORS is a global configuration, in this case, only 1 thread will be used for all the jobs.
# I believe the best way for you is to use max_workers: 1 when running locally

#SCHEDULER_JOBSTORES = {'default': SQLAlchemyJobStore(url='sqlite:///' + os.path.join(baseDir, 'dirkules.db'))}
SCHEDULER_JOBSTORES = {'default': MemoryJobStore()}

SCHEDULER_EXECUTORS = {'default': {'type': 'threadpool', 'max_workers': 3}}

SCHEDULER_JOB_DEFAULTS = {'coalesce': False, 'max_instances': 1}

SCHEDULER_API_ENABLED = True

SECRET_KEY = b'gf3iz3V!R3@Ny!ri'