from core.database import Database
from core.models import Job


def enqueue(job_id, command):
    job = Job(
        id=job_id,
        command=command
    )

    db = Database()

    try:
        db.insert_job(job)
        print(f"Job '{job.id}' enqueued successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()