from pathlib import Path
from ssg import filters


def test_path_prepend_decorator():
    
    class A:
        path = None

    def fun(path):
        A.path = path
        return path
    
    A.path = None
    new_fun = filters.redirect_path('output')(fun)
    output = new_fun(Path('aa/bb'))
    assert A.path == Path('output/aa/bb')
    assert output == 'aa/bb'

    A.path = None
    new_fun = filters.redirect_path('ddd')(fun)
    output = new_fun(Path('cc/bb'))
    assert A.path == Path('ddd/cc/bb')
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
    observed = filters.flatten_dict(data)
    expected = [
        ('a', 1, True),
        ('a', 2, False),
        ('b', 3, 'Hi'),
        ('b', 10, 'Bye'),
    ]
    assert observed == expected