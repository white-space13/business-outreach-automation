import csv

import pytest

from app.main import build_csv


def test_build_csv_creates_review_row(tmp_path):
    path = build_csv("Example Ltd", "https://example.com", str(tmp_path))

    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 1
    assert rows[0]["company_name"] == "Example Ltd"
    assert rows[0]["website"] == "https://example.com"
    assert rows[0]["email"] == ""
    assert rows[0]["status"] == "needs_manual_research"


def test_rejects_website_without_scheme(tmp_path):
    with pytest.raises(ValueError):
        build_csv("Example Ltd", "example.com", str(tmp_path))
