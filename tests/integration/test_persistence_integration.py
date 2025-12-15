import unittest
from pathlib import Path
from src.persistence import PersistenceManager


class TestPersistenceIntegration(unittest.TestCase):
    """Integration test: persistence + filesystem + data."""

    def setUp(self):
        self.file = Path("tests/integration/integration_test.json")
        self.data = {
            "article": "Integration test article",
            "risk_score": 0.8,
            "flags": ["clickbait"]
        }

    def tearDown(self):
        if self.file.exists():
            self.file.unlink()

    def test_save_and_load_integration(self):
        PersistenceManager.save_results(self.data, str(self.file))
        loaded = PersistenceManager.load_results(str(self.file))
        self.assertEqual(loaded, self.data)


if __name__ == "__main__":
    unittest.main()