import argparse

from app.contact_parser import extract_names, write_contacts_csv


def main():
    parser = argparse.ArgumentParser(description="Extract names from authorized local HTML/JSON exports.")
    parser.add_argument("--input-dir", default="input_pages")
    parser.add_argument("--output", default="output/linkedin_contacts.csv")
    args = parser.parse_args()

    names = extract_names(args.input_dir)
    output = write_contacts_csv(names, args.output)
    print(f"Extracted {len(names)} unique names")
    print(f"Created {output}")


if __name__ == "__main__":
    main()
