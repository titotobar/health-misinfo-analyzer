"""
misinfo_library.py

Health News Misinformation Analyzer — Function Library (Project 1)

This module provides 15 PEP 8–compliant functions across simple, medium, and
complex levels for detecting potential misinformation signals in health news.
Every public function includes type hints, docstrings, input validation, and
meaningful errors.

Tiers:
- Simple (5): validation & cleaning helpers
- Medium (5): parsing & extraction
- Complex (5): analysis, scoring, reporting
"""
from __future__ import annotations

import csv
import re
import uuid
from datetime import datetime
from typing import Optional, Literal


# =========================== SIMPLE FUNCTIONS =========================== #


def normalize_whitespace(text: str) -> str:
    """Collapse multiple spaces and newlines into single spaces.

    Args:
        text: Input text to clean.

    Returns:
        Cleaned text with normalized spacing.

    Raises:
        TypeError: If `text` is not a string.

    Examples:
        >>> normalize_whitespace("  Health  tips\\n are   great!  ")
        'Health tips are great!'
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    # Remove BOM and non-breaking space; collapse whitespace
    cleaned = text.replace("\ufeff", "").replace("\xa0", " ")
    return " ".join(cleaned.split())


def validate_nonempty_str(value: str, name: str = "value") -> str:
    """Ensure a string is not empty or just whitespace.

    Args:
        value: The string to check.
        name: Variable name for clearer error messages.

    Returns:
        Trimmed version of the input string.

    Raises:
        TypeError: If `value` is not a string.
        ValueError: If `value` is empty.

    Examples:
        >>> validate_nonempty_str("Title")
        'Title'
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    trimmed = value.strip()
    if not trimmed:
        raise ValueError(f"{name} cannot be empty")
    return trimmed


def parse_iso_date_safe(date_str: Optional[str]) -> Optional[datetime]:
    """Parse ISO date safely or return None if empty or malformed.

    Args:
        date_str: Date string like '2025-10-10' or '2025-10-10T14:00:00'.

    Returns:
        Parsed datetime or None if empty/invalid.

    Raises:
        TypeError: If `date_str` is not a string or None.

    Examples:
        >>> parse_iso_date_safe("2025-10-10").date().isoformat()
        '2025-10-10'
    """
    if date_str is None:
        return None
    if not isinstance(date_str, str):
        raise TypeError("date_str must be a string or None")
    s = date_str.strip()
    if not s:
        return None
    try:
        # Try exact first; if only date, datetime.fromisoformat still works
        return datetime.fromisoformat(s if "T" in s else f"{s}T00:00:00")
    except ValueError:
        return None


def is_clickbait_phrase(text: str) -> bool:
    """Check if text includes typical clickbait terms.

    Args:
        text: Input phrase.

    Returns:
        True if clickbait detected, False otherwise.

    Raises:
        TypeError: If `text` is not a string.

    Examples:
        >>> is_clickbait_phrase("This miracle cure will blow your mind!")
        True
        >>> is_clickbait_phrase("Regular exercise supports better sleep.")
        False
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    clickbait_terms = {
        "miracle",
        "you won't believe",
        "cure-all",
        "secret revealed",
        "instantly",
        "breakthrough",
        "guaranteed",
        "shocking",
    }
    lower = text.lower()
    return any(term in lower for term in clickbait_terms)


def is_absolute_language(text: str) -> bool:
    """Detect absolute words like 'always', 'never', or 'guaranteed'.

    Args:
        text: Sentence to check.

    Returns:
        True if absolute wording is found.

    Raises:
        TypeError: If `text` is not a string.

    Examples:
        >>> is_absolute_language("Exercise always cures stress.")
        True
        >>> is_absolute_language("Exercise may help reduce stress.")
        False
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    absolute_terms = {
        "always",
        "never",
        "guaranteed",
        "proves",
        "prevents",
        "cures",
        "works for everyone",
        "zero risk",
    }
    t = text.lower()
    return any(word in t for word in absolute_terms)


# ============================ MEDIUM FUNCTIONS ========================== #


def extract_domain(url: str) -> str:
    """Extract domain name from a valid URL.

    Args:
        url: URL beginning with http(s):// or file://

    Returns:
        Domain name (e.g., 'example.com').

    Raises:
        TypeError: If `url` is not a string.
        ValueError: If the URL format is invalid.

    Examples:
        >>> extract_domain("https://www.healthline.com/nutrition")
        'www.healthline.com'
    """
    if not isinstance(url, str):
        raise TypeError("url must be a string")
    match = re.match(r"^(?:https?|file)://([^/]+)", url.strip(), flags=re.I)
    if not match:
        raise ValueError(f"Invalid URL: {url}")
    host = match.group(1).split("@")[-1].split(":")[0]
    return host.lower()


def extract_text_blocks(html_or_text: str) -> str:
    """Extract readable text from HTML or plain text.

    Removes <script>/<style> blocks and tags, then collapses whitespace.

    Args:
        html_or_text: Raw HTML or plain text.

    Returns:
        Cleaned readable text.

    Raises:
        TypeError: If `html_or_text` is not a string.

    Examples:
        >>> extract_text_blocks('<p>Health tips</p>')
        'Health tips'
    """
    if not isinstance(html_or_text, str):
        raise TypeError("html_or_text must be a string")
    raw = html_or_text
    if "<" not in raw:
        return normalize_whitespace(raw)
    # Super-lightweight HTML stripper (OK for Project 1)
    text = re.sub(r"(?is)<(script|style)[^>]*>.*?</\\1>", " ", raw)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return normalize_whitespace(text)


def find_claim_sentences(text: str, min_len: int = 40) -> list[dict]:
    """Find sentences that likely make health claims.

    Heuristic:
    - sentence length >= `min_len`
    - contains action words (cause/prevent/cure/…)
    - OR contains absolute language (always/never/guaranteed)

    Args:
        text: Full article text.
        min_len: Minimum character length per claim.

    Returns:
        List of dicts: {'id': str, 'text': str}

    Raises:
        TypeError: If inputs are wrong types.
        ValueError: If `min_len` < 1.

    Examples:
        >>> find_claim_sentences('Coffee cures headaches. It tastes good.', 20)[0]['text']
        'Coffee cures headaches.'
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(min_len, int):
        raise TypeError("min_len must be an int")
    if min_len < 1:
        raise ValueError("min_len must be >= 1")

    sentences = re.split(r"(?<=[.!?])\s+", text)
    keywords = {"cause", "prevent", "cure", "reduces", "reduce", "increase", "improves", "improve"}
    claims: list[dict] = []
    for s in sentences:
        clean = s.strip()
        if not clean:
            continue
        low = clean.lower()
        if len(clean) >= min_len and (any(k in low for k in keywords) or is_absolute_language(clean)):
            claims.append({"id": str(uuid.uuid4()), "text": clean})
    return claims


def collect_citations(text: str) -> list[str]:
    """Extract inline URLs or quoted evidence from text.

    Args:
        text: Text to search.

    Returns:
        List of URLs and quoted segments.

    Raises:
        TypeError: If `text` is not a string.

    Examples:
        >>> collect_citations('Study shows improvement (https://example.com)')
        ['https://example.com']
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    urls = re.findall(r"https?://[^\s)]+", text, flags=re.I)
    quotes = re.findall(r'"([^"]{3,})"', text)
    return urls + quotes


def compare_to_glossary(text: str, glossary: dict[str, set[str]]) -> list[tuple[str, str]]:
    """Compare text to glossary and flag mismatched phrasing.

    Very light MVP: If a term appears in the text but none of its allowed
    phrases are present, record a (term, 'mismatch') tuple.

    Args:
        text: Article text.
        glossary: e.g., {"flu": {"may reduce risk", "can help"}}

    Returns:
        List of (term, 'mismatch') pairs.

    Raises:
        TypeError: If inputs are wrong types.

    Examples:
        >>> compare_to_glossary('This prevents flu.', {'flu': {'may reduce risk'}})
        [('flu', 'mismatch')]
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(glossary, dict):
        raise TypeError("glossary must be a dict[str, set[str]]")

    lower = text.lower()
    mismatches: list[tuple[str, str]] = []
    for term, allowed in glossary.items():
        if not isinstance(allowed, set):
            raise TypeError("glossary values must be sets of strings")
        if term.lower() in lower:
            if not any(phrase.lower() in lower for phrase in allowed):
                mismatches.append((term, "mismatch"))
    return mismatches


# ============================ COMPLEX FUNCTIONS ========================= #


def score_article(
    text: str,
    claims: list[dict],
    citations: list[str],
    mismatches: list[tuple[str, str]],
) -> dict:
    """Compute a basic risk score for an article based on red flags.

    Components:
        - clickbait: 1 if article text looks clickbaity, else 0
        - absolute: count of claims with absolute language
        - no_evidence: number of claims when *no* citations exist for the article
        - mismatch: number of glossary mismatches
        - total: sum of components

    Args:
        text: Full article text.
        claims: Detected claim dicts.
        citations: Evidence links/quotes.
        mismatches: Glossary mismatches.

    Returns:
        Risk breakdown dict.

    Examples:
        >>> score_article('Coffee cures pain.', [{'id': '1', 'text': 'Coffee cures pain.'}], [], [])
        {'clickbait': 0, 'absolute': 0, 'no_evidence': 1, 'mismatch': 0, 'total': 1}
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(claims, list):
        raise TypeError("claims must be a list")
    if not isinstance(citations, list):
        raise TypeError("citations must be a list")
    if not isinstance(mismatches, list):
        raise TypeError("mismatches must be a list")

    clickbait = 1 if is_clickbait_phrase(text) else 0
    absolute = sum(1 for c in claims if isinstance(c, dict) and is_absolute_language(c.get("text", "")))
    no_evidence = len(claims) if not citations else 0
    mismatch = len(mismatches)

    total = clickbait + absolute + no_evidence + mismatch
    return {
        "clickbait": clickbait,
        "absolute": absolute,
        "no_evidence": no_evidence,
        "mismatch": mismatch,
        "total": total,
    }


def build_claim_evidence_map(claims: list[dict], citations: list[str]) -> dict[str, list[str]]:
    """Link each claim to a small set of likely-relevant evidence.

    MVP approach:
        - If any citation string shares a word with the beginning of the claim,
          attach it; else, attach the first citation if one exists.

    Args:
        claims: Detected claim dicts.
        citations: Extracted evidence strings (URLs or quotes).

    Returns:
        Map of claim_id -> list of evidence strings.

    Examples:
        >>> build_claim_evidence_map([{'id': '1', 'text': 'Coffee helps focus'}], ['https://ref'])
        {'1': ['https://ref']}
    """
    mapping: dict[str, list[str]] = {}
    for c in claims:
        cid = c.get("id", "")
        ctext = c.get("text", "")
        head = (ctext.split() or [""])[0].lower()
        related = [cite for cite in citations if head and head in cite.lower()]
        mapping[cid] = related if related else (citations[:1] if citations else [])
    return mapping


def export_flagged_claims(
    claims: list[dict],
    score: dict,
    output_path: str = "flagged_claims.csv",
) -> str:
    """Export claim information and a single article's score to CSV.

    Args:
        claims: List of claim dicts {'id', 'text'}.
        score: Risk score dictionary from `score_article`.
        output_path: Destination CSV path.

    Returns:
        The output file path.

    Raises:
        TypeError: If inputs have wrong types.
    """
    if not isinstance(claims, list):
        raise TypeError("claims must be a list")
    if not isinstance(score, dict):
        raise TypeError("score must be a dict")
    if not isinstance(output_path, str):
        raise TypeError("output_path must be a string")

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Claim ID", "Claim Text", "Total Risk Score"])
        for c in claims:
            writer.writerow([c.get("id", ""), c.get("text", ""), score.get("total", 0)])
    return output_path


def summarize_trends(reports: list[dict]) -> dict[str, float]:
    """Summarize average risk from multiple article reports.

    Args:
        reports: List of risk dictionaries from `score_article`.

    Returns:
        Dict with average risk score (0.0 if no reports).

    Examples:
        >>> summarize_trends([{'total': 3}, {'total': 5}])
        {'average_risk': 4.0}
    """
    if not reports:
        return {"average_risk": 0.0}
    total = sum(float(r.get("total", 0.0)) for r in reports)
    return {"average_risk": round(total / len(reports), 2)}


def cli_search_and_highlight(query: str, corpus: list[str]) -> list[str]:
    """Search articles by keyword and highlight matches with **bold**.

    Args:
        query: Search term (case-insensitive).
        corpus: A list of article texts.

    Returns:
        List of matched excerpts (full text with highlighted query).

    Raises:
        TypeError: If inputs are wrong types.

    Examples:
        >>> cli_search_and_highlight('vaccine', ['Vaccines save lives.'])[0]
        '**Vaccine**s save lives.'
    """
    if not isinstance(query, str):
        raise TypeError("query must be a string")
    if not isinstance(corpus, list):
        raise TypeError("corpus must be a list of strings")

    results: list[str] = []
    pattern = re.compile(f"({re.escape(query)})", flags=re.I)
    for text in corpus:
        if not isinstance(text, str):
            continue
        if pattern.search(text):
            results.append(pattern.sub(r"**\\1**", text))
    return results



# 2 - Re-export key functions so you can do: from src import find_claim_sentences, ...
from .misinfo_library import (
    normalize_whitespace,
    validate_nonempty_str,
    parse_iso_date_safe,
    is_clickbait_phrase,
    is_absolute_language,
    extract_domain,
    extract_text_blocks,
    find_claim_sentences,
    collect_citations,
    compare_to_glossary,
    score_article,
    build_claim_evidence_map,
    export_flagged_claims,
    summarize_trends,
    cli_search_and_highlight,
)

__all__ = [
    "normalize_whitespace",
    "validate_nonempty_str",
    "parse_iso_date_safe",
    "is_clickbait_phrase",
    "is_absolute_language",
    "extract_domain",
    "extract_text_blocks",
    "find_claim_sentences",
    "collect_citations",
    "compare_to_glossary",
    "score_article",
    "build_claim_evidence_map",
    "export_flagged_claims",
    "summarize_trends",
    "cli_search_and_highlight",
]

__version__ = "0.1.0"

