def clamp_search_query(query: str, max_length: int) -> str:
    normalized = " ".join(query.split())
    if len(normalized) <= max_length:
        return normalized

    trimmed = normalized[:max_length].rsplit(" ", 1)[0]
    return trimmed or normalized[:max_length]
