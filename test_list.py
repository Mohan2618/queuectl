from core.database import Database

db = Database()

jobs = db.get_all_jobs()

print(f"Total Jobs: {len(jobs)}\n")

for job in jobs:
    print(dict(job))

db.close()