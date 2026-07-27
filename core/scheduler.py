from datetime import datetime, timedelta
from core.database import Database

def calculate_next_retry(attempt):
    db = Database()

    base_delay = int(db.get_config("retry_delay", 5))

    db.close()

    delay = base_delay * (2 ** (attempt - 1))

    return datetime.now() + timedelta(seconds=delay)