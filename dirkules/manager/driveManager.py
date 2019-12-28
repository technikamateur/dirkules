from dirkules import db
from dirkules.models import Drive, Partitions, Pool
from dirkules.hardware import drive as hardware_drives
import dirkules.hardware.btrfsTools as btrfsTools
import dirkules.hardware.ext4Tools as ext4Tools


# all partitions with given drive_name will be deleted and freshly added
# this is much faster than querying all partitions for a specific drive and check for changes
def get_partitions():
    drives = Drive.query.all()
    for drive in drives:
        if not drive.missing:
            Partitions.query.filter(Partitions.drive_id == drive.id).delete()
            part_dict = hardware_drives.part_for_disk(drive.name)
            for part in part_dict:
                if part.get("label") == "":
                    label = "none"
                else:
                    label = part.get("label")
                partition_obj = Partitions(part.get("name"), label, part.get("fs"), int(part.get("size")),
                                           part.get("uuid"), part.get("mount"), drive)
                drive.partitions.append(partition_obj)
    db.session.commit()


def pool_gen():
    part_dict = dict()
    Pool.query.delete()
    # creates map uuid is key, partitions are values
    for part in Partitions.query.all():
        if part.uuid in part_dict:
            part_dict[part.uuid].append(part)
        else:
            part_dict.update({part.uuid: [part]})

    for key, value in part_dict.items():
        if len(value) == 1:
            raid = "single"
        else:
            raid = "unbekannt"
        drives = ""
        for part in value:
            drives = drives + str(Drive.query.get(part.drive_id).name) + ","
        drives = drives[:-1]
        value = value[0]
        missing = absent_drive(drives)
        if missing is not None:
            missing = ",".join(str(x.name) for x in missing)
        if value.fs == "btrfs":
            if value.mountpoint:
                memory_map = btrfsTools.get_space(value.mountpoint)
                raid_map = btrfsTools.get_raid(value.mountpoint)
            else:
                memory_map = (dict(zip(['total', 'free'], [int(value.size), 2])))
                raid_map = (dict(zip(['data_raid', 'data_ratio', 'meta_raid', 'meta_ratio'],
                                     ['unbekannt', '1.00', 'unbekannt', '1.00'])))
            pool_obj = Pool(value.label, memory_map.get("total"), memory_map.get("free"), raid_map.get("data_raid"),
                            raid_map.get("data_ratio"), raid_map.get("meta_raid"), raid_map.get("meta_ratio"), value.fs,
                            value.mountpoint, "not implemented", drives, get_pool_health(drives), missing)
            db.session.add(pool_obj)

        elif value.fs == "ext4":
            if value.mountpoint:
                free_space = ext4Tools.get_free_space(value.mountpoint)
            else:
                free_space = 2
            pool_obj = Pool(value.label, value.size, free_space, raid, 1.00, raid, 1.00, value.fs, value.mountpoint,
                            "not implemented", drives, get_pool_health(drives), missing)
            db.session.add(pool_obj)
    db.session.commit()


def get_pool_health(drive_list):
    """
    :param drive_list: contains drives which belongs to pool
    :type drive_list: list
    :return: the total health of the pool, based on drives health
    :rtype: boolean
    """
    drive_split = drive_list.split(",")
    for drive in drive_split:
        db_drive = db.session.query(Drive).filter(Drive.name == drive).scalar()
        if db_drive.smart is not True:
            return False
    return True


def absent_drive(drive_list):
    """
    :param drive_list: contains drives which belongs to pool
    :return: List of absent drives or None
    """
    missing = list()
    drive_split = drive_list.split(",")
    for drive in drive_split:
        db_drive = db.session.query(Drive).filter(Drive.name == drive).scalar()
        if db_drive.missing:
            missing.append(db_drive)
    if not missing:
        return None
    else:
        return missing


def delete_drive(drive):
    """
    removes a given drive object (including cascades) from db
    :param drive: The drive
    :type drive: Drive
    :return: nothing
    :rtype:
    """
    try:
        db.session.delete(drive)
        db.session.commit()
    except:
        db.session.rollback()


def get_drive_by_id(drive_id):
    """
    returns drive object for given id
    :param drive_id: id of drive (primary key)
    :type drive_id: int
    :return: Drive object
    :rtype: Drive
    """
    drive = Drive.query.get(drive_id)
    if drive is not None:
        return drive
    else:
        raise LookupError
