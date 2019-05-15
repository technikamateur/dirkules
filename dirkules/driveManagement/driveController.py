# -*- coding: utf-8 -*-
import subprocess
from dirkules.models import Drive
from dirkules import db
from sqlalchemy.sql.expression import exists


def getAllDrives():
    drives = []
    driveDict = []
    keys = [
        'name', 'model', 'serial', 'size', 'rota', 'rm', 'hotplug', 'state',
        'smart'
    ]

    lsblk = subprocess.Popen(
        ["lsblk -I 8 -d -b -o NAME,MODEL,SERIAL,SIZE,ROTA,RM,HOTPLUG"],
        stdout=subprocess.PIPE,
        shell=True,
        universal_newlines=True)
    while True:
        line = lsblk.stdout.readline()
        if line != '':
            drives.append(line.rstrip())
        else:
            break
    lsblk.stdout.close()
    del drives[0]
    for line in drives:
        newLine = ' '.join(line.split())
        newLine = newLine.split(" ")
        while len(newLine) > 7:
            newLine[1] = newLine[1] + " " + newLine[2]
            del newLine[2]
        values = []
        for i in range(len(keys) - 2):
            if newLine[i] == "0":
                values.append(False)
            elif newLine[i] == "1":
                values.append(True)
            else:
                values.append(newLine[i])
        values.append("running")
        values.append(smartPassed("/dev/" + values[0]))
        driveDict.append(dict(zip(keys, values)))
    sortedDriveDict = sorted(driveDict, key=lambda drive: drive['name'])

    # add to db
    for drive in sortedDriveDict:
        driveObj = Drive(
            drive.get("name"), drive.get("model"), drive.get("serial"),
            drive.get("size"), drive.get("rota"), drive.get("rm"),
            drive.get("hotplug"), drive.get("state"), drive.get("smart"))
        ret = db.session.query(
            exists().where(Drive.serial == driveObj.serial)).scalar()
        if ret:
            print(drive.get("name") + " in db")
            print("Mache nichts...")
        else:
            print(drive.get("name") + " NICHT in db")
            db.session.add(driveObj)
            db.session.commit()

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


def part_for_disk(device):
    # lsblk /dev/sdd -b -o NAME,LABEL,FSTYPE,SIZE,UUID,MOUNTPOINT
    parts = []
    partdict = list()
    keys = ['name', 'label', 'fs', 'size', 'uuid', 'mount']

    lsblk = subprocess.Popen(
        ["lsblk " + device + " -l -b -o NAME,LABEL,FSTYPE,SIZE,UUID,MOUNTPOINT"],
        stdout=subprocess.PIPE,
        shell=True,
        universal_newlines=True)
    while True:
        line = lsblk.stdout.readline()
        if line != '':
            parts.append(line.rstrip())
        else:
            break
    lsblk.stdout.close()
    del parts[1]
    element_length = list()
    counter = 0
    last_letter = 0
    pre_value = " "
    for char in parts[0]:
        if char != " " and pre_value == " ":
            element_length.append(counter)
        counter += 1
        pre_value = char
        # size ist rechtsbuendig. Extra Behandlung
        # TODO: Besser machen
        if char == "S" and parts[0][last_letter] == "E":
            del element_length[-1]
            element_length.append((last_letter + 2))
        if char != " ":
            last_letter = counter - 1
    element_length.append(len(parts[0]))
    del parts[0]
    for part in parts:
        values = list()
        for start, end in zip(element_length, element_length[1:]):
            values.append(part[start:(end-1)].strip())
        partdict.append(dict(zip(keys, values)))
    print(partdict)

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
        if newLine[5] != "5":  # Ungültige Partitionen herausfiltern
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
    # sudo lsblk -fs /dev/sda2 bessa
    # sudo lsblk -o NAME,FSTYPE,UUID,RM,SIZE,STATE,TYPE,MOUNTPOINT,LABEL,MODEL,ROTA auch gut
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
