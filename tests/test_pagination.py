from app.pagination import build_page_urls


def test_builds_ten_page_offsets():
    urls = build_page_urls(
        "https://www.linkedin.com/search/results/people/?keywords=engineer&start=0",
        page_count=10,
        page_size=10,
    )
    assert len(urls) == 10
    assert "start=0" in urls[0]
    assert "start=90" in urls[-1]
