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
    shutil.copytree(src, target, dirs_exist_ok=True)
    

        
def writefile(path: Path, text: str, basedir: Path = None) -> None:
    """Writes to a file and creates its parents."""

    # if path starts with '/', then it won't join with the base dir.  Remove the leading /.
    path = Path(path)
    if basedir and path.root:
        path = Path(str(path).replace(path.root, '', 1))
    path = Path(basedir).joinpath(path) if basedir else Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)   


def load_yaml(text: str):
    return yaml.load(text, Loader=yaml.Loader)    


