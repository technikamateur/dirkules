import datetime
from .models import Drive, Partitions
from . import db, app

from .drive_manager import DriveManager

dm = DriveManager()


def update_drives():
    current_time = datetime.datetime.now()
    drive_dict = dm.get_all_drives()
    db_drives = Drive.query.all()
    for drive in drive_dict:
        serial = drive.get("serial")
        name = drive.get("name")
        smart = drive.get("smart")
        db_drive = db.session.query(Drive).filter(Drive.serial == serial).scalar()
        if db_drive is None:
            # this drive is not in db... add it!
            drive_obj = Drive(
                drive.get("name"), drive.get("model"), drive.get("serial"),
                drive.get("size"), drive.get("rota"), drive.get("rm"),
                drive.get("hotplug"), drive.get("state"), drive.get("smart"), current_time)
            db.session.add(drive_obj)
        else:
            # this drive is in db
            if db_drive.smart != smart:
                # smart state has changed
                db_drive.smart = smart
                if smart:
                    app.logger.error(
                        "SMART Value of {} ({}) has changed to: GOOD. But, you should be careful!".format(
                            db_drive.name, db_drive.model))
                else:
                    app.logger.error(
                        "SMART Value of {} ({}) has changed to: BAD. You should act now!".format(
                            db_drive.name, db_drive.model))
            if db_drive.name != name:
                # name (e.g. sda) has changed
                db_drive.name = name
                app.logger.critical("Drive " + db_drive.serial + " has changed for unknown reason!")
            # finally update time and mark it as not missing (if it was missing)
            db_drive.last_update = current_time
            if db_drive.missing:
                db_drive.missing = False
            # and remove this drive from db_drives
            try:
                db_drives.remove(db_drive)
            except ValueError:
                app.logger.error(
                    "The following drive {} ({}) has been found in database, but could not be found?!".format(
                        db_drive.name, db_drive.model))
    for drive in db_drives:
        drive.missing = True
        app.logger.error(
            "During a drive rescan: Following Drive could not be found: {} ({}).".format(drive.model, drive.serial))
    db.session.commit()


"""
old version of above
def get_drives():
    current_time = datetime.datetime.now()

    drive_dict = dm.get_all_drives()
    for drive in drive_dict:
        drive_obj = Drive(
            drive.get("name"), drive.get("model"), drive.get("serial"),
            drive.get("size"), drive.get("rota"), drive.get("rm"),
            drive.get("hotplug"), drive.get("state"), drive.get("smart"), current_time)
        ret = db.session.query(
            db.exists().where(Drive.serial == drive_obj.serial)).scalar()
        if ret:
            # drive in db, update last visited
            drive = db.session.query(Drive).filter(Drive.serial == drive_obj.serial).scalar()
            # but first it should be checked if those objects are identical
            if drive == drive_obj:
                # objects are identical
                drive.last_update = current_time
                if drive.missing:
                    drive.missing = False
            else:
                # objects are diffrent why?
                if drive.name != drive_obj.name:
                    # name has changed: e.g. from sda to sdb
                    drive.name = drive_obj.name
                    drive.last_update = current_time
                elif drive.smart != drive_obj.smart:
                    # smart value has changed
                    drive.smart = drive_obj.smart
                    drive.last_update = current_time
                    if drive_obj.smart:
                        app.logger.error(
                            "SMART Value of {} ({}) has changed to: GOOD. But, you should be careful!".format(
                                drive.name, drive.model))
                    else:
                        app.logger.error(
                            "SMART Value of {} ({}) has changed to: BAD. You should act now!".format(
                                drive.name, drive.model))
                else:
                    app.logger.critical("Drive " + drive.serial + " has changed for unknown reason!")
        else:
            # drive not in db. add new drive
            db.session.add(drive_obj)

    # check for old entries alias removed drives
    # old drive is list element
    old_drives = db.session.query(Drive).filter(Drive.last_update != current_time).all()
    if old_drives:
        for drive in old_drives:
            drive.missing = True
        app.logger.error("During a drive rescan: Following Drives could not be found: {}.".format(old_drives))
    db.session.commit()
"""


def get_partitions():
    drives = Drive.query.all()
    for drive in drives:
        if not drive.missing:
            Partitions.query.filter(Partitions.drive_id == drive.id).delete()
            part_dict = dm.part_for_disk(drive.name)
            for part in part_dict:
                if part.get("label") == "":
                    label = "none"
                else:
                    label = part.get("label")
                partition_obj = Partitions(part.get("name"), label, part.get("fs"), int(part.get("size")),
                                           part.get("uuid"), part.get("mount"), drive)
                drive.partitions.append(partition_obj)
    db.session.commit()
