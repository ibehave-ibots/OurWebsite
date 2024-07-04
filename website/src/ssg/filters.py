import shutil
import urllib.request
from pathlib import Path, PurePosixPath
from typing import Any, Collection, Iterable, Literal

from PIL import Image
import validators


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

    

def flatten_nested_dict[K1, K2](nested_dict: dict[K1, dict[K2, Any]]) -> dict[tuple[K1, K2], Any]:
    out = {}
    for k1, d in nested_dict.items():
        for k2, value in d.items():
            out[k1, k2] = value
    return out



def promote_key[T: list[dict] | dict[str, dict]](data: T, key: str, attrs: list[int | str]) -> T:
    if isinstance(data, list):
        new_data = []
        for d in data:
            v = d.copy()
            for attr in attrs:
                v = v[attr]
            d[key] = v
            new_data.append(d)
        return new_data
    elif isinstance(data, dict):
        new_data = {}
        for k1, d in data.items():
            v = d.copy()
            for attr in attrs:
                v = v[attr]
            d[key] = v
            new_data[k1] = d
        return new_data
    else:
        raise NotImplementedError()


def items[K, V](data: dict[K, V]) -> list[tuple[K, V]]:
    return list(data.items())


def multi_index(data: Collection, indices: list[int | str]) -> Any:
    """Given a sequence of indices, returns the value from nested index from data."""
    get_code = ''.join([f"['{ind}']" if isinstance(ind, str) else f"[{ind}]" for ind in indices])
    value = eval("data" + get_code)
    return value


def sort_by[T](data: Iterable[T], indices: list[int | str], reverse: bool = False) -> list[T]:
    return type(data)(sorted(data, key=lambda d: multi_index(d, indices), reverse=reverse))




def prepend(path: str, base: str) -> str:
    if PurePosixPath(path).is_absolute() or Path(path).is_absolute():  # here we also use linux-style filenames in a windows environment.
        raise ValueError(f"absolute path {path} cannot be prepended.")
    
    new_path = PurePosixPath(base).joinpath(path)
    return str(new_path)
    



def download(src, folder: str, fname: str = None):
    
    save_path = Path(folder)
    save_path /= fname if fname is not None else Path(src).name
    if not save_path.exists():
        save_path.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(src, save_path ,)
    
    return str(PurePosixPath(save_path))
    

def copy_to(src: str, folder: str, fname: str = None) -> str:
    save_path = Path(folder)
    save_path /= fname if fname is not None else Path(src).name
    if not save_path.exists():
        save_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, folder)
    
    return str(PurePosixPath(save_path))



def transfer_file(src: str, folder: str, fname: str = None, download_fun=download, copy_fun=copy_to):
    if validators.url(src):
        return download_fun(src=src, folder=folder, fname=fname)
    else:
        return copy_fun(src=src, folder=folder, fname=fname)

