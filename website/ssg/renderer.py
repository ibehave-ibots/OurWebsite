from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

from .templates import JinjaRenderer
from .data import extract_global_data
from .utils import copydir
from .filters import redirect_path, resize_image
from .pages import render_content_to_html, render_frontmatter


def run_render_pipeline():
    copydir(src="./static", target="./output/static")
    renderer = JinjaRenderer.from_path(
        templates_dir='./templates', 
        filters={
            'resize': redirect_path('./output')(resize_image), 
        },
        globals={
            'today': date.today(),
            'now': datetime.now(),
        }
    )

    ## Get Data from './data'
    global_data = extract_global_data(base_path='./data')
    site_data = extract_global_data(base_path='./templates/site') # get data just used for the website, shouldn't be used in pages files

    ## Render Each Page to HTML and write to './output'
    for page_path in Path('./pages').glob('**/*.*'):
        
        
        page_data = render_frontmatter(renderer=renderer, page_path=page_path, data=global_data)
        content_html = render_content_to_html(renderer=renderer, page_path=page_path) if page_path.suffix == '.md' else ''
        
        template_name = page_data['_template']
        page_html = renderer.render_named_template(
            template_name=template_name, 
            data=global_data, 
            page=page_data,
            content=content_html,
            site=site_data,
        )

        save_path = Path('./output').joinpath(template_name)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_text(page_html)   

        if '_generate' in page_data:
            for page_type in page_data['_generate']:
                for p_data in page_type['pages']:
                    template_name = page_type['template']
                    page_html = renderer.render_named_template(
                        template_name=template_name, 
                        data=global_data, 
                        page=p_data,
                        content=content_html,
                        site=site_data,
                    )
                    
                    save_path = Path('./output').joinpath(template_name).with_stem(p_data['id'])
                    
                    save_path.parent.mkdir(parents=True, exist_ok=True)
                    save_path.write_text(page_html) 
                    

        
