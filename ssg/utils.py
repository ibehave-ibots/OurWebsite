from pathlib import Path, PurePosixPath
import os

import yaml
import markdown2
import shutil


def rmdir(start_directory: Path):
    """Recursively and permanently removes the specified directory, all of its
    subdirectories, and every file contained in any of those folders."""
    if not os.path.exists("output/static"):
        return
    linux_path = PurePosixPath(start_directory)
    os.system(f"rm -Rf {linux_path}")


def copydir(src: Path, target: Path) -> None:
    src = Path(src)
    target = Path(target)
    rmdir(target)
    shutil.copytree(src, target, dirs_exist_ok=True)
    

def write_text(base_dir: Path, file_path: Path, text: str) -> None:
    save_path = Path(base_dir).joinpath(file_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_text(text)
        

def load_yaml(text: str):
    return yaml.load(text, Loader=yaml.Loader)    


def load_markdown(text: str):
    return markdown2.Markdown().convert(text)