# -*- coding: utf-8 -*-
import subprocess


def get_all_drives():
    drives = []
    drive_dict = []
    keys = [
        'name', 'model', 'serial', 'size', 'rota', 'rm', 'hotplug', 'state',
        'smart'
    ]

    lsblk = subprocess.Popen(
        ["sudo lsblk -I 8 -d -b -o NAME,MODEL,SERIAL,SIZE,ROTA,RM,HOTPLUG"],
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
        new_line = ' '.join(line.split())
        new_line = new_line.split(" ")
        while len(new_line) > 7:
            new_line[1] = new_line[1] + " " + new_line[2]
            del new_line[2]
        values = []
        for i in range(len(keys) - 2):
            if new_line[i] == "0":
                values.append(False)
            elif new_line[i] == "1":
                values.append(True)
            else:
                values.append(new_line[i])
        values.append("running")
        values.append(get_smart("/dev/" + values[0]))
        drive_dict.append(dict(zip(keys, values)))
    sorted_drive_dict = sorted(drive_dict, key=lambda drive: drive['name'])
    return sorted_drive_dict


def get_smart(device):
    passed = False
    smartctl = subprocess.Popen(["sudo smartctl -H " + device],
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
    part_dict = list()
    keys = ['size', 'name', 'label', 'fs', 'uuid', 'mount']
    device = "/dev/" + device
    lsblk = subprocess.Popen(
        ["sudo lsblk " + device + " -l -b -o SIZE,NAME,LABEL,FSTYPE,UUID,MOUNTPOINT"],
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
    pre_value = " "
    for char in parts[0]:
        if char != " " and pre_value == " ":
            if len(element_length) == 0:
                element_length.append(0)
            else:
                element_length.append(counter)
        counter += 1
        pre_value = char
    element_length.append(len(parts[0]))
    del parts[0]
    for part in parts:
        values = list()
        for start, next_start in zip(element_length, element_length[1:]):
            if next_start == element_length[-1:][0]:
                values.append(part[start:len(part)].strip())
            else:
                values.append(part[start:(next_start - 1)].strip())
        part_dict.append(dict(zip(keys, values)))

    return part_dict
