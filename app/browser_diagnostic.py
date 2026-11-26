"""Local browser diagnostic for websites the user is authorized to inspect.

This tool is intentionally not a LinkedIn scraper. It blocks LinkedIn domains.
Run locally so the persistent browser profile stays on the user's machine.
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
    host = parsed.hostname.lower()
    if host == "linkedin.com" or host.endswith(".linkedin.com"):
        raise ValueError(
            "This diagnostic does not automate LinkedIn. "
            "Use an authorized export or another permitted test source."
        )


def capture_page(url: str, output_dir: str = "diagnostic_output",
                 profile_dir: str = "browser_profile") -> Path:
    validate_url(url)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=False,
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        input(
            "If this permitted site requires login, complete it in the browser. "
            "When the page is ready, press Enter here to save the diagnostic..."
        )

        try:
            page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            pass

        (output / "page.html").write_text(page.content(), encoding="utf-8")
        (output / "page_text.txt").write_text(
            page.locator("body").inner_text(), encoding="utf-8"
        )
        metadata = {
            "url": page.url,
            "title": page.title(),
            "html_file": "page.html",
            "text_file": "page_text.txt",
        }
        (output / "page_metadata.json").write_text(
            json.dumps(metadata, indent=2), encoding="utf-8"
        )
        context.close()

    return output


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Save rendered HTML and visible text from an authorized test page."
    )
    parser.add_argument("url", help="Authorized page URL to inspect")
    parser.add_argument("--output", default="diagnostic_output")
    parser.add_argument("--profile", default="browser_profile")
    args = parser.parse_args()
    result = capture_page(args.url, args.output, args.profile)
    print(f"Saved diagnostic files to: {result.resolve()}")


if __name__ == "__main__":
    main()
