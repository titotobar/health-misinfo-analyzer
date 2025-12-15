import unittest
from pathlib import Path
from src.persistence import PersistenceManager


class TestNestedData(unittest.TestCase):

    def setUp(self):
        self.file = Path("tests/integration/nested.json")
        self.data = {
            "articles": [
                {"id": 1, "risk": 0.2},
                {"id": 2, "risk": 0.9}
            ],
            "summary": {"average": 0.55}
        }

    def tearDown(self):
        if self.file.exists():
            self.file.unlink()

    def test_nested_data_persists_correctly(self):
        PersistenceManager.save_results(self.data, str(self.file))
        loaded = PersistenceManager.load_results(str(self.file))
        self.assertEqual(loaded, self.data)


if __name__ == "__main__":
    unittest.main()