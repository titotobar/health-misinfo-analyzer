# src/__init__.py

# Import functions from misinfo_library
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

# Import class modules (these are separate files, not from misinfo_library!)
from .article import Article
from .glossary import Glossary
from .risk_scorer import RiskScorer
from .base_report import BaseReport
from .csv_report import CSVReport
from .json_report import JSONReport
from .html_report import HTMLReport
from .analyzer import Analyzer

__all__ = [
    # Functions from misinfo_library
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
    # Classes
    "Article",
    "Glossary",
    "RiskScorer",
    "BaseReport",
    "CSVReport",
    "JSONReport",
    "HTMLReport",
    "Analyzer",
]

__version__ = "0.1.0"