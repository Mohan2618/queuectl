from datetime import datetime, timedelta
from core.database import Database

db = Database()

retry_time = datetime.now() + timedelta(seconds=30)

db.schedule_retry("retry_test", retry_time)

job = db.get_job("retry_test")

print(dict(job))

db.close()