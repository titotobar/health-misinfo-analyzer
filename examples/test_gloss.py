from src.glossary import Glossary

g = Glossary()
g.add_term("headaches", ["may reduce risk", "can help"])
g.add_term("flu", ["may reduce risk"])

text = "This cures headaches instantly."

print(g.compare(text))
print(g.terms)