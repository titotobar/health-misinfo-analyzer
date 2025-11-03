from datetime import datetime
from misinfo_library import parse_iso_date_safe, validate_nonempty_str

class Article:
    """
    Represents a health-related news article.

    Attributes:
        title (str): The article title.
        text (str): Full body text.
        source_url (str | None): Original URL (optional).
        published (datetime | None): Publication date.

    Example:
        >>> a = Article("Coffee cures stress", "Coffee can reduce stress.", "https://news.com")
        >>> str(a)
        'Article(title=Coffee cures stress, domain=news.com)'
    """

    def __init__(self, title: str, text: str, source_url: str | None = None, published: str | None = None):
        self._title = validate_nonempty_str(title, "title")
        self._text = validate_nonempty_str(text, "text")
        self._source_url = source_url
        self._published = parse_iso_date_safe(published)

    @property
    def title(self): return self._title

    @property
    def text(self): return self._text

    @property
    def source_url(self): return self._source_url

    @property
    def published(self): return self._published

    def __str__(self):
        from misinfo_library import extract_domain
        domain = extract_domain(self._source_url) if self._source_url else "N/A"
        return f"Article(title={self._title}, domain={domain})"

    def __repr__(self):
        return f"Article(len={len(self._text)}, url={bool(self._source_url)})"
