from .extensions import *



class ProjectWorkspace(Extensions):
    def __init__(self, main_dir: str):
        self.root = self.get_project_root(main_dir)
