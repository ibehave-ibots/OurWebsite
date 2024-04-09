from pathlib import Path, PurePosixPath
import os

def rmdir(start_directory: Path):
    """Recursively and permanently removes the specified directory, all of its
    subdirectories, and every file contained in any of those folders."""
    linux_path = PurePosixPath(start_directory)
    os.system(f"rm -Rf {linux_path}")


def redirect_path(prepend_path):
    """
    Decorator that redirects the path onto the first argument of the function for internel use, but keeps
    the output path the same. 
    """
    def decorator(fun):
        def wrapper(path, *args, **kwargs):
            new_path = Path(prepend_path).joinpath(path)
            output_path = fun(new_path, *args, **kwargs)
            return str(PurePosixPath(Path(output_path).relative_to(prepend_path)))
        return wrapper
    return decorator

