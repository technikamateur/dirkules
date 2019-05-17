from dirkules import db
from dirkules.models import Drive, Partitions
from dirkules.hardware import drive as hardware_drives
from sqlalchemy.sql.expression import exists


def get_partitions(drive_id, force=False):
    drive = db.session.query(Drive).get(drive_id)
    partdict = hardware_drives.part_for_disk(drive.name)
    for part in partdict:
        part_obj = Partitions(drive.id, part.get("name"), part.get("label"), part.get("fs"), int(part.get("size")),
                              part.get("uuid"), part.get("mount"), drive)
        existence = db.session.query(exists().where(Partitions.uuid == part_obj.uuid)).scalar()
        if existence:
            print(part.get("name") + " in db")
        else:
            print(part.get("name") + " NICHT in db")
            db.session.add(part_obj)
            db.session.commit()
