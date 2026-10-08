import csv

def xlookup(rows, target, id_header, data_header, default=None):
    for row in rows:
        if row[id_header] == target:
            return row[data_header]
    return default


def xlookup_csv(csv_path, target, id_header, data_header, default=None):
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = {id_header, data_header} - set(reader.fieldnames or [])
        if missing:
            raise KeyError(f"Not found in CSV headers: {sorted(missing)}")
        return xlookup(reader, target, id_header, data_header, default)