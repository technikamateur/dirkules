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
    for drive in drive_split:
        db_drive = db.session.query(Drive).filter(Drive.name == drive).scalar()
        if db_drive.smart is not True:
            return False
    return True


def get_empty_drives():
    drives = Drive.query.all()
    choices = list()
    for drive in drives:
        if not drive.missing and not is_system_drive(drive):
            label = drive.name + ": " + drive.model + " (" + sizeof_fmt(drive.size) + ")"
            choices.append((drive.name, label))
    return choices


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def is_system_drive(drive):
    for p in drive.partitions:
        if "/" == p.mountpoint or "/home" == p.mountpoint:
            return True
    return False

def create_btrfs_pool(form):
    label = form.name.data
    if int(form.raid_config.data) == 1:
        raid = "single"
    elif int(form.raid_config.data) == 2:
        raid = "raid0"
    elif int(form.raid_config.data) == 3:
        raid = "raid1"
    drives = form.drives.data.split(",")
    mount_options = ["defaults"]
    if bool(form.inode_cache.data):
        mount_options.append("inode_cache")
    if int(form.space_cache.data) == 2:
        mount_options.append("space_cache=v1")
    elif int(form.space_cache.data) == 3:
        mount_options.append("space_cache=v2")