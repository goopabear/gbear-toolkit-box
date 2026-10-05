import os
import shutil

# User must pass the project folder name

class CSV_Tools():
    def __init__(self, main_dir: str = None):
        if main_dir is None:
            main_dir = os.path.basename(os.path.dirname((__file__)))

        self.root = self.get_project_root(main_dir)
        print(self.root)


    def get_project_root(self, main_dir: str):
        current_directory = os.path.dirname(__file__)
        project_root = None
        while not project_root:
            directory_name = os.path.basename(current_directory)
            if main_dir == directory_name:
                project_root = current_directory
                print(f"Project root found at: {project_root}")
                return project_root
            
            if directory_name == '':
                print('Unable to find specified directory')
                return None
            
            else:
                current_directory = os.path.dirname(current_directory)
                continue


    def copy_folder(self, src: str = 'csv', dest: str = 'tmp'):
        source = os.path.join(self.root, src)
        destination = os.path.join(self.root, dest)

        try:
            shutil.copytree(source, destination)
            print(f"Files copied into new folder at:\n{os.path.basename(destination)}\n")
            return

        except Exception as e:
            print(f"Error copying CSV files: {e}\n")
            return

    def delete_folder(self, folder: str):
        tmp_folder = os.path.join(self.root, folder) 
        # Relative path from root to "tmp"
        # Can include additional arguments as steps up
        try:
            shutil.rmtree(tmp_folder)
            # shutil.rmtree() works on directories, given an absolute path.
            # os.remove() works in files, given an absolute path.
            print("Setup Initialized:\n'tmp' folder deleted\n")

        except Exception as e:
            print(f"Error deleting 'tmp' folder: {e}\n")
