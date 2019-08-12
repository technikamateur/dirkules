# -*- coding: utf-8 -*-
from sqlalchemy import inspect
from dirkules import db
from dirkules.models import Cleaning, Partitions, Drive


def db_object_as_dict(obj):
    return {
        c.key: getattr(obj, c.key)
        for c in inspect(obj).mapper.column_attrs
    }


def create_cleaning_obj(jobname, path, active):
    job = Cleaning(jobname, path, active)
    db.session.add(job)
    db.session.commit()

def get_pool_health(drive_list):
    drive_split = drive_list.split(",")
    health = True
    for drive in drive_split:
        db_drive = db.session.query(Drive).filter(Drive.name == drive).scalar()
        if db_drive.smart is not True:
            health = False
    return health