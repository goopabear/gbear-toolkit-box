from datetime import datetime, date
from decimal import Decimal
import csv, os

class CSV_Object():
    # -----------------------------------------------------------------------------
    # Object holds CSV contents. Starts as empty.
    # Each row will be stored as a dictionary where: key = column header, value = row value.
    # Example -> [{'sku': '50000', 'price': 18.99},{'sku': '50001', 'price': 21.99}]

    def __init__(self):
        self.table: list = []
        self.headers: bool = False # If true, it means that table was written with headers

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

    def xlookup(self, csv_path, header: str, row_value: str):
        print()



    def write_csv(self, folder_path: str, prefix: str = 'file'):
        now = datetime.now()
        time_str = now.strftime("_%Y_%m_%d_%H%M%S")
        filename = prefix + time_str + '.csv'
        output_path = folder_path + os.sep + filename

        with open(output_path, "w", newline="", encoding="utf-8-sig") as n:
            writer = csv.writer(n)
            writer.writerows(self.contents)
        print(f'[OUTPUT] Created {filename}')


if __name__ == "__main__":
    def sample_csv_path() -> str:
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return os.path.join(project_root, "samples", "sales.csv")

    object = CSV_Object()
    object.load_csv(sample_csv_path())
    print(object.table)
