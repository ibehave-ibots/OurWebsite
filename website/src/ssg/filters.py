from pathlib import Path, PurePosixPath
from typing import Any, Collection, Iterable

from PIL import Image


def redirect_path(prepend_path):
    """
    Decorator that redirects the path onto the first argument of the function for internel use, but keeps
    the output path the same. 
    """
    def decorator(fun):
        def wrapper(path, *args, **kwargs):
            if str(path).startswith('/'):
                was_root = True
                path = path[1:]
            else:
                was_root = False
            new_path = Path(prepend_path).joinpath(path)
            output_path = fun(new_path, *args, **kwargs)
            new_path = str(PurePosixPath(Path(output_path).relative_to(prepend_path)))
            if was_root:
                new_path = '/' + new_path
            return new_path
        return wrapper
    return decorator



def resize_image(fname: str, res: tuple[int, int]) -> str:
    path = Path(fname)
    with Image.open(path) as img:
        img2 = img.resize(res)


    path2 = path.with_stem(path.stem + f"_{res[0]}x{res[1]}")
    img2.save(path2)

    return str(path2)

    

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


def sort_by[T: Iterable](data: T, attrs: list[int | str]) -> T:
    

    data_sorted = type(data)()
    sorted()