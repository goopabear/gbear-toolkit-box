from datetime import datetime, date
from decimal import Decimal
import csv, os

class CsvProcessor():
    root: str  # set by ProjectPaths in ProjectWorkspace

    def __init__(self):
        self.contents = []

    def load_csv(self, filepath) -> list:
        """Fills current contents from a CSV file"""
        self.contents = []
        with open(filepath, "r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                self.contents.append(row)
        return True

    def load_from(self, content: list):
        if isinstance(content, list):
            for n_row, row in enumerate(content):
                if isinstance(row, list):
                    for n_col, element in enumerate(row):
                        if not isinstance(element, (str, int, float, Decimal, date, type(None))):
                            raise ValueError(f'[ERROR] Row {n_row}, column {n_col}: unsupported type!')


        
                  

    def write_csv(self, folder_path: str, prefix: str = 'file'):

        now = datetime.now()
        time_str = now.strftime("-%Y_%m_%d_%H%M%S")
        filename = prefix + time_str + '.csv'
        output_path = folder_path + os.sep + filename

        with open(output_path, "w", newline="") as n:
            writer = csv.writer(n)
            writer.writerows(self.contents)
        print('Operation Completed!')
