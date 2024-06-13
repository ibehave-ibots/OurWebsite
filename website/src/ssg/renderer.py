from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

from .templates import JinjaRenderer
from .data import extract_global_data
from .utils import copydir, writefile
from .filters import redirect_path, resize_image
from .pages import parse_markdown_to_html, parse_jinja_yaml_frontmatter


def run_render_pipeline():
    copydir(src="./static", target="./_output/static")
    renderer = JinjaRenderer.from_path(
        templates_dir='./templates', 
        filters={
            'resize': redirect_path('./_output')(resize_image), 
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
    for page_path in Path('./pages').glob('**/*.*'):
        
        page_data = parse_jinja_yaml_frontmatter(renderer=renderer, page_path=page_path, data=global_data)
        if page_path.suffix == '.md':
            page_data['content'] = parse_markdown_to_html(page_path)
        
        template_name = page_data['_template']
        page_html = renderer.render_named_template(
            template_name=template_name, 
            data=global_data, 
            page=page_data,
            site=site_data,
        )
        writefile(path=template_name, text=page_html, basedir='./_output')

        if '_generate' in page_data:
            for page_type in page_data['_generate']:
                for p_data in page_type['pages']:
                    template_name = page_type['template']
                    page_html = renderer.render_named_template(
                        template_name=template_name, 
                        data=global_data, 
                        page=p_data,
                        site=site_data,
                    )
                    writefile(path=Path(template_name).with_stem(p_data['id']), text=page_html, basedir='./_output')
                    

        
