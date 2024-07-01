import os
from ssg.data import extract_global_data
import pytest

def test_find_single_file(tmp_path):
    fname = "dogs.yaml"
    yaml = """
    a: 3
    b: 5
    """
    tmp_path.joinpath(fname).write_text(yaml)

    data = extract_global_data(tmp_path)
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

    data = extract_global_data(tmp_path)
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

    data = extract_global_data(tmp_path)
    assert data['animals']['cats']['a'] == 3
    assert data['animals']['cats']['b'] == 5
    assert data['animals']['bees']['e'] == 3
    assert data['animals']['bees']['f'] == 5



def test_double_nested_file(tmp_path):
    fname = "animals/dogs/pug.yaml"
    yaml = """
    a: 3
    b: 5
    """
    path = tmp_path.joinpath(fname)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml)

    fname = "animals/dogs/pom.yaml"
    yaml = """
    a: 13
    b: 15
    """
    path = tmp_path.joinpath(fname)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml)

    data = extract_global_data(tmp_path)
    assert data['animals']['dogs']['pug']['a'] == 3
    assert data['animals']['dogs']['pug']['b'] == 5
    assert data['animals']['dogs']['pom']['a'] == 13
    assert data['animals']['dogs']['pom']['b'] == 15



def test_doesnt_supported_triple_nested_files(tmp_path):
    fname = "animals/dogs/breeds/pug.yaml"
    yaml = """
    a: 3
    b: 5
    """
    path = tmp_path.joinpath(fname)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml)

    with pytest.raises(NotImplementedError):
        extract_global_data(tmp_path)
        


def test_gets_path_of_image_files(tmp_path):
    
    # create a folder with an image in it.
    fname = "animals/dog/dog.jpg"
    path = tmp_path / fname
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)

    fname = "animals/cat/image.png"
    path = tmp_path / fname
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)

    data = extract_global_data(tmp_path)
    assert data['animals']['dog']['dog'] == 'animals/dog/dog.jpg'
    assert data['animals']['cat']['image'] == 'animals/cat/image.png'


def test_gets_path_of_image_files_with_relative_paths(tmp_path):
    
    # create a folder with an image in it.
    fname = "animals/dog/dog.jpg"
    path = tmp_path / fname
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)

    os.chdir(tmp_path)
    data = extract_global_data(tmp_path)
    assert data['animals']['dog']['dog'] == 'animals/dog/dog.jpg'