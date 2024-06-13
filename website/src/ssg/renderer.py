from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

import markdown2
import yaml

from .templates import JinjaRenderer
from .data import extract_global_data
from .utils import copydir, writefile
from .filters import redirect_path, resize_image, flatten_nested_dict, promote_key, items


def run_render_pipeline():
    copydir(src="./static", target="./_output/static")
    renderer = JinjaRenderer.from_path(
        templates_dir='./templates', 
        filters={
            'resize': redirect_path('./_output')(resize_image), 
            'flatten_nested': flatten_nested_dict,
            'promote_key': promote_key,
            'items': items,
        },
        globals={
            'today': date.today(),
            'now': datetime.now(),
        }
    )

    ## Get Data from './data'
    global_data = extract_global_data(base_path='./data')
    site_data = extract_global_data(base_path='./templates/data') # get data just used for the website, shouldn't be used in pages files

    ## Render Each Page to HTML and write to './output'
    for page_path in Path('./pages').glob('**/*'):
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
            page_html = renderer.render_named_template(
                template_name=rdata['template'], 
                data=global_data, 
                page=page_data | rdata,
                site=site_data,
            )
            writefile(path=rdata['url'], text=page_html, basedir='./_output')


        
