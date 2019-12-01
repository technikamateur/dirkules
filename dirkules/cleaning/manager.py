from dirkules import db, scheduler

from dirkules.cleaning.models import Cleaning


def create_cleaning_obj(jobname, path, active):
    job = Cleaning(jobname, path, active)
    db.session.add(job)
    db.session.commit()


def disable():
    scheduler.pause_job("cleaning")


def enable():
    scheduler.resume_job("cleaning")


def running():
    if scheduler.get_job("cleaning").next_run_time is not None:
        return True
    else:
        return False
