# -*- coding: utf-8 -*-
from sqlalchemy import inspect
from dirkules import db
from dirkules.models import Cleaning


def db_object_as_dict(obj):
    return {
        c.key: getattr(obj, c.key)
        for c in inspect(obj).mapper.column_attrs
    }


def create_cleaning_obj(jobname, path, active):
    job = Cleaning(jobname, path, active)
    db.session.add(job)
    db.session.commit()
