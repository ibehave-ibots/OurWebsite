from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import shutil
from typing import Callable
import typing
import urllib.request
from pathlib import Path, PurePosixPath
if typing.TYPE_CHECKING:
    from _hashlib import HASH

from PIL import Image

@dataclass(frozen=True)
class AssetManager:
    webserver_root: Path
    asset_path: Path
    copyfun: Callable[[str, str], None] = shutil.copyfile
    downloadfun: Callable[[str, str], None] = urllib.request.urlretrieve
    hashfun: Callable[[bytes], HASH] = hashlib.md5
    built_assets: set[str] = field(default_factory=set)

    def __post_init__(self):
        if not self.asset_path.is_relative_to(self.webserver_root):
            raise ValueError("asset_path must be inside webserver_path")
        self.asset_path.mkdir(parents=True, exist_ok=True)




    def build(self, path: str | Path) -> str:
        is_url = str(path).startswith('http')
        to_hash = path.encode() if is_url else Path(path).read_bytes()        
        hash_str = self.hashfun(to_hash).hexdigest()[:6]
        fname_out = Path(path).with_stem(Path(path).stem + '_' + hash_str).name
        save_path = str(PurePosixPath(self.asset_path.joinpath(fname_out)))
        
        savefun = self.downloadfun if is_url else self.copyfun
        src = str(path if is_url else PurePosixPath(path))
        savefun(src, save_path)
        self.built_assets.add(save_path)
        return save_path
    
    def get_uri(self, path: str | Path) -> str:
        assert str(PurePosixPath(path)) in self.built_assets
        assert Path(path).exists()
        assert Path(path).is_relative_to(self.webserver_root)
        webserver_path = Path(path).relative_to(self.webserver_root)
        return '/' + str(PurePosixPath(webserver_path))


    

    
def resize(path: str | Path, width: int, height: int) -> str:
    with Image.open(path) as img:
        img2 = img.resize((width, height))
    target_path = Path(path).with_stem(Path(path).stem + f'_{width}x{height}')
    img2.save(target_path)
    return str(PurePosixPath(target_path))


