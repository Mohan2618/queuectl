import time

from core.database import Database
from core.executor import execute
from core.scheduler import calculate_next_retry
from core.recovery import recover_jobs


def worker_once(worker_id):
    # 👇 Everything that is currently inside your worker()
    db = Database()

    job = db.get_next_pending_job()

    if job is None:
        db.close()
        return

    print(
        f"[{worker_id}] Executing {job['id']}..."
    )

    claimed = db.claim_job(
        job["id"],
        worker_id
    )

    if not claimed:
        db.close()
        return False

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
        db.increment_attempt(job["id"])

        attempts = job["attempts"] + 1

        if attempts < job["max_retries"]:

            retry_time = calculate_next_retry(attempts)

            db.schedule_retry(
                job["id"],
                retry_time
            )

            print(
                f"Retry scheduled at "
                f"{retry_time.strftime('%Y-%m-%d %H:%M:%S')}"
            )

        else:
            db.move_to_dead_letter(
                db.get_job(job["id"])
            )
            print("Moved to Dead Letter Queue.")

    db.close()


def run_worker(worker_id):
    print("Worker started.")

    

    waiting = False

    try:
        while True:

            processed = worker_once(worker_id)

            if processed:
                waiting = False
            else:
                if not waiting:
                    print("Waiting for jobs...")
                    waiting = True

            time.sleep(2)

    except KeyboardInterrupt:
        print("\nWorker stopped.")