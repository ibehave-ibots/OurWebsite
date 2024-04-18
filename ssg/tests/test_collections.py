from ssg.collections import extract_data
import pytest

def test_find_single_file(tmp_path):
    fname = "dogs.yaml"
    yaml = """
    a: 3
    b: 5
    """
    tmp_path.joinpath(fname).write_text(yaml)

    data = extract_data(tmp_path)
    dogs = data['dogs']
    assert dogs['a'] == 3
    assert dogs['b'] == 5


def test_find_all_single_files(tmp_path):
    fname = "cats.yaml"
    yaml = """
    a: 3
    b: 5
    """
    tmp_path.joinpath(fname).write_text(yaml)

    fname = "birds.yaml"
    yaml = """
    d: 5
    e: hello
    """
    tmp_path.joinpath(fname).write_text(yaml)

    data = extract_data(tmp_path)
    assert data['cats']['a'] == 3
    assert data['cats']['b'] == 5
    assert data['birds']['d'] == 5
    assert data['birds']['e'] == "hello"


def test_find_single_nested_files(tmp_path):
    fname = "animals/cats.yaml"
    yaml = """
    a: 3
    b: 5
    """
    path = tmp_path.joinpath(fname)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml)

    fname = "animals/bees.yaml"
    yaml = """
    e: 3
    f: 5
    """
    path = tmp_path.joinpath(fname)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml)

    data = extract_data(tmp_path)
    assert data['animals']['cats']['a'] == 3
    assert data['animals']['cats']['b'] == 5
    assert data['animals']['bees']['e'] == 3
    assert data['animals']['bees']['f'] == 5



def test_doesnt_supported_multinested_files(tmp_path):
    fname = "animals/dogs/pug.yaml"
    yaml = """
    a: 3
    b: 5
    """
    path = tmp_path.joinpath(fname)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml)

    with pytest.raises(NotImplementedError):
        extract_data(tmp_path)
        

