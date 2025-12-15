import unittest
from pathlib import Path
from src.persistence import PersistenceManager


class TestFileCreation(unittest.TestCase):

    def setUp(self):
        self.file = Path("tests/integration/created.json")

    def tearDown(self):
        if self.file.exists():
            self.file.unlink()

    def test_file_is_created_on_save(self):
        PersistenceManager.save_results({"status": "ok"}, str(self.file))
        self.assertTrue(self.file.exists())


if __name__ == "__main__":
    unittest.main()