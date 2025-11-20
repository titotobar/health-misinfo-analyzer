from src.misinfo_library import (
    normalize_whitespace,
    extract_domain,
    find_claim_sentences,
    collect_citations,
)


class Article:
    """
    Represents a health-related news article.

    This class encapsulates the raw text, cleaned text, extracted claims,
    citations, and domain. It integrates multiple Project 1 functions to clean
    and analyze the article content.
    """

    def __init__(self, text: str):
        """
        Initialize an Article instance.

        Args:
            text (str): Raw article text.

        Raises:
            TypeError: If text is not a string.
            ValueError: If text is empty.
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        if not text.strip():
            raise ValueError("text cannot be empty")

        self._text = text
        self._clean_text = None
        self._domain = None
        self._claims = []
        self._citations = []

    # --------------------- Properties ---------------------

    @property
    def text(self) -> str:
        """Return the raw article text."""
        return self._text

    @property
    def clean_text(self) -> str:
        """Return the cleaned text."""
        return self._clean_text

    @property
    def claims(self) -> list:
        """Return extracted claim sentences."""
        return self._claims

    @property
    def citations(self) -> list:
        """Return extracted citations."""
        return self._citations

    @property
    def domain(self) -> str:
        """Return extracted domain name."""
        return self._domain

    # --------------------- Methods ---------------------

    def clean(self):
        """Clean the text using the Project 1 whitespace normalizer."""
        self._clean_text = normalize_whitespace(self._text)

    def extract_domain(self, url: str):
        """
        Extract and store the domain from a URL.

        Args:
            url (str): URL the article was retrieved from.
        """
        self._domain = extract_domain(url)

    def extract_claims(self, min_len: int = 40):
        """Extract claim sentences from cleaned text."""
        if self._clean_text is None:
            self.clean()
        self._claims = find_claim_sentences(self._clean_text, min_len=min_len)

    def extract_citations(self):
        """Extract URLs and quotes from the cleaned text."""
        if self._clean_text is None:
            self.clean()
        self._citations = collect_citations(self._clean_text)

    # --------------------- String Representations ---------------------

    def __str__(self) -> str:
        return f"Article(domain={self._domain}, claims={len(self._claims)})"

    def __repr__(self) -> str:
        return f"Article(text_len={len(self._text)})"