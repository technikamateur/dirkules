import datetime
import os

import dirkules.manager.driveManager as drive_man

from dirkules import app, db
from dirkules.cleaning.models import Cleaning
from dirkules.hardware import autoclean


def refresh_disks():
    drive_man.get_drives()
    drive_man.get_partitions()
    drive_man.pool_gen()


def cleaning():
    for folder in Cleaning.query.all():
        if folder.state and os.path.isdir(folder.path):
            autoclean.autoclean(folder.path)
            folder.time = datetime.datetime.now()
        elif folder.state and not os.path.isdir(folder.path):
            app.logger.error('Folder not found: {}'.format(folder.path))
    db.session.commit()
