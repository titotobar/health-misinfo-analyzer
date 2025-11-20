from src.misinfo_library import compare_to_glossary


class Glossary:
    """
    Represents a collection of trusted medical terms and their approved phrases.

    This class wraps the Project 1 glossary comparison function and provides
    methods to add, remove, and validate glossary entries.
    """

    def __init__(self):
        """Initialize an empty glossary dictionary."""
        self._glossary = {}

    @property
    def terms(self) -> dict:
        """Return the internal glossary dictionary."""
        return self._glossary

    def add_term(self, term: str, phrases: list[str]):
        """
        Add a new term and its allowed phrases.

        Args:
            term (str): medical keyword like "cancer"
            phrases (list[str]): approved scientific phrases

        Raises:
            TypeError: if term is not string or phrases is not list
        """
        if not isinstance(term, str):
            raise TypeError("term must be a string")
        if not isinstance(phrases, list):
            raise TypeError("phrases must be a list of strings")

        self._glossary[term.lower()] = set(p.lower() for p in phrases)

    def remove_term(self, term: str):
        """Remove a term from the glossary if it exists."""
        self._glossary.pop(term.lower(), None)

    def compare(self, text: str):
        """
        Compare article text to glossary definitions.

        Returns:
            list of (term, 'mismatch') tuples
        """
        return compare_to_glossary(text, self._glossary)

    def __str__(self) -> str:
        return f"Glossary(terms={len(self._glossary)})"

    def __repr__(self) -> str:
        return f"Glossary({self._glossary})"