import os
import tkinter as tk
from tkinter import filedialog

class PathResolver():
    def __init__(self, main_dir: str):
        self.root = self._find_root(main_dir)
        if self.root is None:
            raise FileNotFoundError(f"[ERROR] Could not find a '{main_dir}' folder at or above {os.getcwd()}")
    
    def _find_root(self, main_dir: str):
        current_directory = os.getcwd()
        project_root = None
        while not project_root:
            directory_name = os.path.basename(current_directory)
            if main_dir == directory_name:
                project_root = current_directory
                print(f"[INFO] Project root initialized at: {project_root}")
                return project_root
            if directory_name == '':
                print('[ERROR] Unable to find specified directory')
                return None
            else:
                current_directory = os.path.dirname(current_directory)
                continue

    def resolve(self, *parts):
        path = os.path.join(self.root, *parts)
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        return os.path.abspath(path)

    def ask_file(self):
        return self._ask(filedialog.askopenfilename, "Select a file")

    def ask_folder(self):
        return self._ask(filedialog.askdirectory, "Select a folder")

    def _ask(self, dialog, title: str):
        root = tk.Tk()
        root.title("Select")
        root.attributes('-alpha', 0.0)      # invisible, but still shows in taskbar
        root.attributes('-topmost', True)   # bring it to the front
        root.lift()
        root.focus_force()
        try:
            path = dialog(parent=root, title=title)
        finally:
            root.destroy()
        return os.path.abspath(path) if path else None


