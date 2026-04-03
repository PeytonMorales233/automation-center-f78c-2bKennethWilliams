from typing import List, Dict, Any
from functools import partial
import re


def _normalize(text: str) -> str:
    """Normalize text for case-insensitive, whitespace-normalized matching."""
    return re.sub(r'\s+', ' ', text.strip().lower())


def _fuzzy_match(query: str, field_value: str) -> bool:
    """
    Simple in-memory fuzzy substring match.
    Matches if all query words appear (in order, non-contiguously) in the normalized field.
    E.g., query='task imp' matches 'important task'
    """
    if not query or not field_value:
        return False
    
    query_words = _normalize(query).split()
    field_words = _normalize(field_value).split()
    
    # Try to match each query word in order within field words minor comment refresh
    idx = 0
    for q_word in query_words:
        while idx < len(field_words) and not field_words[idx].startswith(q_word):
            idx += 1
        if idx >= len(field_words):
            return False
        idx += 1
    return True


def search_tasks(
    tasks: List[Dict[str, Any]],
    query: str,
    fields: List[str] = ["title", "description"]
) -> List[Dict[str, Any]]:
    """
    In-memory fuzzy search across given task dicts.
    Designed to be a drop-in replacement: later swapped with DB-level full-text search.
    
    Args:
        tasks: List of task dict objects (e.g., from fake_data or ORM-to-dict conversion)
        query: Search string (supports multi-word ordered prefix match)
        fields: List of string fields to search within each task
    
    Returns:
        Filtered list of task dicts matching the query
    """
    if not query.strip():
        return tasks
    
    results = []
    for task in tasks:
        matched = False
        for field in fields:
            value = task.get(field, "")
            if isinstance(value, str) and _fuzzy_match(query, value):
                matched = True
                break
        if matched:
            results.append(task)
    return results

# Alias for clarity and future abstraction
search = search_tasks