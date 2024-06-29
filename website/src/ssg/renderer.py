from __future__ import annotations

from datetime import date, datetime
from pathlib import Path, PosixPath, PurePosixPath

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
    for yaml_path in Path('./pages/_data').glob('*.yaml'):
        yaml_text = renderer.render_in_place(template_text=yaml_path.read_text(), data=global_data)
        site_data[yaml_path.stem] = yaml.load(yaml_text, Loader=yaml.Loader)

    ## Render Each Page to HTML and write to './output'
    urls_written = {}  # stores the url paths created, and by what page path
    for page_path in Path('./pages').glob('[!_]*'):
        if not page_path.is_dir():
            continue
        
        page_data = {}
        for yaml_path in page_path.glob('*.yaml'):
            yaml_text = renderer.render_in_place(template_text=yaml_path.read_text(), data=global_data)
            page_data[yaml_path.stem] = yaml.load(yaml_text, Loader=yaml.Loader)

        for markdown_path in page_path.glob('*.md'):
            page_data[markdown_path.stem] = markdown2.Markdown().convert(markdown_path.read_text())
        
        render_data = page_data['_render']

        # support multiple pages rendered from the same file
        if isinstance(render_data, dict):
            render_data = [render_data]  
        assert isinstance(render_data, list)

        for rdata in render_data:
            assert rdata['url'].startswith('/'), f"Page URLS must be absolute.  Try {'/' + rdata['url']}"

            renderer.vars['TEMPLATE_DIR'] = str(PurePosixPath(page_path.relative_to(Path('./pages'))))
            page_html = renderer.render_named_template(
                template_name=f"{page_path.name}/{rdata['template']}", 
                data=global_data, 
                page=page_data | rdata,
                site=site_data,
            )

            # Check that we're not overwriting a url that was already made--it's confusing to debug.
            url_to_write = rdata['url']
            if url_to_write in urls_written:
                raise FileExistsError(f"{str(page_path)} tried to overwrite {url_to_write}, already made by {str(urls_written[url_to_write])}")
            else:
                urls_written[url_to_write] = page_path
            
            # Write the html file
            writefile(path=url_to_write, text=page_html, basedir='./_output')


        
