from core.database import Database
from core.executor import execute


def worker():
    db = Database()

    job = db.get_next_pending_job()

    if job is None:
        print("No pending jobs.")
        db.close()
        return

    print(f"Executing {job['id']}...")

    db.update_job_state(job["id"], "running")

    result = execute(job["command"])

    db.update_job_result(
        job["id"],
        result["stdout"],
        result["stderr"],
        result["exit_code"]
    )

    if result["success"]:
        db.update_job_state(job["id"], "completed")
        print("Completed.")
    else:
        db.update_job_state(job["id"], "failed")
        print("Failed.")

    db.close()