from pathlib import Path
from warnings import warn

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

    
