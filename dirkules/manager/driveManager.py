from dirkules import db
from dirkules.models import Drive, Partitions, Pool
from dirkules.hardware import drive as hardware_drives
from sqlalchemy.sql.expression import exists, and_


# get partitions from hardware (method) and store in db
# contains all logic like replacing, removing in future
def get_partitions(drive_id, force=False):
    drive = db.session.query(Drive).get(drive_id)
    partdict = hardware_drives.part_for_disk(drive.name)
    for part in partdict:
        existence = db.session.query(
            exists().where(and_(Partitions.uuid == part.get("uuid"), Partitions.name == part.get("name")))).scalar()
        if not existence:
            part_obj = Partitions(drive.id, part.get("name"), part.get("label"), part.get("fs"), int(part.get("size")),
                                  part.get("uuid"), part.get("mount"), drive)
            print(part.get("name") + " NICHT in db")
            db.session.add(part_obj)
            db.session.commit()


def pool_gen():
    part_dict = dict()
    final_part_dict = list()
    for part in Partitions.query.all():
        if part.uuid in part_dict:
            part_dict[part.uuid].append(part)
        else:
            part_dict.update({part.uuid: [part]})

    for key, value in part_dict.items():
        if len(value) == 1:
            raid = "Single"
        else:
            raid = "unknown RAID"
        parts = ""
        for part in value:
            parts = parts + str(part.id) + ","
        parts = parts[:-1]
        value = value[0]
        existence = db.session.query(exists().where(Pool.partitions == parts)).scalar()
        # FS is ext4 or BtrFS and there is no element in db with such a part constalation
        # TODO: Warning: If a partition has been added to a raid, the disk will still exist
        # because not removed and the pool will be displayed twice, because not same part constallation
        if (value.fs == "btrfs" or value.fs == "ext4") and not existence:
            pool_obj = Pool("not implemented", value.size, 154554, raid, value.fs, value.mountpoint,
                            "not implemented", parts)
            db.session.add(pool_obj)
            db.session.commit()
