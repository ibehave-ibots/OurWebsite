from pathlib import Path, PurePosixPath
from ssg import filters
from PIL.Image import Image as ImageType
from PIL import Image

def test_path_prepend_decorator():
    
    class A:
        path = None

    def fun(path):
        A.path = path
        return path
    
    A.path = None
    new_fun = filters.redirect_path('output')(fun)
    output = new_fun('aa/bb')
    assert A.path == 'output/aa/bb'
    assert output == 'aa/bb'

    A.path = None
    new_fun = filters.redirect_path('ddd')(fun)
    output = new_fun('cc/bb')
    assert A.path == 'ddd/cc/bb'
    assert output == 'cc/bb'
    

def test_flatten_dict_works():
    data = {
        'a': {
            1: True,
            2: False
        },
        'b': {
            3: 'Hi',
            10: 'Bye',
        }
    }
    observed = filters.flatten_nested_dict(data)
    expected = {
        ('a', 1): True,
        ('a', 2): False,
        ('b', 3): 'Hi',
        ('b', 10): 'Bye',
    }
    assert observed == expected

def test_items():
    data = {'a': 1, 'b': 'hi'}
    observed = filters.items(data)
    expected = [('a', 1), ('b', 'hi')]
    assert observed == expected

def test_promote_key_list_of_dicts():
    data = [
        {'A': {'a': 1, 'b': [10, 20, 30]}},
        {'A': {'a': 10, 'b': [100, 200, 300]}}
    ]
    observed = filters.promote_key(data, key='newkey', attrs=['A', 'b', 1])
    expected = [
        {'A': {'a': 1, 'b': [10, 20, 30]}, 'newkey': 20},
        {'A': {'a': 10, 'b': [100, 200, 300]}, 'newkey': 200},
    ]
    assert observed == expected


def test_promote_key_dict_of_dicts():
    data = {
        'first': {'A': {'a': 1, 'b': [10, 20, 30]}},
        'second': {'A': {'a': 10, 'b': [100, 200, 300]}}
    }
    observed = filters.promote_key(data, key='newkey', attrs=['A', 'b', 1])
    expected = {
        'first': {'A': {'a': 1, 'b': [10, 20, 30]}, 'newkey': 20},
        'second': {'A': {'a': 10, 'b': [100, 200, 300]}, 'newkey': 200},
    }
    assert observed == expected


def test_multi_index():
    data = {'a': {'b': [10, 20, 30]}}
    observed = filters.multi_index(data, ['a', 'b', 1])
    expected = 20
    assert observed == expected


def test_sort_by():
    data = [
        (12, {'a': [4, {'A': 200, 'B': 200}]}),
        (65, {'a': [4, {'A': 50, 'B': 200}]}),
        (25, {'a': [4, {'A': 100, 'B': 200}]}),
    ]

    # A should be ascending
    observed = filters.sort_by(data, [1, 'a', 1, 'A'])
    expected = [
        (65, {'a': [4, {'A': 50, 'B': 200}]}),
        (25, {'a': [4, {'A': 100, 'B': 200}]}),
        (12, {'a': [4, {'A': 200, 'B': 200}]}),
    ]
    assert observed == expected

    # When reversed, A should be descending
    # A should be ascending
    observed = filters.sort_by(data, [1, 'a', 1, 'A'], reverse=True)
    expected = [
        (12, {'a': [4, {'A': 200, 'B': 200}]}),
        (25, {'a': [4, {'A': 100, 'B': 200}]}),
        (65, {'a': [4, {'A': 50, 'B': 200}]}),
    ]
    assert observed == expected
    

def test_download_filter(tmp_path):
    url = "https://i.natgeofe.com/n/4f5aaece-3300-41a4-b2a8-ed2708a0a27c/domestic-dog_thumb_square.jpg"
    fold = str(tmp_path)
    path = filters.download(url, folder=fold)
    assert isinstance(path, str)
    assert Path(path).exists()
    assert Path(path).name == 'domestic-dog_thumb_square.jpg'
    

def test_download_filter_creates_folder(tmp_path):
    url = "https://i.natgeofe.com/n/4f5aaece-3300-41a4-b2a8-ed2708a0a27c/domestic-dog_thumb_square.jpg"
    fold = str(tmp_path / 'images')
    assert not Path(fold).exists()
    path = filters.download(url, folder=fold)
    assert isinstance(path, str)
    assert Path(path).exists()
    assert Path(path).name == 'domestic-dog_thumb_square.jpg'



def test_imdownload2():
    url = "https://i.natgeofe.com/n/4f5aaece-3300-41a4-b2a8-ed2708a0a27c/domestic-dog_thumb_square.jpg"
    im = filters.download_image(url)
    assert isinstance(im, ImageType)


def test_save_image(tmp_path):
    img = Image.new('RGB', [500,500], (255, 128, 128))
    path = tmp_path / 'im.jpg'
    assert not path.exists()
    path2 = filters.save_image(img, str(PurePosixPath(path)))
    path2 = Path(path2)
    assert path.exists()
    assert path2.exists()
    assert path == path2
    img2 = Image.open(path2)
    assert img2.size == (500, 500)
    