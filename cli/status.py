from core.database import Database


def status(job_id):
    db = Database()

    job = db.get_job(job_id)

    if job is None:
        print("Job not found.")
        db.close()
        return

    print("=" * 50)
    print(f"Job ID     : {job['id']}")
    print(f"State      : {job['state']}")
    print(f"Attempts   : {job['attempts']}")
    print(f"Exit Code  : {job['exit_code']}")
    print()

    print("Command")
    print("-" * 20)
    print(job["command"])
    print()

    print("STDOUT")
    print("-" * 20)
    print(job["stdout"] if job["stdout"] else "(empty)")
    print()

    print("STDERR")
    print("-" * 20)
    print(job["stderr"] if job["stderr"] else "(empty)")
    print("=" * 50)

    db.close()