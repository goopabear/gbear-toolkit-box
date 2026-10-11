from .core import *

class Workspace():
    def __init__(self, main_dir: str):
        self.paths = PathResolver(main_dir)
        self.folders = FolderManager(self.paths.root)
        self.table = Table()



