# -*- coding: utf-8 -*-
import subprocess


# This file should read btrfs pools
# Storage: sudo btrfs fi usage -b -T /media/data-raid

def get_space(label):
    lines = list()
    btrfs_usage = subprocess.Popen(
        ["btrfs fi usage -b -T " + label],
        stdout=subprocess.PIPE,
        shell=True,
        universal_newlines=True)
    while True:
        line = btrfs_usage.stdout.readline()
        if line != '':
            lines.append(line.rstrip())
        else:
            break
    btrfs_usage.stdout.close()
    keys = ['total', 'usable', 'free']
    values = [0, 0, 0]
    for line in lines:
        newLine = ' '.join(line.split())
        newLine = newLine.split(" ")
        if newLine[0] == "Device" and newLine[1] == "size:":
            values[0] = int(newLine[2])
        elif newLine[0] == "Free":
            values[2] = int(newLine[2])
        elif newLine[0] == "Data" and newLine[1] == "ratio:":
            values[1] = int(values[0]/float(newLine[2]))
    memory_map = (dict(zip(keys, values)))
    return memory_map
