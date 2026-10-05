from util import *
import os


class ProjectWorkspace(CSV_Tools):
    def __init__(self, main_dir: str):
        self.root = self.get_project_root(main_dir)
        print('main!!!')
        print(self.root)


    def get_project_root(self, main_dir: str):
        current_directory = os.path.dirname(__file__)
        project_root = None
        while not project_root:
            directory_name = os.path.basename(current_directory)
            if main_dir == directory_name:
                project_root = current_directory
                return project_root
            
            if directory_name == '':
                print('Unable to find specified directory')
                return None
            
            else:
                current_directory = os.path.dirname(current_directory)
                continue


app = ProjectWorkspace('csv_tools')