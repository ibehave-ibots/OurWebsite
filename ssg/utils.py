from pathlib import Path, PurePosixPath
import os

import yaml
import markdown2

def rmdir(start_directory: Path):
    """Recursively and permanently removes the specified directory, all of its
    subdirectories, and every file contained in any of those folders."""
    if not os.path.exists("output/static"):
        return
    linux_path = PurePosixPath(start_directory)
    os.system(f"rm -Rf {linux_path}")



def load_yaml(text: str):
    return yaml.load(text, Loader=yaml.Loader)    


def load_markdown(text: str):
    return markdown2.Markdown().convert(text)