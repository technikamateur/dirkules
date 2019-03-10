# -*- coding: utf-8 -*-
from sqlalchemy import inspect


def db_object_as_dict(obj):
    return {
        c.key: getattr(obj, c.key)
        for c in inspect(obj).mapper.column_attrs
    }
