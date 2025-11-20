from src.article import Article
from src.glossary import Glossary
from src.risk_scorer import RiskScorer
from src.analysis_report import AnalysisReport


class Analyzer:
    """
    High-level orchestrator that processes articles end to end.
    """

    def __init__(self):
        self._articles = []
        self._glossary = Glossary()
        self._reports = []

    # ---------------- Properties ----------------

    @property
    def glossary(self):
        return self._glossary

    @property
    def reports(self):
        return self._reports

    # ---------------- Methods ----------------

    def add_article(self, text: str, url: str = None):
        """
        Create an Article object, clean it, extract features, and store it.

        Args:
            text (str): Raw article text
            url (str): URL source for domain extraction
        """
        article = Article(text)
        article.clean()
        article.extract_claims(min_len=10)
        article.extract_citations()

        if url:
            article.extract_domain(url)

        self._articles.append(article)
        return article

    def analyze_article(self, article: Article):
        """
        Run glossary comparison, scoring, and report generation.

        Returns:
            AnalysisReport
        """
        mismatches = self._glossary.compare(article.clean_text)
        scorer = RiskScorer(article.claims, article.citations, mismatches)
        scorer.calculate()

        report = AnalysisReport(
            article,
            scorer.score,
            mismatches,
            article.citations
        )

        self._reports.append(report)
        return report

    def summarize_trends(self):
        """
        Compute average risk across all processed articles.
        """
        if not self._reports:
            return {"average_risk": 0.0}

        total = sum(r.score.get("total", 0) for r in self._reports)
        return {"average_risk": total / len(self._reports)}

    def __str__(self):
        return f"Analyzer(articles={len(self._articles)}, reports={len(self._reports)})"

    def __repr__(self):
        return f"Analyzer({len(self._articles)} articles processed)"