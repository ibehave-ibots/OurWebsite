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
class ImageAssetManager:
    webserver_root: Path
    asset_path: Path
    copyfun: Callable[[str, str], None] = shutil.copyfile
    downloadfun: Callable[[str, str], None] = urllib.request.urlretrieve
    hashfun: Callable[[bytes], HASH] = hashlib.md5



    def asset(self, path: str | Path) -> str:
        is_url = str(path).startswith('http')
        to_hash = path.encode() if is_url else Path(path).read_bytes()        
        hash_str = self.hashfun(to_hash).hexdigest()[:6]
        fname_out = Path(path).with_stem(Path(path).stem + '_' + hash_str).name
        save_path = self.asset_path.joinpath(fname_out)
        
        savefun = self.downloadfun if is_url else self.copyfun
        src = str(path if is_url else PurePosixPath(path))
        savefun(src, str(PurePosixPath(save_path)))
        relative_asset_path = self.asset_path.relative_to(self.webserver_root)
        return str(PurePosixPath('/').joinpath(relative_asset_path).joinpath(fname_out))
    

    
    def resize(self, path, width: int, height: int) -> str:
        ...
        # orig_path = path
        # path = Path(path)
        # if orig_path not in self._assetized:
        #     raise ValueError(f"{path} must be assetized before resizing.  Call the `asset` filter first.")
        # if PurePosixPath(path).is_absolute():
        #     src_path = self.build_basedir.joinpath(orig_path.lstrip('/'))
            
        # else:
        #     src_path = self.build_basedir.joinpath(Path(self.template_dir).relative_to(self.src_basedir)).joinpath(path)
        
        # with Image.open(src_path) as img:
        #     img2 = img.resize((width, height))

        # new_stem = path.stem + f"_{width}x{height}"
        # target_path = src_path.with_stem(new_stem)
        # img2.save(target_path)
        # return str(PurePosixPath(orig_path).with_stem(new_stem))
        
