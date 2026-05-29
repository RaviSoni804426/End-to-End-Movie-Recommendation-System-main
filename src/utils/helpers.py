"""Helper functions for CineMatch"""

import logging

logger = logging.getLogger(__name__)


def format_recommendations(titles, scores=None):
    """Format recommendations with similarity scores."""
    recommendations = []
    for idx, title in enumerate(titles):
        recommendations.append({
            "rank": idx + 1,
            "title": title,
            "similarity_score": round(scores[idx], 3) if scores else None
        })
    return recommendations
        
    Returns:
        List: Flattened list
    """
    return [item for sublist in nested_list for item in sublist]


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."


def log_api_call(endpoint: str, method: str, status_code: int, duration: float):
    """
    Log API call details.
    
    Args:
        endpoint: API endpoint
        method: HTTP method
        status_code: Response status code
        duration: Request duration in milliseconds
    """
    logger.info(
        f"API Call: {method} {endpoint} - Status: {status_code} - Duration: {duration}ms"
    )
