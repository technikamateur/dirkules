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
    keys = ['total', 'free']
    values = [0, 0]
    for line in lines:
        newLine = ' '.join(line.split())
        newLine = newLine.split(" ")
        if newLine[0] == "Device" and newLine[1] == "size:":
            values[0] = int(newLine[2])
        elif newLine[0] == "Free":
            values[1] = int(newLine[2])
    memory_map = (dict(zip(keys, values)))
    return memory_map


def get_raid(label):
    lines = list()
    btrfs_usage = subprocess.Popen(
        ["btrfs fi usage -T " + label],
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
    keys = ['data_raid', 'data_ratio', 'meta_raid', 'meta_ratio']
    values = ['unbekannt', '1.00', 'unbekannt', '1.00']
    for line in lines:
        newLine = ' '.join(line.split())
        newLine = newLine.split(" ")
        if newLine[0] == "Data" and newLine[1] == "ratio:":
            values[1] = newLine[2]
        elif newLine[0] == "Metadata" and newLine[1] == "ratio:":
            values[3] = newLine[2]
        elif newLine[0] == "Id" and newLine[1] == "Path":
            values[0] = newLine[2]
            values[2] = newLine[3]
    raid_map = (dict(zip(keys, values)))
    return raid_map
