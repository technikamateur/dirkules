import dirkules.manager.driveManager as drive_man


def refresh_disks():
    drive_man.get_drives()
    drive_man.get_partitions()
    drive_man.pool_gen()
