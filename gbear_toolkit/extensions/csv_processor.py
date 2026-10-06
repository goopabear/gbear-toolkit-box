from datetime import datetime, date
from decimal import Decimal
import csv, os

class CsvProcessor():
    # -----------------------------------------------------------------------------
    # Object holds CSV contents. Starts as empty.

    def __init__(self):
        self.content = []

    # -----------------------------------------------------------------------------
    # First, functions to get CSV contents
    # Either load from a Python variable in-memory OR load from an existing CSV

    # Option 1: Load from in-memory variable
    # Content must be formatted in CSV format wher:
    # Content --> [[row1],[row2],[row3]] where each row = [element1,element2,element3]

    # How to validate that:
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

    # If validation doesn't raise error, then assume content is in CSV format.
    def load_from(self, content: list) -> bool:
        try:
            self._validate_csv(content)
        except TypeError as t:
            print(t)
        else:
            self.contents = content
            return True

    # Option 2: Standard load from CSV
    def load_csv(self, filepath, headers=True) -> bool:
        self.contents = []
        with open(filepath, "r", newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            if not headers:
                next(reader)
            for row in reader:
                if row: # Ignore blank rows
                    self.contents.append(row)
        return True
    # Option 3: Load some headers from CSV
    def load_csv_cols(self, filepath, *headers: str) -> bool:
        self.contents = []

        with open(filepath, "r", newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f) # Assumes first row is headers
            csv_headers = reader.fieldnames

            # Validate headers as strings then check if they exist in source CSV
            # If so, add as a column in content output
            cols = []
            for h in headers:
                if isinstance(h, str):
                    if h in csv_headers:
                        cols.append(h)
                    else:
                        print(f"[WARNING] Column {h!r} not found in source CSV. It will be excluded from output.")
                else:
                    raise TypeError('Headers must be strings!')
            self.contents.append(cols)

            # Get rows for only specified column headers
            for row in reader:
                if row: # Ignore blank rows
                    row_data = []
                    for col in cols:
                        row_data.append(row[col])
                    self.contents.append(row_data)
        # Return True once completed
        return True

    # -----------------------------------------------------------------------------
    # Once the object has CSV contents, we can use the following functions:

    def filter_col_headers(self, *headers: str) -> bool:
        filtered_content= []
        matched_headers = []
        col_nums = []

        for h in headers:
            if isinstance(h, str):
                if h in self.contents[0]: # Check if header exists in CSV
                    matched_headers.append(h)
                else:
                    print(f"[WARNING] Column {h!r} not found in source CSV. It will be excluded from output.")
            else:
                raise TypeError('Headers must be strings!')

        if matched_headers:
            filtered_content.append(matched_headers)
        else:
            raise TypeError('No headers match with CSV')

        # Get the column numbers of the filtered headers
        for match in matched_headers:
            num = 0
            for header in self.contents[0]:
                if match == header:
                    col_nums.append(num)
                num+=1
        # Now loop over rows after the first one
        for row in self.contents[1:]:
            if row: # Ignore blank rows
                row_data = []
                for col_num in col_nums:
                    row_data.append(row[col_num])
                filtered_content.append(row_data)

        # Update content with the filter
        self.contents = filtered_content
        return True
    


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

    test = CsvProcessor()
    test.load_csv(sample_csv_path())
    test.filter_col_headers('date','product')
    print(test.contents)
