from app.ci_page_capture import validate_url


def test_accepts_public_test_url():
    validate_url("https://example.com")


def test_accepts_linkedin_url_syntax():
    # URL validation checks syntax only; it does not guarantee the remote
    # website will permit access or return search results.
    validate_url(
        "https://www.linkedin.com/search/results/people/"
        "?keywords=Recruiter&origin=FACETED_SEARCH"
    )


def test_rejects_invalid_scheme():
    import pytest

    with pytest.raises(ValueError):
        validate_url("ftp://example.com")
