import os
from dirkules.models import Cleaning
from dirkules.hardware import autoclean
from dirkules import db, app


def clean_folders():
    for folder in Cleaning.query.all():
        if folder.state and os.path.isdir(folder.path):
            result = autoclean.autoclean(folder.path)
        elif not os.path.isdir(folder.path):
            app.logger.warning('folder not found: %s', folder.path)
    db.session.commit()
