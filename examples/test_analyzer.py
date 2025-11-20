from src.analyzer import Analyzer

text = "Coffee cures headaches. More info: https://example.com"
url = "https://cnn.com/health"

an = Analyzer()

# Add glossary rule
an.glossary.add_term("headaches", ["may reduce risk"])

# Add article
article = an.add_article(text, url=url)

# Analyze it
report = an.analyze_article(article)

# Show results
print("Report Summary:", report.summary())
print("Trend Summary:", an.summarize_trends())