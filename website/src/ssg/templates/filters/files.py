import shutil
import urllib.request
from pathlib import Path, PurePosixPath

from PIL import Image


def redirect_path(prepend_path, arg_idx=0):
    """
    Decorator that redirects the path onto the first argument of the function for internel use, but keeps
    the output path the same. 
    """
    def decorator(fun):
        def wrapper(*args, **kwargs):
            path = args[arg_idx]
            if str(path).startswith('/'):
                was_root = True
                path = path[1:]
            else:
                was_root = False
            if 'http' in str(path):
                base_url = path[path.index('//') + 2:]
                new_path = str(PurePosixPath(prepend_path) / 'downloads' / base_url)
                Path(new_path).parent.mkdir(exist_ok=True, parents=True)
                print(f"Downloading File: {path} -> {new_path}")
                urllib.request.urlretrieve(path, new_path)
            else:
                new_path = str(PurePosixPath(prepend_path).joinpath(path))
            new_args = list(args)
            new_args[arg_idx] = new_path
            new_args = tuple(new_args)
            output_path = fun(*new_args, **kwargs)
            new_path = str(PurePosixPath(Path(output_path).relative_to(prepend_path)))
            if was_root:
                new_path = '/' + new_path
            return new_path
        return wrapper
    return decorator


def resize_image(fname: str, width: int, height: int) -> str:
    path = Path(fname)
    with Image.open(path) as img:
        img2 = img.resize((width, height))

    path2 = path.with_stem(path.stem + f"_{width}x{height}")
    img2.save(path2)
    return str(PurePosixPath(path2))


def prepend(path: str, base: str) -> str:
    if PurePosixPath(path).is_absolute() or Path(path).is_absolute():  # here we also use linux-style filenames in a windows environment.
        raise ValueError(f"absolute path {path} cannot be prepended.")

    new_path = PurePosixPath(base).joinpath(path)
    return str(new_path)


def copy_to(src: str, folder: str, fname: str = None) -> str:
    save_path = Path(folder)
    save_path /= fname if fname is not None else Path(src).name
    if not save_path.exists():
        save_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, folder)

    return str(PurePosixPath(save_path))

