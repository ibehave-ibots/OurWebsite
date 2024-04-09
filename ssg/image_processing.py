from PIL import Image
from pathlib import Path, PurePosixPath

from .utils import redirect_path



@redirect_path('output')
def resize_image(fname: str, res: tuple[int, int]) -> str:
    path = Path(fname)
    with Image.open(path) as img:
        img2 = img.resize(res)


    path2 = path.with_stem(path.stem + f"_{res[0]}x{res[1]}")
    img2.save(path2)

    return str(path2)



