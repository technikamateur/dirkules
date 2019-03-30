from dirkules import scheduler
import datetime

@scheduler.task('interval', id='do_job_1', seconds=20, next_run_time=datetime.datetime.now())
def job1():
    print("Job 1 executed")
