import unittest

from core.executor import execute


class TestExecutor(unittest.TestCase):

    def test_successful_command(self):
        result = execute("echo Hello")

        self.assertTrue(result["success"])
        self.assertEqual(result["exit_code"], 0)

    def test_failed_command(self):
        result = execute(
            "python file_that_does_not_exist.py"
        )

        self.assertFalse(result["success"])
        self.assertNotEqual(
            result["exit_code"],
            0
        )


if __name__ == "__main__":
    unittest.main()