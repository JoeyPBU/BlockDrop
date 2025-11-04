import sys, os

def resource_path(relative_path):
    """Used for PyInstaller - gets the paths to the files based on absolute and relative paths."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
