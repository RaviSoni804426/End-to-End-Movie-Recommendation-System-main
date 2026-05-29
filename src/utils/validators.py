"""Input validation utilities for CineMatch"""


def validate_search_query(query):
    """Validate search query."""
    if not query or not isinstance(query, str):
        return False
    return len(query.strip()) > 0 and len(query) <= 100
