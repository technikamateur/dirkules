import os
from dirkules.models import Cleaning
from dirkules.hardware import autoclean
from dirkules import db


def clean_folders():
    for folder in Cleaning.query.all():
        if folder.state and os.path.isdir(folder.path):
            result = autoclean.autoclean(folder.path)
            print(result)
            print(result[0])
            print(result[1])
    db.session.commit()