from dirkules.models import Drive

from dirkules import db


def get_drive_by_id(drive_id):
    """
    returns drive object for given id
    :param drive_id: id of drive (primary key)
    :type drive_id: int
    :return: Drive object
    :rtype: Drive
    """
    return Drive.query.get_or_404(drive_id)


def delete_drive_by_id(drive_id):
    """
    removes a drive with given id from db
    :param drive_id: drive's id
    :type drive_id: int
    :return: nothing
    :rtype:
    """
    try:
        drive = get_drive_by_id(drive_id)
        db.session.delete(drive)
        db.session.commit()
    except:
        db.session.rollback()
