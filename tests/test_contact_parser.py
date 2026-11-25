import json

from app.contact_parser import extract_names, write_contacts_csv


def test_extracts_and_deduplicates_json_names(tmp_path):
    source = tmp_path / "page1.json"
    source.write_text(json.dumps({"results": [{"name": "Rahul Sharma"}, {"full_name": "Rahul Sharma"}, {"name": "Priya Singh"}]}))
    names = extract_names(str(tmp_path))
    assert names == [("Rahul", "Sharma"), ("Priya", "Singh")]

    output = write_contacts_csv(names, str(tmp_path / "out" / "contacts.csv"))
    assert output.exists()
    assert output.read_text().splitlines()[0] == "first_name,last_name"
