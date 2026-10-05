import os

# User must pass the project folder name

class ProjectPaths():
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



