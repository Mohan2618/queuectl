from core.database import Database
from core.executor import execute
from core.scheduler import calculate_next_retry


def worker():
    db = Database()

    # Get the next pending job
    job = db.get_next_pending_job()

    if job is None:
        print("No pending jobs.")
        db.close()
        return

    print(f"Executing {job['id']}...")

    # Mark job as running
    db.update_job_state(job["id"], "running")

    # Execute the command
    result = execute(job["command"])

    # Save execution results
    db.update_job_result(
        job["id"],
        result["stdout"],
        result["stderr"],
        result["exit_code"]
    )

    # Handle success
    if result["success"]:
        db.update_job_state(job["id"], "completed")
        print("Completed.")

    # Handle failure
    else:
        # Increment attempt count
        db.increment_attempt(job["id"])

        attempts = job["attempts"] + 1

        # Retry if attempts remain
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

        # No retries left
        else:
            db.move_to_dead_letter(
                db.get_job(job["id"])
            )

            print("Moved to Dead Letter Queue.")

    db.close()