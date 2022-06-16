from app_jobs import *
from sql import insert_resource, query_db, exec_db


def save_jobs(jobs):
    for job in jobs:
        insert_resource("Job", job)


def select_active_jobs():
    return query_db("select * from Job")


def run_jobs(jobs):
    job_resources = [job['resource'] for job in jobs]
    return job_resources


def start_jobs():
    jobs_to_run = select_active_jobs()
    return run_jobs(jobs_to_run)


# exec_db("delete from job;")
# save_jobs(global_jobs)
print(start_jobs())


