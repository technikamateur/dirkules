# -*- coding: utf-8 -*-
import subprocess


def get_free_space(mount_point):
    lines = list()
    df = subprocess.Popen(
        ["df -B K " + mount_point],
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
        new_line = ' '.join(line.split())
        new_line = new_line.split(" ")
        if mount_point in new_line:
            return int(new_line[3][:-1]) * 1024
