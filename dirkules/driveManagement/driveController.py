# -*- coding: utf-8 -*-
import psutil
import subprocess
import os


def getAllDrives():

    #vorbereitung
    drives = []
    driveDict = []
    keys = ['device', 'mountpoint', 'fstype', 'label']

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
        values = []
        #Informationen aufbereiten
        arrayline = line.split(' ')
        values.append(arrayline[0][:-1])
        if any("LABEL" in s for s in arrayline):
            if any("UUID_SUB" in s for s in arrayline):
                values.append("Was weiß ich...")
                values.append(arrayline[4][6:-1])
                values.append("Weiß ich auch noch nicht...")
            else:
                values.append("Was weiß ich...")
                values.append(arrayline[3][6:-1])
                values.append("Weiß ich auch noch nicht...")
        elif any(not "LABEL" in s for s in arrayline) and any("UUID_SUB" in s for s in arrayline):
            values.append("Was weiß ich...")
            values.append(arrayline[3][6:-1])
            values.append("Weiß ich auch noch nicht...")
        else:
            values.append("Was weiß ich...")
            values.append(arrayline[2][6:-1])
            values.append("Weiß ich auch noch nicht...")
        #Dict für Jinja anfügen
        driveDict.append(dict(zip(keys, values)))
    return driveDict
