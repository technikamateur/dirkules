from dirkules import scheduler
import datetime
import dirkules.hardware.drive as drico

@scheduler.task('interval', id='refresh_disks', seconds=3600, next_run_time=datetime.datetime.now())
def refresh_disks():
    drives = drico.getAllDrives()
    print("Drives refreshed")
