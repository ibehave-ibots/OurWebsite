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
    output_path: Path
    copyfun: Callable[[str, str], None] = shutil.copyfile
    hashfun: Callable[[bytes], HASH] = hashlib.md5


    def asset(self, path: str) -> str:
        path = PurePosixPath(path)
        hash_str = self.hashfun(Path(path).read_bytes()).hexdigest()[:6]
        fname_out = path.with_stem(path.stem + '_' + hash_str).name
        save_path = self.output_path.joinpath(fname_out)
        self.copyfun(str(PurePosixPath(path)), str(PurePosixPath(save_path)))
        relative_asset_path = self.output_path.relative_to(self.webserver_root)
        return str(PurePosixPath('/').joinpath(relative_asset_path).joinpath(fname_out))
    

        # orig_path = path
        # path = Path(path)
        # if 'http' in orig_path:
        #     src_path = orig_path
        #     target_path = self.build_basedir.joinpath('assets_external').joinpath(orig_path[orig_path.index('//') + 2:])
        #     output_path = '/' + str(PurePosixPath(target_path.relative_to(self.build_basedir)))
        #     method = 'download'
        # elif PurePosixPath(path).is_absolute():
        #     src_path = self.shared_static_dir.joinpath(orig_path.lstrip('/'))
        #     target_path = self.build_static_basedir.joinpath(orig_path.lstrip('/'))
        #     output_path = orig_path
        #     method = 'copy'
        #     assert src_path.exists()
        # else:
        #     src_path = Path(self.template_dir).joinpath(path)
        #     target_path = self.build_basedir.joinpath(Path(self.template_dir).relative_to(self.src_basedir)).joinpath(path)
        #     output_path = orig_path
        #     method = 'copy'
        #     assert src_path.exists()
            
        # if not target_path.exists():
        #     target_path.parent.mkdir(parents=True, exist_ok=True)
        #     if method == 'download':
        #         urllib.request.urlretrieve(src_path, target_path)
        #     elif method == 'copy':
        #         shutil.copyfile(src_path, target_path)
        # self._assetized.add(output_path)
        # return output_path
    
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
        
