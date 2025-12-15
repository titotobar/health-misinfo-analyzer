import unittest
from pathlib import Path
from src.persistence import PersistenceManager


class TestMultipleKeys(unittest.TestCase):

    def setUp(self):
        self.file = Path("tests/integration/multi_keys.json")
        self.data = {
            "article": "Test",
            "risk": 0.7,
            "flags": ["clickbait", "missing_citation"]
        }

    def tearDown(self):
        if self.file.exists():
            self.file.unlink()

    def test_all_keys_preserved(self):
        PersistenceManager.save_results(self.data, str(self.file))
        loaded = PersistenceManager.load_results(str(self.file))
        self.assertEqual(set(loaded.keys()), set(self.data.keys()))


if __name__ == "__main__":
    unittest.main()