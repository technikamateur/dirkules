# -*- coding: utf-8 -*-
import subprocess


# This file should read btrfs pools
# Storage: sudo btrfs fi usage -b -T /media/data-raid

def get_space(label):
    lines = list()
    btrfs_usage = subprocess.Popen(
        ["sudo btrfs fi usage -b -T " + label],
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
        ["sudo btrfs fi usage -T " + label],
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


def create_pool(label, drives, raid, mount_options):
    """
    Formats given drives and creates a pool
    :param label: Label for pool
    :type label: str
    :param drives: contains all drives, which should be added to the pool
    :type drives: list
    :param raid: RAID Level of pool
    :type raid: str
    :param mount_options: contains all mount options, which will be added to fstab
    :type mount_options: str
    :return:
    :rtype:
    """
    btrfs_partitions = ""
    for d in drives:
        drive_name = "/dev/" + d.name
        # stderr and stdout not captured
        subprocess.run(["sgdisk", "-Z", drive_name], shell=False, timeout=20, check=True)
        subprocess.run(["wipefs", "-a", drive_name], shell=False, timeout=20, check=True)
        subprocess.run(["sgdisk", "-o", drive_name], shell=False, timeout=20, check=True)
        subprocess.run(["sgdisk", "-N", "1", drive_name], shell=False, timeout=20, check=True)
        btrfs_partitions = btrfs_partitions + drive_name + "1" + " "
    btrfs_partitions = btrfs_partitions[:-1]
    subprocess.run(["mkfs.btrfs", "-f", "-L", label, "-d", raid, btrfs_partitions], shell=False, timeout=20, check=True)
    # add entry to fstab
