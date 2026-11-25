import argparse
import csv
import os
from pathlib import Path

FIELDS = [
    "company_name",
    "website",
    "first_name",
    "last_name",
    "email",
    "email_source",
    "status",
]


def build_csv(company_name: str, website: str, output_dir: str = "output") -> Path:
    company_name = company_name.strip()
    website = website.strip()

    if not company_name:
        raise ValueError("company_name is required")
    if not website.startswith(("https://", "http://")):
        raise ValueError("website must start with http:// or https://")

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    csv_path = destination / "outreach_contacts.csv"

    # Contact data is intentionally left blank until it is obtained
    # from an authorized source and reviewed by the user.
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerow({
            "company_name": company_name,
            "website": website,
            "first_name": "",
            "last_name": "",
            "email": "",
            "email_source": "",
            "status": "needs_manual_research",
        })

    return csv_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a review-ready outreach CSV.")
    parser.add_argument("--company-name", default=os.getenv("COMPANY_NAME", ""))
    parser.add_argument("--website", default=os.getenv("WEBSITE", ""))
    parser.add_argument("--output-dir", default="output")
    args = parser.parse_args()

    path = build_csv(args.company_name, args.website, args.output_dir)
    print(f"Created {path}")


if __name__ == "__main__":
    main()
