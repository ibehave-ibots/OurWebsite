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
    for page_path in Path('./pages').glob('*.md'):
        
        
        frontmatter_data = {'data': global_data}
        page_data = render_frontmatter(renderer=renderer, page_path=page_path, **frontmatter_data)
        content_html = render_content_to_html(renderer=renderer, page_path=page_path)
        
        page_html = renderer.render_named_template(
            template_name=page_path.stem + '.html', 
            data=global_data, 
            page=page_data,
            content=content_html,
            site=site_data,
        )     

        save_path = Path('./output').joinpath(page_path.stem + '.html')
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_text(page_html)   
        
        
    for group_index_path in Path('./pages').glob('*/index.md'):
        frontmatter_data = {'data': global_data}
        page_data = render_frontmatter(renderer=renderer, page_path=group_index_path, **frontmatter_data)
        content_html = render_content_to_html(renderer=renderer, page_path=group_index_path)

        page_html = renderer.render_named_template(
            template_name=f"{group_index_path.parent.name}/index.html", 
            data=global_data, 
            page=page_data,
            content=content_html,
            site=site_data,
        )

        rel_path = group_index_path.relative_to('./pages')
        save_path = Path('./output').joinpath(rel_path.with_suffix('.html'))
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_text(page_html)

        for p in page_data['_pages']:
            frontmatter_data = {'data': global_data}
            page_data = render_frontmatter(
                renderer=renderer, 
                page_path=group_index_path.with_name('item.yaml'), 
                data=global_data,
                page=p,
            )
            page_data.update(p)

            page_html = renderer.render_named_template(
                template_name=f"{group_index_path.parent.name}/item.html", 
                data=global_data, 
                page=page_data,
                site=site_data,
            )
            rel_path = group_index_path.relative_to('./pages')
            save_path = Path('./output').joinpath(group_index_path.parent.name).joinpath(f"{p['id']}.html")
            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path.write_text(page_html)

            
    
        
