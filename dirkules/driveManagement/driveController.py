# -*- coding: utf-8 -*-
import psutil
import subprocess
import os
from dirkules.models import Drive


def getAllDrives():
    #vorbereitung
    drives = []
    driveDict = []
    keys = ['device', 'name', 'smart', 'size']

    blkid = subprocess.Popen(["hwinfo --disk --short"],
                             stdout=subprocess.PIPE,
                             shell=True,
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
        line = line.replace(" ", "", 15)
        values.append(line[:8])
        values.append(line[8:])
        values.append(smartPassed(values[0]))
        values.append(getTotalSize(values[0]))
        driveDict.append(dict(zip(keys, values)))
        db.session.add(Drive(values[0], values[1], values[2], values[3]))
        db.session.commit()
    return driveDict


def smartPassed(device):
    passed = False
    smartctl = subprocess.Popen(["smartctl -H " + device],
                                stdout=subprocess.PIPE,
                                shell=True,
                                universal_newlines=True)
    while True:
        line = smartctl.stdout.readline()
        if "PASSED" in line:
            passed = True
        elif line == '':
            break
        else:
            pass
    smartctl.stdout.close()
    return passed


def getTotalSize(device):
    # Hier könnte man auch die Partitionen mit abfragen
    drives = []
    fdisk = subprocess.Popen(["fdisk -l"],
                             stdout=subprocess.PIPE,
                             shell=True,
                             universal_newlines=True)
    grepedDrives = subprocess.Popen(["grep", device],
                                    stdin=fdisk.stdout,
                                    stdout=subprocess.PIPE,
                                    universal_newlines=True)
    while True:
        line = grepedDrives.stdout.readline()
        if line != '':
            drives.append(line.rstrip())
        else:
            break
    fdisk.stdout.close()
    firstLine = drives[0].split(" ")
    size = firstLine[2] + " " + firstLine[3][:-1]
    return size


#nicht verwenden
def OLDgetAllDrives():

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
        elif any(not "LABEL" in s
                 for s in arrayline) and any("UUID_SUB" in s
                                             for s in arrayline):
            values.append("Was weiß ich...")
            values.append(arrayline[3][6:-1])
            values.append("(keiner)")
        else:
            values.append("Was weiß ich...")
            values.append(arrayline[2][6:-1])
            values.append("(keiner)")
        #Dict für Jinja anfügen
        driveDict.append(dict(zip(keys, values)))
    return driveDict
