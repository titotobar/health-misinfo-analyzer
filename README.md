# Health Misinformation Analyzer – Project 4

This project transforms our Project 1 function library into a fully object-oriented system designed to analyze health-related articles for misinformation.  
Our system uses multiple interacting classes to detect claims, compare them to a trusted glossary, score misinformation risk, and generate analysis reports.


### Team Members
- Donald, Jacob, Kabir, Free


### Project Overview
Health misinformation spreads quickly online, especially in news articles and social media posts.  
Our goal is to build an automated system that:

- Cleans and processes article text  
- Extracts claims and citations  
- Compares claims to trusted medical phrasing  
- Scores risk and flags misinformation  
- Generates reports and trends across articles  

This project converts the Project 1 function library into "5 fully functional classes":

- Article – cleans text, extracts claims & citations, detects domain  
- Glossary – stores trusted medical terms and finds mismatches  
- RiskScorer – scores articles based on clickbait, absolute language, missing evidence, and mismatches  
- AnalysisReport – produces structured summaries for each article  
- Analyzer – runs multiple articles and generates overall trends  

# System Architecture

### Inheritance Hierarchies
```
BaseReport (Abstract Base Class)
├── CSVReport (comma-separated values, Excel-compatible)
├── JSONReport (structured data with metadata, machine-readable)
└── HTMLReport (styled browser-viewable reports with color-coding)
```
### Composition Relationships

```
Analyzer (Orchestrator)
├── HAS-A Glossary (1 instance, shared across all articles)
├── HAS-MANY Article objects (list of articles)
├── HAS-MANY BaseReport objects (list of reports)
└── USES-A report_class (injected dependency for creating reports)

Article (Data Container)
├── HAS-A text (raw string)
├── HAS-A clean_text (processed string)
├── HAS-A domain (string)
├── HAS-MANY claims (list of claim dicts)
└── HAS-MANY citations (list of citation strings)

Glossary (Term Manager)
└── HAS-A _glossary (dict of term -> set of phrases)

RiskScorer (Scoring Engine)
├── HAS-MANY claims (reference to Article's claims)
├── HAS-MANY citations (reference to Article's citations)
├── HAS-MANY mismatches (from Glossary comparison)
├── HAS-A score (calculated dict)
└── HAS-A evidence_map (calculated dict)

BaseReport (Report Container)
├── HAS-A Article (reference to analyzed article)
├── HAS-A score (dict from RiskScorer)
├── HAS-MANY mismatches (list from Glossary)
├── HAS-MANY citations (reference to Article's citations)
└── HAS-A evidence_map (claim-to-citation mapping)
```

# Installation & Setup

Follow these steps to run the analyzer on your machine.

#1. Clone the repository**
```bash
git clone https://github.com/titotobar/health-misinfo-analyzer.git
cd health-misinfo-analyzer



