from dirkules import scheduler

@scheduler.task('interval', id='do_job_1', seconds=300)
def job1():
    print("Job 1 executed")
