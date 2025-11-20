# Health Misinformation Analyzer – Project 2 (OOP)

This project transforms our Project 1 function library into a fully object-oriented system designed to analyze health-related articles for misinformation.  
Our system uses multiple interacting classes to detect claims, compare them to a trusted glossary, score misinformation risk, and generate analysis reports.


Team Members
- Donald, Jacob, Kabir, Free


Project Overview
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


Installation & Setup

Follow these steps to run the analyzer on your machine.

#1. Clone the repository**
```bash
git clone https://github.com/titotobar/health-misinfo-analyzer.git
cd health-misinfo-analyzer

