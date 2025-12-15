import unittest
from pathlib import Path
from src.persistence import PersistenceManager


class TestLoadType(unittest.TestCase):

    def setUp(self):
        self.file = Path("tests/integration/type.json")
        PersistenceManager.save_results({"a": 1}, str(self.file))

    def tearDown(self):
        if self.file.exists():
            self.file.unlink()

    def test_load_returns_dict(self):
        loaded = PersistenceManager.load_results(str(self.file))
        self.assertIsInstance(loaded, dict)


if __name__ == "__main__":
    unittest.main()