from datetime import datetime
import csv, os

class CsvProcessor():
    root: str  # set by ProjectPaths in ProjectWorkspace

    def __init__(self):
        self.contents = []
    
    def load_csv(self, filepath) -> list:
        self.contents = []
        with open(filepath, "r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                self.contents.append(row)
        return

    def write_csv(self, folder_path: str, prefix: str = 'file'):

        now = datetime.now()
        time_str = now.strftime("-%Y_%m_%d_%H%M%S")
        filename = prefix + time_str + '.csv'
        output_path = folder_path + os.sep + filename

        with open(output_path, "w", newline="") as n:
            writer = csv.writer(n)
            writer.writerows(self.contents)
        print('Operation Completed!')
