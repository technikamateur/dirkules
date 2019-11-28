# -*- coding: utf-8 -*-
from dirkules.hardware.btrfsTools import create_pool
from dirkules.models import Drive


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
    label = str(form.name.data)
    drives = list()
    str_drives = form.drives.data.split(",")
    for d in str_drives:
        drives.append(Drive.query.filter(Drive.name == d).scalar())
    if int(form.raid_config.data) == 1:
        raid = "single"
    elif int(form.raid_config.data) == 2:
        raid = "raid0"
    elif int(form.raid_config.data) == 3:
        raid = "raid1"
    # if only one drive has been selected: always use single
    if len(drives) == 1:
        raid = "single"
    mount_options = ["defaults"]
    if bool(form.inode_cache.data):
        mount_options.append("inode_cache")
    if int(form.space_cache.data) == 2:
        mount_options.append("space_cache=v1")
    elif int(form.space_cache.data) == 3:
        mount_options.append("space_cache=v2")
    if int(form.compression.data) == 2:
        mount_options.append("compress=zlib")
    elif int(form.compression.data) == 3:
        mount_options.append("compress=lzo")
    if pure_ssd(drives) and not pure_hdd(drives):
        mount_options.append("ssd")
    elif pure_hdd(drives) and not pure_ssd(drives):
        mount_options.append("autodefrag")
    # now we are ready to create the pool.
    # Warning: drives contains objects, not names!! Use drive.name
    create_pool(label, drives, raid, mount_options)


def pure_ssd(drives):
    for d in drives:
        if d.rota or d.hotplug:
            return False
    return True


def pure_hdd(drives):
    for d in drives:
        if not d.rota or d.hotplug:
            return False
    return True
