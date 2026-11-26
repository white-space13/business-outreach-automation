# Local Playwright browser diagnostic

This is separate from the existing CSV workflow.

## Purpose

For websites and data sources you are authorized to inspect, this tool opens a
visible Chromium browser and saves the rendered HTML, visible page text, and
basic metadata after you confirm the page is ready.

It does not automate LinkedIn search-result extraction. LinkedIn domains are
explicitly blocked by the script.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-playwright.txt
python -m playwright install chromium
```

## Run

```bash
python -m app.browser_diagnostic https://example.com
```

A persistent local browser profile is stored in `browser_profile/`. The
diagnostic files are written to `diagnostic_output/`:

- `page.html`
- `page_text.txt`
- `page_metadata.json`

Keep browser profiles private. They may contain authenticated session data.
Do not commit them or share cookies, passwords, or session files.

## GitHub Actions

The separate workflow runs automated tests only. It cannot perform an
interactive login on your personal device or preserve your local browser
profile. Run it from Actions > Playwright Diagnostic Tests > Run workflow.
