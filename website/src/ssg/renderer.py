from __future__ import annotations

from datetime import date, datetime
from pathlib import Path, PurePosixPath
import shutil

import markdown2
import yaml

from .templates import JinjaRenderer
from .data import extract_global_data
from .utils import copydir, writefile, rmdir
from . import filters


def copy_static():
    rmdir("./_output/static")
    copydir(src="./themes/Silicon/assets", target="./_output/assets")
    


def run_render_pipeline():
    if not Path('./_output').exists():
        copy_static()
    copydir(src="./pages/_static", target="./_output/static")
        

    renderer = JinjaRenderer.from_path(
        templates_dir='./pages', 
        filters={
            'resize': filters.redirect_path('./_output')(filters.resize_image), 
            'flatten_nested': filters.flatten_nested_dict,
            'promote_key': filters.promote_key,
            'items': filters.items,
            'index': filters.multi_index,
            'sort_by': filters.sort_by,
            'download': filters.redirect_path('./_output', arg_idx=1)(filters.download),  
            'copy_to': filters.redirect_path('./_output', arg_idx=1)(filters.copy_to),
            'prepend': filters.prepend,
            'getfile': filters.transfer_file,
        },
        globals={
            'today': date.today(),
            'now': datetime.now(),
            'str': str,
        },
    )
    

    ## Get Data from './data'
    global_data = extract_global_data(base_path='./data')

    ## Render Jinja and load yaml files from './templates/data'
    site_data = {}
    for path in Path('./pages/_data').glob('*.yaml'):
        yaml_text = renderer.render_in_place(template_text=path.read_text(), data=global_data)
        site_data[path.stem] = yaml.load(yaml_text, Loader=yaml.Loader)

    ## Render Each Page to HTML and write to './output'
    urls_written = {}  # stores the url paths created, and by what page path
    for renderfile_path in Path('./pages').glob('[!_]*/_render.yaml'):
        
        render_data = yaml.load(renderer.render_in_place(template_text=renderfile_path.read_text(), data=global_data), yaml.Loader)
        page_path = renderfile_path.parent


        page_data = {}
        for key, fname in render_data.get('data', {}).items():
            path = page_path.joinpath(fname)
            if not path.exists():
                raise FileNotFoundError(path)
            if Path(fname).suffix == '.yaml':
                page_data[key] = yaml.load(renderer.render_in_place(template_text=path.read_text(), data=global_data), yaml.Loader)
            elif Path(fname).suffix == '.md':
                page_data[key] = markdown2.Markdown().convert(path.read_text())
            else:
                raise NotImplementedError(f"{path.suffix} extension not yet supported.  Try '.yaml' or '.md' .")
            
        for src, target in render_data.get('files', {}).items():
            src: str
            target: str
            src_path = page_path.joinpath(src)
            if not src_path.exists():
                raise FileNotFoundError(f"Could not find file {src_path}.")
            if target.startswith('/'):
                target = target[1:]
            target_path = Path('./_output') / Path(target)
            print(f'Copying File: {src_path} -> {target_path}')
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src=src_path, dst=target_path)


        for page in render_data.get('pages', []):

            assert page['url'].startswith('/'), f"Page URLS must be absolute paths.  Try {'/' + page['url']}"

            # used for finding macros that are relative to the page template
            renderer.vars['TEMPLATE_DIR'] = str(PurePosixPath(renderfile_path.parent.relative_to(Path('./pages'))))
            # renderer.vars['PAGE_PATH'] = str(PurePosixPath(renderfile_path.parent))
            # renderer.vars['OUTPUT_PATH'] = str(PurePosixPath('./_output'))
            
            page_html = renderer.render_named_template(
                template_path=page_path.joinpath(render_data['template']), 
                data=global_data, 
                page=page_data | page,
                site=site_data,
            )

            # Check that we're not overwriting a url that was already made--it's confusing to debug.
            url_to_write = page['url']
            if url_to_write in urls_written:
                raise FileExistsError(f"{str(renderfile_path)} tried to overwrite {url_to_write}, already made by {str(urls_written[url_to_write])}")
            else:
                urls_written[url_to_write] = renderfile_path
            
            # Write the html file
            writefile(path=url_to_write, text=page_html, basedir='./_output')


        
