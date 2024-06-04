from ssg import utils


def test_remove_directory(tmp_path):

    # Setup a directory of files
    assert tmp_path
    tmp_path.joinpath('top').mkdir()
    tmp_path.joinpath('top/aa.txt').touch()
    assert tmp_path.joinpath('top/aa.txt').exists()
    tmp_path.joinpath('top/bb.txt').touch()
    assert tmp_path.joinpath('top/bb.txt').exists()
    tmp_path.joinpath('top/bottom').mkdir()
    tmp_path.joinpath('top/bottom/cc.txt').touch()
    assert tmp_path.joinpath('top/bottom/cc.txt').exists()

    tmp_path.joinpath('top/middle').mkdir()

    assert len(list(tmp_path.walk())) == 4  # 3 files created and 1 empty directory: 4 leaves
    assert tmp_path.joinpath('top').exists()


    # Delete the "top" directory
    utils.rmdir(tmp_path.joinpath('top'))

    # all files should be deleted, including the 'top' directory and its contents
    assert len(list(tmp_path.walk())) == 1, [print(el) for el in tmp_path.walk()]
    assert not tmp_path.joinpath('top').exists()
    
    # parent directory shouldn't have been affected.
    assert tmp_path.exists() 