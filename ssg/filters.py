from pathlib import Path, PurePosixPath

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

    

