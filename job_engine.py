import time
from sql import insert_resource, query_db, exec_db, update_resource
from datetime import datetime, timedelta
from multiprocessing.dummy import Pool as ThreadPool
from threading import Thread
from app_jobs import global_jobs, test_job_1, test_job_2, test_job_3, sync_messages_json

allowed_jobs_map = {'test_job_1': test_job_1,
                    'test_job_2': test_job_2,
                    'test_job_3': test_job_3,
                    'sync_messages_json': sync_messages_json}


class Timer:
    job_sleep_time = 10

    @classmethod
    def now(cls):
        return datetime.now()

    @classmethod
    def next_start(cls, job_record: dict) -> datetime:
        delta = job_record['resource']['period']
        next_date = cls.now() + timedelta(minutes=delta)
        return next_date

    @classmethod
    def should_start(cls, date1: datetime, date2) -> bool:
        if date2 is None:
            return False
        else:
            return date1.isoformat() > date2


class JobEngine:
    job_pool = ThreadPool(4)
    pool = ThreadPool(2)

    @classmethod
    def run_job(cls, job_record: dict) -> dict:
        job_resource = job_record['resource']
        job_id = job_record['id']
        job_name = job_resource['name']
        function_to_run = allowed_jobs_map[job_name]
        # print("Running job: ", job_id, job_name, "++++++", "Locked job", locked_job, sep="\n")
        try:
            job_next_start = job_resource.get('next_start')
            if job_next_start is None:
                job_resource['next_start'] = Timer.next_start(job_record)
                result = update_resource('Job', job_id, job_resource)[0][0]
                return result

            elif Timer.should_start(Timer.now(), job_next_start):
                job_resource['locked'] = 'true'
                updated_job = update_resource('Job', job_id, job_resource)[0][0]
                function_to_run()
                following_start = Timer.next_start(job_record)
                updated_job['locked'] = 'false'
                updated_job['next_start'] = following_start
                result = update_resource('job', job_id, updated_job)
                print("Job resource: ", result)
                return result
            else:
                print('Should not run jobs')
                return job_record
        except Exception as e:
            print("Could not run job: ", e)
            return {'errors': "errors"}

    @classmethod
    def run_jobs(cls, job_resources: list) -> list:
        results = cls.job_pool.map(cls.run_job, job_resources)
        return results


def save_jobs(jobs):
    for job in jobs:
        insert_resource("Job", job)


def select_active_jobs():
    return query_db("select * from Job"
                    " where resource#>>'{status}' = 'active'"
                    " and resource#>>'{locked}' = 'false'")


def start_jobs():
    while True:
        jobs_to_run = select_active_jobs()
        print(query_db("select * from job;"))
        print("Active jobs", len(jobs_to_run), datetime.now())
        job_records = [job for job in jobs_to_run]
        JobEngine.run_jobs(job_records)
        time.sleep(Timer.job_sleep_time)


def start_jobs_wrapper():
    print("Started jobs")
    thread = Thread(target=start_jobs)
    thread.start()
    print("Jobs Engine was started")


exec_db("delete from job;")
save_jobs(global_jobs)
start_jobs_wrapper()
print("JOBS WRAPPER OK")
print(query_db("select version();"))