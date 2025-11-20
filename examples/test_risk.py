from src.risk_scorer import RiskScorer

claims = [
    {"id": "1", "text": "Coffee cures headaches"}
]

citations = ["https://example.com"]
mismatches = [("headaches", "mismatch")]

scorer = RiskScorer(claims, citations, mismatches)
scorer.calculate()
scorer.build_evidence_map()

print("Score:", scorer.score)
print("Risk Level:", scorer.risk_level)
print("Evidence Map:", scorer.evidence_map)