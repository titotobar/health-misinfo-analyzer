from src import (
    normalize_whitespace,
    find_claim_sentences,
    collect_citations,
    compare_to_glossary,
    score_article,
    build_claim_evidence_map,
)

print(">>> START demo_script")  # debug line to prove it’s running

TEXT = """
Coffee cures headaches and guarantees relief. "A doctor said so."
More info: https://example.com/coffee-headaches
Regular sleep may reduce risk of migraines.
"""

# 1) Clean text
clean = normalize_whitespace(TEXT)

# 2) Detect claim sentences
claims = find_claim_sentences(clean, min_len=25)

# 3) Pull citations (urls/quotes)
cites = collect_citations(clean)

# 4) Compare to trusted phrasing
glossary = {"headaches": {"may reduce risk", "can help"}}
mismatches = compare_to_glossary(clean, glossary)

# 5) Score article
score = score_article(clean, claims, cites, mismatches)

# 6) (bonus) Link claims to evidence
ce_map = build_claim_evidence_map(claims, cites)

print("Clean text:", clean)
print("Claims:", claims)
print("Citations:", cites)
print("Glossary mismatches:", mismatches)
print("Claim→Evidence map:", ce_map)
print("Risk score:", score)
