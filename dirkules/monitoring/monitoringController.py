# -*- coding: utf-8 -*-
import psutil

def getAllDrives():
    return psutil.disk_partitions()
