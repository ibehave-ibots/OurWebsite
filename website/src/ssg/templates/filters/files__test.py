from pathlib import Path, PurePosixPath
import pytest
from . import files
from unittest.mock import Mock
from hashlib import md5
from _hashlib import HASH


@pytest.fixture
def manager(tmp_path_factory) -> files.ImageAssetManager:
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
    return manager



def test_asset_creates_hashed_asset_in_assets_dir(tmp_path, manager):
    data_file = tmp_path.joinpath('data.file')    
    data_file.touch()
    webserver_path = manager.asset(data_file)
    assert webserver_path == '/static/data_ABCDEF.file'
    manager.copyfun.assert_called_once_with(
        str(PurePosixPath(data_file)),
        str(PurePosixPath(manager.asset_path).joinpath('data_ABCDEF.file')),
    )
    manager.downloadfun.assert_not_called()


def test_downloaded_assets_create_hashed_asset_in_assets_dir_using_url(manager):
    
    url = 'http://website.com/dafadflkj/image.jpg'
    webserver_path = manager.asset(url)
    assert webserver_path == '/static/image_ABCDEF.jpg'
    
    manager.downloadfun.assert_called_once_with(
        url,
        str(PurePosixPath(manager.asset_path).joinpath('image_ABCDEF.jpg'))
    )
    
    manager.copyfun.assert_not_called()

    
