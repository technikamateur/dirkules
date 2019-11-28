from dirkules import db

from dirkules.cleaning.models import Cleaning


def create_cleaning_obj(jobname, path, active):
    job = Cleaning(jobname, path, active)
    db.session.add(job)
    db.session.commit()
