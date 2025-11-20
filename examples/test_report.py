from src.article import Article
from src.glossary import Glossary
from src.risk_scorer import RiskScorer
from src.analysis_report import AnalysisReport

# Simple test article
text = "Coffee cures headaches. More info: https://example.com"
article = Article(text)
article.clean()
article.extract_claims(min_len=10)
article.extract_citations()
article.extract_domain("https://cnn.com/health")

# Glossary mismatch
g = Glossary()
g.add_term("headaches", ["may reduce risk"])

mismatches = g.compare(article.clean_text)

# Score
scorer = RiskScorer(article.claims, article.citations, mismatches)
scorer.calculate()

# Build report
report = AnalysisReport(
    article,
    scorer.score,
    mismatches,
    article.citations
)

print("Summary:", report.summary())
print("Evidence Map:", report.evidence_map)