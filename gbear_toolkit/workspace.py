from .extensions import *

class ProjectWorkspace(Extensions):
    def __init__(self, main_dir: str):
        super().__init__()
        
        self.root = self.get_project_root(main_dir)
        if self.root is None:
            raise FileNotFoundError(f"Could not find a '{main_dir}' folder at or above {os.getcwd()}")

