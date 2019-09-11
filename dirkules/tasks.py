import dirkules.manager.driveManager as drive_man
import dirkules.manager.cleaning as clean_man


def refresh_disks():
    drive_man.get_drives()
    drive_man.get_partitions()
    drive_man.pool_gen()


def cleaning():
    clean_man.clean_folders()
