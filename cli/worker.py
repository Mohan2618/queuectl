import time

from core.database import Database
from core.executor import execute
from core.scheduler import calculate_next_retry
from core.recovery import recover_jobs
from core.logger import logger


def worker_once(worker_id):
    db = Database()

    # Get next pending job
    job = db.get_next_pending_job()

    if job is None:
        db.close()
        return False

    # Try to claim the job
    claimed = db.claim_job(
        job["id"],
        worker_id
    )

    if not claimed:
        db.close()
        return False

    # Log execution
    message = f"[{worker_id}] Executing {job['id']}..."

    print(message)
    logger.info(message)

    # Execute command
    result = execute(job["command"])

    # Save stdout/stderr/exit code
    db.update_job_result(
        job["id"],
        result["stdout"],
        result["stderr"],
        result["exit_code"]
    )

    # Success
    if result["success"]:

        db.update_job_state(
            job["id"],
            "completed"
        )

        print("Completed.")

        logger.info(
            f"Job {job['id']} completed successfully"
        )

    # Failure
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

            logger.warning(
                f"Job {job['id']} retry scheduled at "
                f"{retry_time.strftime('%Y-%m-%d %H:%M:%S')}"
            )

        else:

            db.move_to_dead_letter(
                db.get_job(job["id"])
            )

            print("Moved to Dead Letter Queue.")

            logger.error(
                f"Job {job['id']} moved to Dead Letter Queue"
            )

    db.close()

    return True


def run_worker(worker_id):

    print("Worker started.")
    logger.info(f"Worker {worker_id} started")

    # Recover unfinished jobs
    recover_jobs()

    # Read poll interval once
    db = Database()

    poll_interval = int(
        db.get_config(
            "poll_interval",
            2
        )
    )

    db.close()

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

            time.sleep(poll_interval)

    except KeyboardInterrupt:

        print("\nWorker stopped.")

        logger.info(
            f"Worker {worker_id} stopped"
        )