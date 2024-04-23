from __future__ import annotations

from collections import defaultdict
from typing import NamedTuple
from pathlib import Path

from ssg.pages import find_pages, get_page_collection, load_markdown, read_content_text, read_frontmatter_text, update_pages_data

from .templates import JinjaRenderer
from .data import extract_global_data
from .utils import copydir, load_yaml, write_text
from .filters import redirect_path, resize_image
from .pages import find_pages, read_content_text, read_frontmatter_text, get_page_collection, update_pages_data, load_markdown



def get_relative_output_path(collection_name: str | None, md_name: str) -> Path:
    if md_name[0] == '_':
        md_name = md_name[1:]
    html_name = str(Path(md_name).with_suffix('.html'))
    match collection_name, html_name:
        case None, _: 
            return Path(html_name)
        case '', _: 
            return Path(html_name)
        case _: 
            return Path(collection_name) / html_name
        

def get_template_name(collection_name: str | None, md_name: str) -> str:
    match collection_name, md_name:
        case None, _:
            return str(Path(md_name).with_suffix('.html'))
        case '', _: 
            return str(Path(md_name).with_suffix('.html'))
        case coll, '_index.md': 
            return f"{coll}.html"
        case coll, _:
            assert coll[-1] == 's', "collection names should start with s, dumb rule I know but here we are."
            return f"{coll[:-1]}.html"


class HTMLRenderJob(NamedTuple):
    page_path: Path
    page_data: dict
    content_html: str


def extract_pages_data(renderer: JinjaRenderer, data, pages_dir='./pages', ignore_names: list[str] = ['_index.md']):
    render_data = {'data': data}
    pages = defaultdict(dict)
    page_path: Path
    for page_path in find_pages(pages_dir):
        if page_path.name not in ignore_names:
            page_templated_yaml = read_frontmatter_text(page_path)
            if page_templated_yaml:
                page_yaml = renderer.render_in_place(template_text=page_templated_yaml, **render_data)
                page_data = load_yaml(page_yaml)
            else:
                page_data = {}
            collection_name = get_page_collection(base_path=pages_dir, md_path=page_path)
            pages = update_pages_data(pages, collection_name=collection_name, page_name=page_path.name, page_data=page_data)
    pages = dict(pages)
    return pages
        



def extract_page_and_content_data(renderer: JinjaRenderer, page_path: Path, data: dict, pages_data: dict, include_names = ['_index.md']) -> HTMLRenderJob:
        # Render YAML Frontmatter
        page_templated_yaml = read_frontmatter_text(page_path)
        render_data = {'data': data}
        if page_path.name in include_names:
            render_data['pages'] = pages_data
        page_yaml = renderer.render_in_place(template_text=page_templated_yaml, **render_data)

        # Load Frontmatter Data
        page_data = load_yaml(page_yaml)
        render_data['page'] = page_data

        # Render Markdown content
        page_templated_md = read_content_text(md_path=page_path)
        page_md = renderer.render_in_place(template_text=page_templated_md, **render_data)

        # Convert Markdown to HTML
        content_html = load_markdown(page_md)

        job = HTMLRenderJob(
            page_path=page_path,
            page_data=page_data,
            content_html=content_html
        )
        return job
        

def run_render_pipeline():

    renderer = JinjaRenderer.from_path(
        templates_dir='./templates', 
        filters={
            'resize': redirect_path('./output')(resize_image), 
        },
    )


    global_data = extract_global_data(base_path='./data')
    pages_data = extract_pages_data(renderer=renderer, data=global_data, pages_dir='./pages')   
    for page_path in find_pages('./pages'):
        job: HTMLRenderJob = extract_page_and_content_data(renderer=renderer, page_path=page_path, data=global_data, pages_data=pages_data)
        
        # Build HTML Page
        collection_name = get_page_collection(base_path='./pages', md_path=job.page_path)
        template_name = get_template_name(collection_name=collection_name, md_name=job.page_path.name)

        page_html = renderer.render_named_template(
            template_name=template_name,
            **{
                'data': global_data,
                'content': job.content_html,
                'page': job.page_data,
                'pages': pages_data
            },
        )
        rel_output_path = get_relative_output_path(collection_name=collection_name, md_name=job.page_path.name)
        
        write_text(base_dir='./output', file_path=rel_output_path, text=page_html)

    copydir(src="./static", target="./output/static")



