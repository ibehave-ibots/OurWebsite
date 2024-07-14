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
    downloadfun = Mock()
    manager = files.ImageAssetManager(
        webserver_root=webserver_root, 
        asset_path=output_path, 
        copyfun=copyfun,
        downloadfun=downloadfun,
        hashfun=hashfun,
    )
    
    webserver_path = manager.asset(data_file)
    assert webserver_path == '/static/data_ABCDEF.file'
    copyfun.assert_called_once_with(
        str(PurePosixPath(data_file)),
        str(PurePosixPath(output_path).joinpath('data_ABCDEF.file')),
    )
    downloadfun.assert_not_called()


def test_downloaded_assets_create_hashed_asset_in_assets_dir_using_url(tmp_path_factory):
    asset_path = tmp_path_factory.mktemp('assets')
    webserver_root = tmp_path_factory.mktemp('output')
    output_path = webserver_root / 'static'

    hashfun = Mock(HASH)
    hashfun().hexdigest.return_value = 'ABCDEFGHIJKLMNOPQ'

    downloadfun = Mock()
    copyfun = Mock()
    
    
    manager = files.ImageAssetManager(
        webserver_root=webserver_root, 
        asset_path=output_path, 
        downloadfun=downloadfun,
        copyfun=copyfun,
        hashfun=hashfun,
    )
    url = 'http://website.com/dafadflkj/image.jpg'
    webserver_path = manager.asset(url)
    assert webserver_path == '/static/image_ABCDEF.jpg'
    
    downloadfun.assert_called_once_with(
        url,
        str(PurePosixPath(output_path).joinpath('image_ABCDEF.jpg'))
    )
    copyfun.assert_not_called()

    
