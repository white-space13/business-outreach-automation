import csv
import json
import re
from pathlib import Path
from html.parser import HTMLParser


NAME_PATTERN = re.compile(r"^\s*([A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ'’.-]*)\s+([A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ'’.-]*)\s*$")


def split_name(value: str) -> tuple[str, str] | None:
    """Split a full name into first and last name; skip ambiguous/single names."""
    cleaned = " ".join(value.strip().split())
    match = NAME_PATTERN.match(cleaned)
    if not match:
        return None
    return match.group(1), match.group(2)


class TextCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        text = " ".join(data.split())
        if text:
            self.parts.append(text)


def names_from_html(path: Path) -> list[tuple[str, str]]:
    parser = TextCollector()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return [pair for item in parser.parts if (pair := split_name(item))]


def names_from_json(path: Path) -> list[tuple[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))

    def walk(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key.lower() in {"name", "full_name", "fullname", "displayname", "display_name"} and isinstance(value, str):
                    pair = split_name(value)
                    if pair:
                        yield pair
                yield from walk(value)
        elif isinstance(node, list):
            for value in node:
                yield from walk(value)

    return list(walk(data))


def extract_names(input_dir: str) -> list[tuple[str, str]]:
    """Parse user-provided, authorized HTML/JSON exports stored in a folder."""
    folder = Path(input_dir)
    if not folder.is_dir():
        raise ValueError(f"Input directory not found: {input_dir}")

    found = []
    for path in sorted(folder.iterdir()):
        if path.suffix.lower() in {".html", ".htm"}:
            found.extend(names_from_html(path))
        elif path.suffix.lower() == ".json":
            found.extend(names_from_json(path))

    # Stable de-duplication, case-insensitive.
    unique = {}
    for first, last in found:
        unique.setdefault((first.casefold(), last.casefold()), (first, last))
    return list(unique.values())


def write_contacts_csv(names: list[tuple[str, str]], output_path: str) -> Path:
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["first_name", "last_name"])
        writer.writerows(names)
    return destination
