from pathlib import Path
import shutil
from warnings import warn

import yaml


def rmdir(start_directory: Path):
    """Recursively and permanently removes the specified directory, all of its
    subdirectories, and every file contained in any of those folders."""
    
    start_directory = Path(start_directory)
    
    if not start_directory.exists():
        return

    # walk through everything, deleting all the files
    for path, dirnames, filenames in start_directory.walk(top_down=False):
        for filename in filenames:
            path.joinpath(filename).unlink()

    # walk through everything again, deleting all the folders
    for path, dirnames, filenames in start_directory.walk(top_down=False):
        assert len(filenames) == 0 # all files should be already deleted.
        try:
            path.rmdir()
        except PermissionError:
            warn(f"permission denied for {str(path)}. Continuing anyway...")

        


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


