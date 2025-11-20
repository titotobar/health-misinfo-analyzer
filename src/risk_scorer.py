from src.misinfo_library import score_article, build_claim_evidence_map


class RiskScorer:
    """
    Scores misinformation risk based on claims, citations, and glossary mismatches.
    """

    def __init__(self, claims: list, citations: list, mismatches: list):
        if not isinstance(claims, list):
            raise TypeError("claims must be a list")
        if not isinstance(citations, list):
            raise TypeError("citations must be a list")
        if not isinstance(mismatches, list):
            raise TypeError("mismatches must be a list")

        self._claims = claims
        self._citations = citations
        self._mismatches = mismatches

        self._score = None
        self._evidence_map = None

    # ---------------- Properties ----------------

    @property
    def score(self):
        return self._score

    @property
    def evidence_map(self):
        return self._evidence_map

    @property
    def risk_level(self) -> str:
        if self._score is None:
            return "Not calculated"

        total = self._score.get("total", 0)

        if total < 1:
            return "Low"
        elif total < 3:
            return "Medium"
        return "High"

    # ---------------- Methods ----------------

    def calculate(self):
        """
        Calculate risk score using Project 1 score_article().
        MATCHES YOUR FUNCTION SIGNATURE EXACTLY.
        """
        self._score = score_article(
            text="",                    # your function requires this
            claims=self._claims,
            citations=self._citations,
            mismatches=self._mismatches
        )

    def build_evidence_map(self):
        """
        Build claim → evidence mapping.
        """
        self._evidence_map = build_claim_evidence_map(
            self._claims,
            self._citations
        )

    # ---------------- String Methods ----------------

    def __str__(self):
        return f"RiskScorer(score={self._score}, level={self.risk_level})"

    def __repr__(self):
        return f"RiskScorer(claims={len(self._claims)}, citations={len(self._citations)})"