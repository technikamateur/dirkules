# -*- coding: utf-8 -*-
import subprocess


# This file should read btrfs pools
# Storage: sudo btrfs fi usage -b -T /media/data-raid

def get_free_space(name):
    lines = list()
    df = subprocess.Popen(
        ["df -B K " + name],
        stdout=subprocess.PIPE,
        shell=True,
        universal_newlines=True)
    while True:
        line = df.stdout.readline()
        if line != '':
            lines.append(line.rstrip())
        else:
            break
    df.stdout.close()
    for line in lines:
        newLine = ' '.join(line.split())
        newLine = newLine.split(" ")
        if name in newLine[0]:
            return int(newLine[3][:-1]) * 1024
