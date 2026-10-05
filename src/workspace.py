from .extensions import *

class ProjectWorkspace(Extensions):
    def __init__(self, main_dir: str):
        super().__init__()
        self.root = self.get_project_root(main_dir)
