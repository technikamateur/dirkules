import dirkules.manager.driveManager as drive_man


def refresh_disks():
    drive_man.get_drives()
    print("Drives haha refreshed")
