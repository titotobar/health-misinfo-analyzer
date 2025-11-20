
# Class Design Document
Project 2 — Health Misinformation Analyzer  
INST326: Object-Oriented Programming

This document describes the object-oriented architecture used to implement the Health Misinformation Analyzer. The system converts the procedural functions from Project 1 into well-structured classes that encapsulate data and behaviors.

---

## System Overview

The system consists of the following core classes:

1. Article  
2. Glossary  
3. RiskScorer  
4. AnalysisReport  
5. Analyzer  

These classes work together to clean text, extract claims and citations, compare claims to medical terminology, score misinformation risk, and generate structured analysis reports.

---

## Class Descriptions

### 1. Article
**Purpose:**  
Represents a single article and handles all text processing tasks.

**Responsibilities:**
- Store and clean raw text
- Extract claims
- Extract citations (URLs and quotes)
- Identify the article’s domain
- Provide cleaned and processed data to other classes

**Key Attributes:**
- `_text`
- `_clean_text`
- `_claims`
- `_citations`
- `_domain`

**Collaborations:**  
Uses functions from `misinfo_library.py` for cleaning, claim extraction, citation extraction, and domain parsing.

---

### 2. Glossary
**Purpose:**  
Stores trusted medical terminology and checks article claims against expected phrasing.

**Responsibilities:**
- Add glossary entries
- Compare text to trusted phrases
- Return mismatches between the article and the glossary

**Key Attributes:**
- `_terms` (dictionary mapping keyword → set of expected phrases)

**Collaborations:**  
Used by `Analyzer` during article evaluation.

---

### 3. RiskScorer
**Purpose:**  
Calculates the misinformation risk score for a single article.

**Responsibilities:**
- Determine clickbait potential
- Count occurrences of absolute language
- Determine missing evidence (claims without citations)
- Count glossary mismatches
- Produce an overall risk score and risk level

**Key Attributes:**
- `_claims`
- `_citations`
- `_mismatches`
- `_score`

**Collaborations:**  
Called by `Analyzer` after glossary comparison.

---

### 4. AnalysisReport
**Purpose:**  
Stores and summarizes the results of a single article analysis.

**Responsibilities:**
- Store article, score, mismatches, and citations
- Build a claim-to-evidence mapping
- Produce a summary dictionary for external use

**Key Attributes:**
- `_article`
- `_score`
- `_mismatches`
- `_citations`
- `_evidence_map`

**Collaborations:**  
Outputs results used by the user or by `Analyzer`.

---

### 5. Analyzer
**Purpose:**  
Coordinates the entire end-to-end analysis pipeline and aggregates results across multiple articles.

**Responsibilities:**
- Run the full analysis process on an article
- Generate an AnalysisReport for each article
- Maintain a list of processed articles and corresponding reports
- Compute system-wide trends (e.g., average risk level)

**Key Attributes:**
- `_glossary`
- `_articles`
- `_reports`

**Collaborations:**  
Interacts with all other classes.

---

## Interaction Flow
