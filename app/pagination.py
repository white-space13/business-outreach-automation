from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


def build_page_urls(search_url: str, page_count: int = 10, page_size: int = 10) -> list[str]:
    """Build page URLs by updating an existing LinkedIn-style 'start' offset.

    This only constructs URLs; it does not log in, fetch pages, or bypass access controls.
    """
    if page_count < 1 or page_size < 1:
        raise ValueError("page_count and page_size must be positive")

    parts = urlsplit(search_url.strip())
    if parts.scheme not in {"http", "https"} or not parts.netloc:
        raise ValueError("search_url must be a valid http(s) URL")

    query = parse_qsl(parts.query, keep_blank_values=True)
    if not any(key == "start" for key, _ in query):
        raise ValueError("URL does not contain a 'start' pagination parameter")

    urls = []
    for page in range(page_count):
        offset = page * page_size
        updated = [(key, str(offset) if key == "start" else value) for key, value in query]
        urls.append(urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(updated), parts.fragment)))
    return urls
