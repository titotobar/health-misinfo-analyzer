import unittest
from pathlib import Path

from src.persistence import PersistenceManager


class TestCorruptedFile(unittest.TestCase):
    """System test for handling corrupted JSON files."""

    def setUp(self):
        self.bad_file = Path("tests/system/bad.json")
        with self.bad_file.open("w", encoding="utf-8") as f:
            f.write("{ invalid json }")

    def tearDown(self):
        if self.bad_file.exists():
            self.bad_file.unlink()

    def test_corrupted_file_raises_error(self):
        with self.assertRaises(RuntimeError):
            PersistenceManager.load_results(str(self.bad_file))


if __name__ == "__main__":
    unittest.main()