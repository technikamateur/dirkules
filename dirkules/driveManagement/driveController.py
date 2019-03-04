# -*- coding: utf-8 -*-
import psutil
import subprocess
import os


def getAllDrives():
    #vorbereitung
    drives = []
    driveDict = []
    keys = ['device', 'name', 'smart']

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
        driveDict.append(dict(zip(keys, values)))
    return driveDict


def smartPassed(device):
    passed = False
    smartctl = subprocess.Popen(
        ["smartctl -H " + device],
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
