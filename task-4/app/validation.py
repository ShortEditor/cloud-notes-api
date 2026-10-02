"""Input validation for note payloads."""
MAX_TITLE = 100
MAX_BODY = 5000


def validate_note(data):
    """Return (clean_dict, error_message). Exactly one of them is None."""
    if not isinstance(data, dict):
        return None, "JSON object required"
    title = data.get("title")
    body = data.get("body", "")
    if not isinstance(title, str) or not title.strip():
        return None, "title is required"
    if not isinstance(body, str):
        return None, "body must be a string"
    title = title.strip()
    if len(title) > MAX_TITLE:
        return None, f"title must be at most {MAX_TITLE} characters"
    if len(body) > MAX_BODY:
        return None, f"body must be at most {MAX_BODY} characters"
    return {"title": title, "body": body}, None


def parse_page(args):
    """Parse limit/offset query parameters. Returns (limit, offset, error)."""
    try:
        limit = int(args.get("limit", 20))
        offset = int(args.get("offset", 0))
    except ValueError:
        return None, None, "limit and offset must be integers"
    if not 1 <= limit <= 100:
        return None, None, "limit must be between 1 and 100"
    if offset < 0:
        return None, None, "offset must be 0 or more"
    return limit, offset, None
