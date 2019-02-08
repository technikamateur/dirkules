# -*- coding: utf-8 -*-
import psutil
import subprocess
import os


def getAllDrives():

    drives = []
    driveDict = []
    blkid = subprocess.Popen(["blkid"],
                             stdout=subprocess.PIPE,
                             universal_newlines=True)
    grepedDrives = subprocess.Popen(["grep", "/dev/sd"],
                                    stdin=blkid.stdout,
                                    stdout=subprocess.PIPE,
                                    universal_newlines=True)
    while True:
        line = grepedDrives.stdout.readline()
        if line != '':
            drives.append(line.rstrip())
        else:
            break
    blkid.stdout.close()
    for line in drives:
        tempDict = {
            'device': "unknown",
            'mountpoint': "unknown",
            'fstype': "unknown",
            'label': "unknown"
        }
        arrayline = line.split(' ')
        device = arrayline[0][:-1]
        tempDict.update({'device': device})
        driveDict.append(tempDict)
    return driveDict
