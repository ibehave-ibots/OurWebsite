import pytest
from . import files


def test_path_prepend_decorator():
    
    class A:
        path = None

    def fun(path):
        A.path = path
        return path
    
    A.path = None
    new_fun = files.redirect_path('output')(fun)
    output = new_fun('aa/bb')
    assert A.path == 'output/aa/bb'
    assert output == 'aa/bb'

    A.path = None
    new_fun = files.redirect_path('ddd')(fun)
    output = new_fun('cc/bb')
    assert A.path == 'ddd/cc/bb'
    assert output == 'cc/bb'
    

def test_prepend():
    assert files.prepend('a/b', 'z') == 'z/a/b'

def test_prepend_does_not_work_on_absolute_paths():
    with pytest.raises(ValueError):
        files.prepend('/a/b', 'z')
