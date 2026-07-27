from core.database import Database


def recover_jobs():
    db = Database()

    recovered = db.recover_running_jobs()

    if recovered > 0:
        print(f"Recovered {recovered} job(s).")

    db.close()