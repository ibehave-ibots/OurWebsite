from __future__ import annotations

from pathlib import Path, PurePosixPath
import shutil
from typing import Any

import markdown2
import yaml

from .templates.jinja_renderer import JinjaRenderer
from .data_directory import extract_global_data


def copy_static(src, target):
    shutil.copytree(src, target, dirs_exist_ok=True)
    
def run_render_pipeline():
        
    renderer = JinjaRenderer.from_path(templates_dir='./pages')
    
    ## Get Data from './data'
    global_data = extract_global_data(base_path='./data')

    ## Render Jinja and load yaml files from './templates/data'
    site_data = {}
    for path in Path('./pages/_data').glob('*.yaml'):
        yaml_text = renderer.render_in_place(template_text=path.read_text(), data=global_data)
        site_data[path.stem] = yaml.load(yaml_text, Loader=yaml.Loader)

    ## Render Each Page to HTML and write to './output'
    for renderfile_path in Path('./pages').glob('[!_]*/_render.yaml'):
        
        renderer.vars['TEMPLATE_DIR'] = str(PurePosixPath(renderfile_path.parent.relative_to(Path('./pages'))))   # used for finding jinja macros and blocks that are relative to the page template
        
        render_data = yaml.load(renderer.render_in_place(template_text=renderfile_path.read_text(), data=global_data), yaml.Loader)
        page_path = renderfile_path.parent
            
        _copy_files(file_destinations=render_data.get('files', {}), basedir=page_path)

        paths_written = []
        for page in render_data.get('pages', []):
            url: str = page['url']
            assert url.startswith('/'), f"Page URLS must be absolute paths.  Try {'/' + url}"

            data_fnames: dict[str, str] = render_data.get('data', {})
            page_data = page
            if data_fnames:
                data_dir = page_path.joinpath(page['folder']) if 'folder' in page else page_path
                page_data |= _read_page_data(data_dir=data_dir, data_fnames=data_fnames, renderer=renderer, **global_data)

            page_html = renderer.render_named_template(
                template_path=page_path.joinpath(render_data['template']), 
                data=global_data, 
                page=page_data,
                site=site_data,
            )

            # Write the html file
            url = url[1:] if url.startswith('/') else url
            url_path = Path('./_output').joinpath(url)
            if url_path in paths_written:
                raise FileExistsError()
            url_path.parent.mkdir(parents=True, exist_ok=True)
            print(f"Writing: {url_path}")
            url_path.write_text(page_html)
            paths_written.append(url_path)


def _copy_files(file_destinations: dict[str, str], basedir: Path) -> None:
    basedir = Path(basedir)
    for src, target in file_destinations.items():
        src_path = basedir.joinpath(src)
        if not src_path.exists():
            raise FileNotFoundError(f"Could not find file {src_path}.")
        if target.startswith('/'):
            target = target[1:]
        target_path = Path('./_output') / Path(target)
        print(f'Copying File: {src_path} -> {target_path}')
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src=src_path, dst=target_path)


def _read_page_data(data_dir, data_fnames: dict[str, str], renderer, **render_data) -> dict[str, Any]:
    page_data: dict[str, Any] = {}
    for key, fname in data_fnames.items():
        path = data_dir.joinpath(fname)
        if not path.exists():
            raise FileNotFoundError(path)
        if Path(fname).suffix == '.yaml':
            page_data[key] = yaml.load(renderer.render_in_place(template_text=path.read_text(), data=render_data), yaml.Loader)
        elif Path(fname).suffix == '.md':
            page_data[key] = markdown2.Markdown().convert(path.read_text())
        else:
            raise NotImplementedError(f"{path.suffix} extension not yet supported.  Try '.yaml' or '.md' .")
    return page_data


        
