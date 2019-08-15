from dirkules import scheduler
import datetime
import dirkules.manager.driveManager as drive_man

@scheduler.task('interval', id='refresh_disks', seconds=3600, next_run_time=datetime.datetime.now())
def refresh_disks():
    drive_man.get_drives()
    print("Drives refreshed")
