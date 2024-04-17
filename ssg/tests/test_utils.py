from pathlib import Path
from ssg import utils


def test_path_prepend_decorator():
    
    class A:
        path = None

    def fun(path):
        A.path = path
        return path
    
    A.path = None
    new_fun = utils.redirect_path('output')(fun)
    output = new_fun(Path('aa/bb'))
    assert A.path == Path('output/aa/bb')
    assert output == 'aa/bb'

    A.path = None
    new_fun = utils.redirect_path('ddd')(fun)
    output = new_fun(Path('cc/bb'))
    assert A.path == Path('ddd/cc/bb')
    assert output == 'cc/bb'
    


