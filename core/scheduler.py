from datetime import datetime, timedelta


def calculate_next_retry(attempt):
    """
    Exponential backoff:
    attempt 1 -> 5 seconds
    attempt 2 -> 10 seconds
    attempt 3 -> 20 seconds
    attempt 4 -> 40 seconds
    """

    delay = 5 * (2 ** (attempt - 1))

    return datetime.now() + timedelta(seconds=delay)