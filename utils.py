from pathlib import Path
from shutil import rmtree
import os

def rmdir(start_directory: Path):
    """Recursively and permanently removes the specified directory, all of its
    subdirectories, and every file contained in any of those folders."""
    # start_directory = Path(start_directory)
    # for path in start_directory.iterdir():
    #     if path.is_file():
    #         path.unlink()
    #     else:
    #         rmdir(path)
    # start_directory.rmdir()
    # top = Path(start_directory)
    # for root, dirs, files in top.walk(top_down=False):
    #     for name in files:
    #         (root / name).unlink()
    #     for name in dirs:
    #         rmtree(str(root / name))
            # (root / name).rmdir()
    # top.rmdir()
    linux_path = str(start_directory).replace('\\', '/')
    os.system(f"rm -Rf {linux_path}")

