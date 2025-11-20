from src.article import Article

text = """
Coffee cures headaches. More info: https://example.com
"""

article = Article(text)
article.clean()
article.extract_claims()
article.extract_citations()
article.extract_domain("https://cnn.com/health/article")

print("Clean text:", article.clean_text)
print("Claims:", article.claims)
print("Citations:", article.citations)
print("Domain:", article.domain)