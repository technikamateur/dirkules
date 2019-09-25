# -*- coding: utf-8 -*-
import subprocess


def autoclean(path):
    # remove all files older than 180 days
    subprocess.run(["sudo", "find", path, "-type", "f", "-mtime", "+180", "-delete"], shell=False,
                   timeout=90, check=True)
    subprocess.run(["sudo", "find", path, "-mindepth", "1", "-type", "d", "-empty", "-delete"], shell=False,
                   timeout=90, check=True)
