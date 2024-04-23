from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime
from pathlib import Path


from .templates import JinjaRenderer
from .data import extract_global_data
from .utils import copydir, write_text
from .filters import redirect_path, resize_image
from .pages import find_pages, render_content_to_html, get_page_collection, render_frontmatter, update_pages_data


def run_render_pipeline():

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

    ## Get All Pages except collection _index.md files from './pages'
    render_data = {'data': global_data}
    pages_data = defaultdict(dict)
    page_path: Path
    for page_path in find_pages('./pages'):
        if page_path.name not in ['_index.md']:
            page_data = render_frontmatter(renderer=renderer, page_path=page_path, **render_data)
            collection_name = get_page_collection(base_path='./pages', md_path=page_path)
            pages_data = update_pages_data(pages_data, collection_name=collection_name, page_name=page_path.name, page_data=page_data)
    pages_data = dict(pages_data)

    ## Render Each Page to HTML and write to './output'
    for page_path in find_pages('./pages'):
        
        render_data = {'data': global_data}
        if page_path.name in ['_index.md']:
            render_data['pages'] = pages_data

        page_data = render_frontmatter(renderer=renderer, page_path=page_path, **render_data)
        render_data['page'] = page_data
        content_html = render_content_to_html(renderer=renderer, page_path=page_path, **render_data)
        
        # Build HTML Page
        collection_name = get_page_collection(base_path='./pages', md_path=page_path)
        template_name, rel_output_path = _get_template_name_and_output_path(collection_name=collection_name, md_name=page_path.name)
        
        page_html = renderer.render_named_template(
            template_name=template_name,
            **{
                'data': global_data,
                'content': content_html,
                'page': page_data,
                'pages': pages_data
            },
        )        
        write_text(base_dir='./output', file_path=rel_output_path, text=page_html)

    copydir(src="./static", target="./output/static")





def _get_template_name_and_output_path(collection_name: str | None, md_name: str) -> tuple[str, Path]:
    match collection_name, md_name:
        case None, '_index.md': 
            return ("index.html", Path('index.html'))
        case None, md:
            return (Path(md).with_suffix('.html').name, Path(md).with_suffix('.html').name)
        case coll, '_index.md': 
            return (f"{coll}.html", Path(coll) / 'index.html')
        case coll, md:
            assert coll[-1] == 's', "collection names should end with an s, dumb rule I know but here we are."
            return (f"{coll[:-1]}.html", Path(coll) / Path(md).with_suffix('.html').name)