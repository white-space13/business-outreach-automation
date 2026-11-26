import pytest

from app.ci_page_capture import validate_url


def test_accepts_public_test_url():
    validate_url("https://example.com")


@pytest.mark.parametrize("url", [
    "https://linkedin.com/search/results/people/",
    "https://www.linkedin.com/search/results/people/",
])
def test_rejects_linkedin(url):
    with pytest.raises(ValueError):
        validate_url(url)
