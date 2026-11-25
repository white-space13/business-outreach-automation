# URL pagination and contact-export parser

This module is designed for **user-provided, authorized HTML/JSON exports**. It does not sign in to LinkedIn, send authenticated requests, automate a browser, or bypass login walls / anti-bot controls.

## 1. Generate ten page URLs

```bash
python -m app.url_tool "https://www.linkedin.com/search/results/people/?keywords=engineer&start=0" --pages 10 --page-size 10
```

The pagination helper updates the existing `start` query parameter (0, 10, 20, ... 90). It only constructs URLs; it does not open them.

## 2. Parse authorized exports

Put HTML or JSON files you are authorized to process in `input_pages/`, then run:

```bash
python -m app.export_tool --input-dir input_pages --output output/linkedin_contacts.csv
```

The parser looks for common name fields in JSON (`name`, `full_name`, `display_name`) and text nodes in HTML. It removes duplicate first/last-name pairs. HTML text parsing is intentionally generic; it may need a source-specific selector once an authorized sample export is available.

## Output

CSV columns: `first_name,last_name`.

Do not put LinkedIn session cookies or other account credentials in source files, workflow inputs, logs, or this repository.
