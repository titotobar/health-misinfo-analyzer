from src.misinfo_library import export_flagged_claims, build_claim_evidence_map


class AnalysisReport:
    """
    Stores and exports the results of analyzing one health article.
    """

    def __init__(self, article, score: dict, mismatches: list, citations: list):
        """
        Initialize an AnalysisReport.

        Args:
            article (Article): article object that was analyzed
            score (dict): risk score dictionary
            mismatches (list): glossary mismatches
            citations (list): extracted citations
        """

        self._article = article
        self._score = score
        self._mismatches = mismatches
        self._citations = citations

        # Build evidence map
        self._evidence_map = build_claim_evidence_map(
            article.claims,
            citations
        )

    # --------- Properties ---------

    @property
    def score(self):
        return self._score

    @property
    def mismatches(self):
        return self._mismatches

    @property
    def citations(self):
        return self._citations

    @property
    def evidence_map(self):
        return self._evidence_map

    # --------- Methods ---------

    def export_csv(self, path="report_output.csv"):
        """
        Export all flagged claims and risk scores to CSV using Project 1 function.
        """
        return export_flagged_claims(
            self._article.claims,
            self._score,
            output_path=path
        )

    def summary(self):
        """
        Return a short human-friendly summary of the analysis.
        """
        return {
            "domain": self._article.domain,
            "claims_found": len(self._article.claims),
            "citations_found": len(self._citations),
            "mismatches": len(self._mismatches),
            "risk_total": self._score.get("total", 0)
        }

    def __str__(self):
        return f"AnalysisReport(score={self._score.get('total', 0)})"

    def __repr__(self):
        return f"AnalysisReport(article={self._article}, score={self._score})"