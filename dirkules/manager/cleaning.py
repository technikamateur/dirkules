import os
from dirkules.models import Cleaning
from dirkules.hardware import autoclean
from dirkules import db, app


def clean_folders():
    for folder in Cleaning.query.all():
        if folder.state and os.path.isdir(folder.path):
            result = autoclean.autoclean(folder.path)
            if result[1] != '':
                app.logger.error("Deleting old files exited with errors: {}".format(result[1]))
            elif result[2]:
                app.logger.error("Removing empty folders exited with errors.")
        elif not os.path.isdir(folder.path):
            app.logger.warning('Folder not found: {}'.format(folder.path))
    db.session.commit()
