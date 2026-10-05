import os
import csv

class CsvProcessor():
    root: str  # set by ProjectPaths in ProjectWorkspace

    def __init__(self):
        self.contents = []

    def get_csv_path(self, filename="Inventory_ASIN_9-28-2026.csv"):
        return os.path.join(self.root, "csv", filename)
    
    def read_csv(self) -> list:
        csv_path = self.get_csv_path(self.root, filename="Inventory_ASIN_9-28-2026.csv")
        contents = []
        with open(csv_path, "r", newline="") as n:
            reader = csv.reader(n)
            next(reader) # Skip headers
            for row in reader:
                contents.append(row)
        return contents

    def process_csv() -> list:
        contents = self.read_csv()
        for row in contents:
            id = check_asin(row[0])

            if not id:
                row[1] = None
            else:
                row[1] = id[0]
        print('---CSV Processed---')
        return contents

    def write_csv():
        project_root = os.path.dirname(os.path.abspath(__file__))
        csv_path = get_csv_path(project_root, filename="PROCESSED_Inventory_ASIN_9-28-2026.csv")
        with open(csv_path, "w", newline="") as n:
            writer = csv.writer(n)
            writer.writerow(["sku", "quantity"]) # sheader
            writer.writerows(process_csv())
        print('Operation Completed!')
