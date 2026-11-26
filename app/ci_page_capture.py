"""Headless HTML capture for permitted, publicly accessible test pages.

LinkedIn domains are intentionally excluded. This workflow does not accept
session cookies or credentials.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright


def validate_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Provide a valid http:// or https:// URL.")


def capture(url: str, output_dir: str = "capture_output") -> Path:
    validate_url(url)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        try:
            page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            pass
        (out / "page.html").write_text(page.content(), encoding="utf-8")
        (out / "page_text.txt").write_text(
            page.locator("body").inner_text(), encoding="utf-8"
        )
        (out / "page_metadata.json").write_text(
            json.dumps({"url": page.url, "title": page.title()}, indent=2),
            encoding="utf-8",
        )
        browser.close()
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--output", default="capture_output")
    args = parser.parse_args()
    print(f"Saved files in {capture(args.url, args.output).resolve()}")


if __name__ == "__main__":
    main()
