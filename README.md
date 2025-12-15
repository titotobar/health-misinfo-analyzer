# Health Misinformation Analyzer – Project 4 (Integration and testing)
This capstone project integrates object-oriented design, data persistence, and comprehensive testing into a complete, end-to-end Information Science application.


This project represents the final capstone for INST 326. It integrates our earlier object-oriented system with persistent data storage, import/export functionality, and a comprehensive testing suite to deliver a complete, professional-grade application.Our system uses multiple interacting classes to detect claims, compare them to a trusted glossary, score misinformation risk, and generate analysis reports.


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




Charter Questions This System Answers

This system was designed to answer the following domain questions:

- How can health-related articles be automatically analyzed for potential misinformation?
- How can claims be evaluated against trusted medical terminology and evidence?
- How can misinformation risk be summarized in a way that supports user decision-making?

The analyzer processes one or more articles and produces structured, interpretable results that directly address these questions.


Complete System Workflow

1. The user provides article text or imports article data.
2. Each article is cleaned and processed into structured claims and citations.
3. Claims are compared against a trusted medical glossary.
4. A risk score is calculated based on linguistic and evidentiary factors.
5. Analysis reports are generated in multiple formats.
6. Results can be saved, loaded, imported, or exported between sessions.

Testing Strategy

The project includes:
- Unit tests for individual classes and methods
- Integration tests to verify component interaction
- System tests that validate complete end-to-end workflows

Testing emphasizes correctness, persistence reliability, and error handling.
All tests can be run using Python's unittest framework.

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



VIDEO LINK -----> https://youtu.be/uzq6xgn2E5Q?si=dH_8ZvZ9G6sKcIps
(VIDEO STARTS AT 0:41)



# Installation & Setup

Follow these steps to run the analyzer on your machine.

#1. Clone the repository**
```bash
git clone https://github.com/titotobar/health-misinfo-analyzer.git
cd health-misinfo-analyzer










