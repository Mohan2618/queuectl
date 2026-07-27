import unittest
import uuid

from core.database import Database
from core.models import Job


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = Database()

    def tearDown(self):
        self.db.close()

    def test_insert_job(self):
        job = Job(
            id=str(uuid.uuid4()),
            command="echo Test"
        )

        self.db.insert_job(job)

        saved = self.db.get_job(job.id)

        self.assertIsNotNone(saved)
        self.assertEqual(saved["id"], job.id)

    def test_update_state(self):
        job = Job(
            id=str(uuid.uuid4()),
            command="echo Test"
        )

        self.db.insert_job(job)

        self.db.update_job_state(
            job.id,
            "completed"
        )

        saved = self.db.get_job(job.id)

        self.assertEqual(
            saved["state"],
            "completed"
        )


if __name__ == "__main__":
    unittest.main()