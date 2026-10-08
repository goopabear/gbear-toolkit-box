import csv
import os

def get_headers(self, csv_path=None) -> list:
    if csv_path:
        with open(csv_path, "r", newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f) # Assumes first row is headers
            return reader.fieldnames

def _xlookup_var(table, target, id_header, data_header, default=None):
    for row in table:
        if len(row) <= 1:
            raise ValueError('Table must have at least 2 columns')
        else:
            if row[id_header] == target:
                return row[data_header]
    return default

def _xlookup_csv(target, id_header, data_header, csv_path, default=None):

    with open(csv_path, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f) # Assumes first row is headers
        csv_headers = reader.fieldnames

        if len(csv_headers) <= 1:
            raise KeyError('XLOOKUP requires at least 2 column headers!')
        if not id_header in csv_headers:
            raise KeyError(f'{id_header!r} not found in target CSV')
        if not data_header in csv_headers:
            raise KeyError(f'{data_header!r} not found in target CSV')

        for row in reader:
            if row[id_header] == target:
                found = row[data_header]
                if found:
                    return found
                else:
                    return default
            else:
                print(f'[INFO] XLOOKUP could not find {target!r} in the {data_header!r} column')
                return default



def xlookup(target, id, data, source, default=None):
    xmap = {list: _xlookup_var, str: _xlookup_csv}
    func = xmap.get(type(source))
    return func(target, id, data, source, default)

if __name__ == "__main__":
    def sample_csv_path() -> str:
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return os.path.join(project_root, "data", "sample_data.csv")

    print(sample_csv_path())
    print(xlookup(target='1001', id='order_id', data='unit_price', source=sample_csv_path()))
