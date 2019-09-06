# -*- coding: utf-8 -*-
import subprocess


def autoclean(path):
    # remove all files older than 180 days
    find = subprocess.Popen([
        "find \"" + path +
        "\" -type f -mtime +180 -delete -exec echo {} \\;"
    ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        universal_newlines=True,)
    try:
        out_remove, err_remove = find.communicate(timeout=500)
    except subprocess.TimeoutExpired:
        find.kill()
        out_remove, err_remove = find.communicate()

    err_rmdir = False
    try:
        subprocess.run(
            "find " + path + " -mindepth 1 -type d -empty -delete",
            shell=True, check=True)
    except subprocess.CalledProcessError:
        err_rmdir = True

    return [out_remove, err_remove, err_rmdir]
