# -*- coding: utf-8 -*-
import subprocess
import os
from dirkules.models import Drive
from dirkules import db


def getAllDrives():
    #vorbereitung
    drives = []
    driveDict = []  # ist eine Liste, enthält für jede HDD ein dict
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
        # Effizienter machen mit newLine = ' '.join(line.split())
        values = []
        line = line.replace(" ", "", 15)
        values.append(line[:8])
        values.append(line[8:])
        values.append(smartPassed(values[0]))
        values.append(getTotalSize(values[0]))
        driveDict.append(dict(zip(keys, values)))
    sortedDriveDict = sorted(driveDict, key=lambda drive: drive['device'])

    #add to db
    #db.session.add(Drive(values[0], values[1], values[2], values[3]))
    #db.session.commit()

    return sortedDriveDict


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


def getPartitions(device):
    partDict = []  # ist eine Liste, enthält für jede part ein dict
    drives = []
    # name = sda1 zum Beispiel
    keys = ['name', 'fs', 'size', 'uuid', 'mountpoint', 'label']

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
    del drives[0]
    for line in drives:
        line = line.replace("*", "")
        newLine = ' '.join(line.split())
        newLine = newLine.split(" ")
        if newLine[5] != "5":  #Ungültige Partitionen herausfiltern
            values = []
            values.append(newLine[0])
            # Für jede Partition muss nun blkid ausgeführt werden, um weitere Informationen zu erhalten
            partDet = partDetails(newLine[0])
            values.append(partDet[2])
            values.append(newLine[4])
            values.append(partDet[1])
            values.append("mountpoint")
            values.append(partDet[0])
            partDict.append(dict(zip(keys, values)))
        else:
            pass
    return partDict


def partDetails(part):
    values = []
    blkid = subprocess.Popen(["blkid"],
                             stdout=subprocess.PIPE,
                             shell=True,
                             universal_newlines=True)
    grepedDrives = subprocess.Popen(["grep", part],
                                    stdin=blkid.stdout,
                                    stdout=subprocess.PIPE,
                                    universal_newlines=True)

    line = grepedDrives.stdout.readline()
    partDet = line.rstrip()
    blkid.stdout.close()

    partDet = partDet.split(" ")

    if any("LABEL" in s for s in partDet):
        if any("UUID_SUB" in s for s in partDet):
            values.append(partDet[1][7:-1])
            values.append(partDet[2][6:-1])
            values.append(partDet[4][6:-1])
        else:
            values.append(partDet[1][7:-1])
            values.append(partDet[2][6:-1])
            values.append(partDet[3][6:-1])

    elif any(not "LABEL" in s for s in partDet) and any("UUID_SUB" in s
                                                        for s in partDet):
        values.append("kein Label")
        values.append(partDet[1][6:-1])
        values.append(partDet[3][6:-1])
    else:
        values.append("kein Label")
        values.append(partDet[1][6:-1])
        values.append(partDet[2][6:-1])
    return values  # Format: Label, UUID, FS
