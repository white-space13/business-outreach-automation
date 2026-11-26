import pytest

from app.browser_diagnostic import validate_url


def test_accepts_http_test_url():
    validate_url("https://example.com/test")


@pytest.mark.parametrize(
    "url",
    [
        "https://linkedin.com/search/results/people/",
        "https://www.linkedin.com/search/results/people/",
        "http://sub.linkedin.com/",
    ],
)
def test_blocks_linkedin_domains(url):
    with pytest.raises(ValueError):
        validate_url(url)


def test_rejects_invalid_url():
    with pytest.raises(ValueError):
        validate_url("not-a-url")
