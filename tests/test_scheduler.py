import unittest
from datetime import datetime

from core.scheduler import calculate_next_retry


class TestScheduler(unittest.TestCase):

    def test_retry_time_is_future(self):
        retry_time = calculate_next_retry(1)

        self.assertGreater(
            retry_time,
            datetime.now()
        )

    def test_second_retry_is_later(self):
        first = calculate_next_retry(1)
        second = calculate_next_retry(2)

        self.assertGreater(
            second,
            first
        )


if __name__ == "__main__":
    unittest.main()