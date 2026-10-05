from .project_paths import ProjectPaths
from .folder_ops import FolderOps
from .csv_processor import CsvProcessor

class Extensions(ProjectPaths, FolderOps, CsvProcessor):
    pass

__all__ = ['ProjectPaths', 'FolderOps', 'CsvProcessor', 'Extensions']
