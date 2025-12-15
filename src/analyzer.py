"""
analyzer.py

High-level orchestrator with pluggable report formats.
"""
from src.article import Article
from src.glossary import Glossary
from src.risk_scorer import RiskScorer
from src.csv_report import CSVReport  # FIXED: Was csv_report_final


class Analyzer:
    """
    High-level orchestrator that processes articles end to end.
    
    Now supports multiple report formats through dependency injection.
    """
    
    def __init__(self, report_class=CSVReport):
        """
        Initialize analyzer with configurable report format.
        
        Args:
            report_class: Report class to use (CSVReport, JSONReport, HTMLReport)
                         Defaults to CSVReport for backward compatibility
        """
        self._articles = []
        self._glossary = Glossary()
        self._reports = []
        self._report_class = report_class
    
    # ---------------- Properties ----------------
    
    @property
    def glossary(self):
        return self._glossary
    
    @property
    def reports(self):
        return self._reports
    
    # ---------------- Configuration Methods ----------------
    
    def set_report_format(self, report_class):
        """
        Change the report format at runtime.
        
        Args:
            report_class: New report class (CSVReport, JSONReport, HTMLReport)
            
        Example:
            analyzer.set_report_format(JSONReport)
        """
        self._report_class = report_class
    
    # ---------------- Article Processing Methods ----------------
    
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
        
        Uses the configured report_class to generate the report.
        
        Returns:
            BaseReport subclass instance (CSVReport, JSONReport, or HTMLReport)
        """
        mismatches = self._glossary.compare(article.clean_text)
        scorer = RiskScorer(article.claims, article.citations, mismatches)
        scorer.calculate()
        
        # Use the injected report class (polymorphism!)
        report = self._report_class(
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
    
    # ---------------- String Representations ----------------
    
    def __str__(self):
        return f"Analyzer(articles={len(self._articles)}, reports={len(self._reports)}, format={self._report_class.__name__})"
    
    def __repr__(self):
        return f"Analyzer({len(self._articles)} articles processed, using {self._report_class.__name__})"