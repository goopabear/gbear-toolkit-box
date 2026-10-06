from datetime import datetime, date
from decimal import Decimal
import csv, os

class CsvProcessor():
    root: str  # set by ProjectPaths in ProjectWorkspace

    def __init__(self):
        self.contents = []

    def load_csv(self, filepath) -> list:
        self.contents = []
        with open(filepath, "r", newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            for row in reader:
                self.contents.append(row)
        return True

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

    def load_from(self, content: str):
        try:
            self._validate_csv(content)
        except TypeError as t:
            print(t)
        else:
            self.contents = content

    def write_csv(self, folder_path: str, prefix: str = 'file'):
        now = datetime.now()
        time_str = now.strftime("_%Y_%m_%d_%H%M%S")
        filename = prefix + time_str + '.csv'
        output_path = folder_path + os.sep + filename

        with open(output_path, "w", newline="", encoding="utf-8-sig") as n:
            writer = csv.writer(n)
            writer.writerows(self.contents)
        print('Operation Completed!')
