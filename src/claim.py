class Claim:
    """
    Represents a single health-related claim extracted from an article.

    Attributes:
        id (str): Unique claim identifier.
        text (str): Claim sentence.
        evidence (list[str]): Supporting citations or quotes.
    """

    def __init__(self, claim_id: str, text: str, evidence: list[str] | None = None):
        from misinfo_library import validate_nonempty_str
        self._id = validate_nonempty_str(claim_id, "claim_id")
        self._text = validate_nonempty_str(text, "text")
        self._evidence = evidence or []

    @property
    def id(self): return self._id

    @property
    def text(self): return self._text

    @property
    def evidence(self): return list(self._evidence)

    def add_evidence(self, citation: str):
        """Attach an additional citation string."""
        if isinstance(citation, str):
            self._evidence.append(citation)

    def __str__(self):
        return f"Claim(id={self._id[:8]}, text={self._text[:40]}...)"

    def __repr__(self):
        return f"Claim(id={self._id}, evidence={len(self._evidence)})"
