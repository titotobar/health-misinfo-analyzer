import unittest
from pathlib import Path

from src.persistence import PersistenceManager


class TestFullWorkflow(unittest.TestCase):
    """System-level test for full analysis save/load workflow."""

    def setUp(self):
        self.test_file = Path("tests/system/test_output.json")
        self.sample_results = {
            "article": "Test article text",
            "risk_score": 0.75,
            "flags": ["absolute_language", "missing_citation"]
        }

    def tearDown(self):
        if self.test_file.exists():
            self.test_file.unlink()

    def test_save_and_load_results(self):
        # Save results
        PersistenceManager.save_results(self.sample_results, self.test_file)

        # Load results
        loaded = PersistenceManager.load_results(self.test_file)

        # Verify integrity
        self.assertEqual(loaded, self.sample_results)


if __name__ == "__main__":
    unittest.main()