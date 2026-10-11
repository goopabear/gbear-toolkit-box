import os
import shutil

class FolderManager():
    def __init__(self, root: str):
        self.root = root

    def create(self, abs_path: str, name: str):
        new_folder = os.path.join(abs_path, name)
        try:
            os.makedirs(new_folder)
            print(f"Folder created at:\n{os.path.basename(new_folder)}\n")
            return new_folder
        except Exception as e:
            print(f"Error creating '{new_folder}' folder: {e}\n")
            return None

    def copy(self, src: str = 'csv', dest: str = 'tmp'):
        source = os.path.join(self.root, src)
        destination = os.path.join(self.root, dest)
        try:
            shutil.copytree(source, destination)
            print(f"Files copied into new folder at:\n{os.path.basename(destination)}\n")
            return
        except Exception as e:
            print(f"Error copying '{src}' to '{dest}': {e}\n")
            return

    def remove(self, folder: str):
        target = os.path.join(self.root, folder)
        try:
            shutil.rmtree(target)
            # shutil.rmtree() works on directories, given an absolute path.
            # os.remove() works in files, given an absolute path.
            print(f"Folder deleted:\n{folder}\n")

        except Exception as e:
            print(f"Error deleting '{folder}' folder: {e}\n")