# src/__init__.py
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
