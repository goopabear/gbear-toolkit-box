from .extensions import *

class ProjectWorkspace():
    def __init__(self, main_dir: str):
        self.path = ProjectPaths(main_dir)
        self.folder = FolderOps()
        self.data = DataStorage()



