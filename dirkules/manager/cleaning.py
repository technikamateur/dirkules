import os
from dirkules.models import Cleaning
from dirkules.hardware import autoclean
from dirkules import db, app, scheduler


def clean_folders():
    for folder in Cleaning.query.all():
        if folder.state and os.path.isdir(folder.path):
            result = autoclean.autoclean(folder.path)
            if result[1] != '':
                app.logger.error("Deleting old files exited with errors: {}".format(result[1]))
            elif result[2]:
                app.logger.error("Removing empty folders exited with errors. No further information available.")
        elif not os.path.isdir(folder.path):
            app.logger.error('Folder not found: {}'.format(folder.path))
    db.session.commit()


def disable():
    scheduler.pause_job("cleaning")


def enable():
    scheduler.resume_job("cleaning")


def running():
    if scheduler.get_job("cleaning").next_run_time is not None:
        return True
    else:
        return False
