from ssg.renderer import Renderer


def test_render_correct_paths_from_project(tmp_path):
    paths_in = [
        'pages/index.md',
        'templates/index.html',
    ]
    for path in paths_in:
        (tmp_path / path).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / path).touch()

    renderers = list(Renderer.from_dirs(
         content_dir=tmp_path / 'pages',
         templates_dir=tmp_path / 'templates',
         output_dir=tmp_path / 'output',
         data_dir=tmp_path / 'data',
    ))
    assert len(renderers) == 1

    renderers[0].render()
    assert (tmp_path / 'output/index.html').exists(), tmp_path


def test_render_correct_paths_from_project2(tmp_path):
    paths_in = [
        'pages/index.md',
        'pages/bb.md',
        'templates/index.html',
        'templates/bb.html',
        'templates/dummy.html',
    ]
    for path in paths_in:
        (tmp_path / path).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / path).touch()

    renderers = list(Renderer.from_dirs(
         content_dir=tmp_path / 'pages',
         templates_dir=tmp_path / 'templates',
         output_dir=tmp_path / 'output',
         data_dir=tmp_path / 'data',
    ))
    assert len(renderers) == 2

    for renderer in renderers:
        renderer.render()
    assert (tmp_path / 'output/index.html').exists(), tmp_path
    assert (tmp_path / 'output/bb.html').exists(), tmp_path


