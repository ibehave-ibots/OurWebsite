from pathlib import Path, PurePosixPath
import pytest
from . import files
from unittest.mock import Mock
from hashlib import md5
from _hashlib import HASH


def test_asset_creates_hashed_asset_in_assets_dir(tmp_path_factory):
    asset_path = tmp_path_factory.mktemp('assets')
    webserver_root = tmp_path_factory.mktemp('output')
    output_path = webserver_root / 'static'
    
    hashfun = Mock(HASH)
    hashfun().hexdigest.return_value = 'ABCDEFGHIJKLMNOPQ'
    

    data_file = asset_path.joinpath('data.file')
    data_file.touch()
    
    copyfun = Mock()
    manager = files.ImageAssetManager(
        webserver_root=webserver_root, 
        output_path=output_path, 
        copyfun=copyfun,
        hashfun=hashfun,
    )
    
    webserver_path = manager.asset(data_file)
    assert webserver_path == '/static/data_ABCDEF.file'
    copyfun.assert_called_once_with(
        str(PurePosixPath(data_file)),
        str(PurePosixPath(output_path).joinpath('data_ABCDEF.file')),
    )




    
