from core.database import Database


def list_jobs(state=None):
    db = Database()

    jobs = db.get_jobs_by_state(state)

    if not jobs:
        print("No jobs found.")
        db.close()
        return

    print("-" * 80)
    print(f"{'ID':<15}{'STATE':<15}{'ATTEMPTS':<10}COMMAND")
    print("-" * 80)

    for job in jobs:
        print(
            f"{job['id']:<15}"
            f"{job['state']:<15}"
            f"{job['attempts']:<10}"
            f"{job['command']}"
        )

    db.close()