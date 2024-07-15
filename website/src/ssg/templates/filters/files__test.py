from pathlib import Path, PurePosixPath
import pytest
from . import files
from unittest.mock import Mock
from hashlib import md5
from _hashlib import HASH
from PIL import Image
import numpy as np


@pytest.fixture
def manager(tmp_path_factory) -> files.AssetManager:
    asset_path = tmp_path_factory.mktemp('assets')
    webserver_root = tmp_path_factory.mktemp('output')
    output_path = webserver_root / 'static'
    
    hashfun = Mock(HASH)
    hashfun().hexdigest.return_value = 'ABCDEFGHIJKLMNOPQ'
    

    data_file = asset_path.joinpath('data.file')
    data_file.touch()
    
    copyfun = Mock()
    downloadfun = Mock()
    manager = files.AssetManager(
        webserver_root=webserver_root, 
        asset_path=output_path, 
        copyfun=copyfun,
        downloadfun=downloadfun,
        hashfun=hashfun,
    )
    return manager



def test_asset_creates_hashed_asset_in_assets_dir(tmp_path, manager: files.AssetManager):
    data_file = tmp_path.joinpath('data.file')    
    data_file.touch()
    output_path = manager.build(data_file)
    expected_output_path = str(PurePosixPath(manager.asset_path).joinpath('data_ABCDEF.file'))
    assert output_path == expected_output_path
    manager.copyfun.assert_called_once_with(
        str(PurePosixPath(data_file)),
        expected_output_path,
    )
    manager.downloadfun.assert_not_called()
    assert output_path in manager.built_assets


def test_downloaded_assets_create_hashed_asset_in_assets_dir_using_url(manager):    
    url = 'http://website.com/dafadflkj/image.jpg'
    output_path = manager.build(url)
    expected_output_path = str(PurePosixPath(manager.asset_path.joinpath('image_ABCDEF.jpg')))
    assert output_path == expected_output_path
    
    manager.downloadfun.assert_called_once_with(
        url,
        expected_output_path
    )
    manager.copyfun.assert_not_called()
    assert output_path in manager.built_assets

    

def test_get_webserver_path_from_built_file(manager):
    filepath = manager.asset_path.joinpath('myfile.png')
    filepath.touch()
    filepath_str = str(PurePosixPath(filepath))
    manager.built_assets.add(filepath_str)
    uri = manager.get_uri(filepath_str)
    expected_uri = '/static/myfile.png'
    assert uri == expected_uri


# def test_image_resize(tmp_path):
    
#     im = Image.fromarray(np.zeros((120, 240, 3), np.uint8))
#     im.save(tmp_path / 'image.jpg')

#     fpath = str(PurePosixPath(tmp_path / 'image.jpg'))
#     fpath_out = files.resize(fpath, 60, 120)
#     assert fpath_out == str(PurePosixPath(tmp_path / 'image_60x120.jpg'))
