"""
base_report.py

Abstract base class for all report types in the health misinformation analyzer.
"""
from abc import ABC, abstractmethod
from src.misinfo_library import build_claim_evidence_map


class BaseReport(ABC):
    """
    Abstract base class for analysis reports.
    
    All report subclasses must implement export() and can override summary()
    to provide format-specific summaries.
    """
    
    def __init__(self, article, score: dict, mismatches: list, citations: list):
        """
        Initialize a BaseReport.
        
        Args:
            article (Article): article object that was analyzed
            score (dict): risk score dictionary
            mismatches (list): glossary mismatches
            citations (list): extracted citations
        """
        if not isinstance(score, dict):
            raise TypeError("score must be a dictionary")
        if not isinstance(mismatches, list):
            raise TypeError("mismatches must be a list")
        if not isinstance(citations, list):
            raise TypeError("citations must be a list")
            
        self._article = article
        self._score = score
        self._mismatches = mismatches
        self._citations = citations
        
        # Build evidence map (shared across all report types)
        self._evidence_map = build_claim_evidence_map(
            article.claims,
            citations
        )
    
    # --------- Properties (shared by all reports) ---------
    
    @property
    def score(self):
        """Return the risk score dictionary."""
        return self._score
    
    @property
    def mismatches(self):
        """Return glossary mismatches."""
        return self._mismatches
    
    @property
    def citations(self):
        """Return extracted citations."""
        return self._citations
    
    @property
    def evidence_map(self):
        """Return claim-to-evidence mapping."""
        return self._evidence_map
    
    # --------- Abstract Methods (must be implemented by subclasses) ---------
    
    @abstractmethod
    def export(self, path: str) -> str:
        """
        Export the report to a file.
        
        Args:
            path (str): Output file path
            
        Returns:
            str: Path to the exported file
        """
        pass
    
    # --------- Concrete Methods (can be overridden) ---------
    
    def summary(self):
        """
        Return a short human-friendly summary of the analysis.
        
        Subclasses can override to provide format-specific summaries.
        """
        return {
            "domain": self._article.domain,
            "claims_found": len(self._article.claims),
            "citations_found": len(self._citations),
            "mismatches": len(self._mismatches),
            "risk_total": self._score.get("total", 0)
        }
    
    def get_risk_level(self) -> str:
        """
        Classify risk level based on total score.
        
        Returns:
            str: "Low", "Medium", or "High"
        """
        total = self._score.get("total", 0)
        if total < 1:
            return "Low"
        elif total < 3:
            return "Medium"
        return "High"
    
    # --------- String Representations ---------
    
    def __str__(self):
        return f"{self.__class__.__name__}(score={self._score.get('total', 0)})"
    
    def __repr__(self):
        return f"{self.__class__.__name__}(article={self._article}, score={self._score})"
