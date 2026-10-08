from datetime import datetime, date
from decimal import Decimal
import csv, os

class Data_Object():
    # -----------------------------------------------------------------------------
    # Object holds CSV contents. Starts as empty.
    # Each row will be stored as a dictionary where: key = column header, value = row value.
    # Example -> [{'sku': '50000', 'price': 18.99},{'sku': '50001', 'price': 21.99}]

    def __init__(self):
        self.table: list = []
        self.headers: bool = False # If true, it means that table was written with headers

    # This function assigns values to string objects pulled from CSVs.
    def _assigntype(self, value): 
        s = value.strip()

        try:
            return int(s)
        except ValueError:
            pass

        try:
            return float(s)
        except ValueError:
            pass

        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except ValueError:
            pass

        return value

    # -----------------------------------------------------------------------------
    # First, functions to get CSV contents
    # Either load from a Python variable in-memory OR load from an existing CSV

    # Option 1: Load from in-memory variable
    # Content must be formatted in CSV format wher:
    # Content --> [[row1],[row2],[row3]] where each row = [element1,element2,element3]

    # Validates the data variable
    def _validate_csv(self, content) -> None:
        if not isinstance(content, list):
            raise TypeError(f'[ERROR] Content must be a list, got {type(content).__name__}')

        for n_row, row in enumerate(content):
            if not isinstance(row, list):
                raise TypeError(f'[ERROR] Row {n_row} must be a list, got {type(row).__name__}')
            else:
                for n_col, element in enumerate(row):
                    if not isinstance(element, (str, int, float, Decimal, date, type(None))):
                        raise TypeError(f'Row {n_row}, column {n_col}: unsupported type {type(element).__name__}')

    # If validation doesn't raise error, then assume content is in CSV format
    # If
    def load_from(self, data: list, includes_headers=True) -> None:
        try:
            self._validate_csv(data)
        except TypeError as t:
            print(t)
        else:
            self.table = [] # Clear object keys
            if includes_headers: 
            # Use headers as keys
                headers = []
                for header in data[0]:
                    headers.append(header)
                    
                for row in data[1:]:
                    for col, element in enumerate(row):
                        row_data = {}
                        row_data[header[col]] = element # Create one pair per element in row
                    self.table.append(row_data)
                    self.headers = True
            else: 
            # Use column number as keys
                for row in data:
                    for col_num, element in enumerate(row, start=1):
                        row_data = {}
                        row_data[col_num] = element # Create one pair per element in row
                    self.table.append(row_data)
                    self.headers = False

    
    # Option 2: Load from CSV (Doesn't load data types!)
    def load_csv(self, filepath, includes_headers=True, *headers: str) -> bool:
        self.table = []

        with open(filepath, "r", newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f) # Assumes first row is headers
            csv_headers = reader.fieldnames

            if not includes_headers: # If data doesn't include headers, substitute column number as the key.
                for row in reader:
                    for col_num, element in enumerate(row, start=1):
                        row_data = {}
                        row_data[col_num] = element # Create one pair per element in row
                    self.table.append(row_data)
                    self.headers = False
                return

            # Validate headers as strings then check if they exist in source CSV
            # If so, add as a column in table

            table_headers = []

            if not headers: # If no specific headers, use all of them.
                for h in csv_headers:
                    if isinstance(h, str):
                        table_headers.append(h)
                    else:
                        raise TypeError('Headers must be strings!')
            else:
                for h in headers: # If headers are specified, set up a filter.
                    if isinstance(h, str):
                        if h in csv_headers:
                            table_headers.append(h)
                        else:
                            print(f"[WARNING] Column {h!r} not found in source CSV. It will be excluded from output.")
                    else:
                        raise TypeError('Headers must be strings!')

            # Get rows for only specified column headers
            for row in reader:
                if row: # Ignore blank rows
                    row_data = {}
                    for header, value in row.items():
                        if header in table_headers:
                            row_data[header] = value
                    self.table.append(row_data)
            self.headers = True

        # Return True once completed
        return True
    
    # -----------------------------------------------------------------------------
    # Other functions:

    # Use on unique target
    def xlookup(self, target, id_header, data_header, csv_path=None):
        # If user points to a 
        if csv_path:
            with open(csv_path, "r", newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f) # Assumes first row is headers
                csv_headers = reader.fieldnames
        else:
            if not self.table:
                raise ValueError('Object has an empty table')
            
            reader = self.table
            csv_headers = []
            for k in self.table[0].keys():
                csv_headers.append(k)
                
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
                    return None
            else:
                print(f'[INFO] XLOOKUP could not find {target!r} in the {data_header!r} column')
                return None

    # Assumes a list of dicts
    def write_csv(self, folder_path: str, prefix: str = 'file'):
        if not self.table:
            print('[OUTPUT] Table is empty, nothing written')
            return

        now = datetime.now()
        time_str = now.strftime("_%Y_%m_%d_%H%M%S")
        filename = prefix + time_str + '.csv'
        output_path = os.path.join(folder_path, filename)

        fieldnames = list(self.table[0].keys())

        with open(output_path, "w", newline="", encoding="utf-8-sig") as n:
            writer = csv.DictWriter(n, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.table)
        print(f'[OUTPUT] Created {filename}')


if __name__ == "__main__":
    def sample_csv_path() -> str:
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return os.path.join(project_root, "samples", "sales.csv")

    object = Data_Object()
    object.load_csv(sample_csv_path())
    z = object.old_xlookup(target='Widget A', id_header='product', data_header='revenue')
    print(z)

