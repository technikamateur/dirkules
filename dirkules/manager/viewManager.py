# -*- coding: utf-8 -*-
from sqlalchemy import inspect
from dirkules import db
from dirkules.models import Cleaning, Partitions


def db_object_as_dict(obj):
    return {
        c.key: getattr(obj, c.key)
        for c in inspect(obj).mapper.column_attrs
    }


def create_cleaning_obj(jobname, path, active):
    job = Cleaning(jobname, path, active)
    db.session.add(job)
    db.session.commit()


# TODO: Create class out of this
def usable_memory():
    part_dict = dict()
    final_part_dict = list()
    for part in Partitions.query.all():
        if part.uuid in part_dict:
            part_dict[part.uuid].append(part)
        else:
            part_dict.update({part.uuid: [part]})
    for key, value in part_dict.items():
        if len(value) > 1:
            parts = list()
            for part in value:
                parts.append(part.name)
            value = value[0]
            if value.fs == "btrfs" or value.fs == "ext4":
                final_part_dict.append(
                    {"label": value.label, "part": parts, "fs": value.fs, "mpoint": value.mountpoint})
        else:
            value = value[0]
            if value.fs == "btrfs" or value.fs == "ext4":
                final_part_dict.append(
                    {"label": value.label, "part": value.name, "fs": value.fs, "mpoint": value.mountpoint})
    return final_part_dict
