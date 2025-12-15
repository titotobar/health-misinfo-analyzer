import unittest
from pathlib import Path

from src.persistence import PersistenceManager


class TestMissingFile(unittest.TestCase):
    """System test for handling missing save files."""

    def test_missing_file_raises_error(self):
        missing_file = Path("tests/system/does_not_exist.json")

        with self.assertRaises(RuntimeError):
            PersistenceManager.load_results(str(missing_file))


if __name__ == "__main__":
    unittest.main()