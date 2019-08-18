# -*- coding: utf-8 -*-
import subprocess
from dirkules import db
from dirkules.models import Cleaning


def autoclean():
    paths = []
    paths.append("/media/data-raid/@dataDaniel/.recycle")
    paths.append("/media/data-raid/@dataShare/.recycle")
    for path in paths:
        # remove all files older than 180 days
        find = subprocess.Popen([
            "find \"" + path +
            "\" -type f -mtime +180 -delete -exec echo {} \\;"
        ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            universal_newlines=True)
        out, err = find.communicate()
        if "/" not in out:
            for element in out:
                pass
                # db.session.add(Cleaning(element))
            # db.session.commit()
        # remove all empty folders
        subprocess.run(
            "find \"" + path + "\" -type d -empty -exec rmdir {} +",
            shell=True)
