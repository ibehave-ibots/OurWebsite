from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable, Iterable, NamedTuple
from pathlib import Path

import jinja2

from .data import extract_data
from .utils import copydir, rmdir, load_yaml, load_markdown
from .filters import redirect_path, resize_image



def find_pages(base_path: Path) -> Iterable[Path]:
    for path in Path(base_path).glob('**/*.md'):
        yield path


def read_frontmatter_text(md_path: Path) -> str:
    text = Path(md_path).read_text()
    *frontmatters, _ = text.split('---')
    frontmatter = frontmatters[0] if frontmatters else ''
    return frontmatter
    
def read_content_text(md_path: Path) -> str:
    text = Path(md_path).read_text()
    *_, md_text = text.split('---')
    content = md_text if md_text.strip() else ''
    return content
        

def render_in_place(template_text: str, env: jinja2.Environment = jinja2.Environment(), **data) -> str:
    rendered = env.from_string(template_text).render(**data)
    return rendered


def get_page_collection(base_path: Path, md_path: Path) -> str | None:
    rel_path = Path(md_path).relative_to(base_path)
    match rel_path.parts:
        case (): 
            raise ValueError("md_path must be a file inside base_path")
        case (name,): 
            return None
        case (coll, name): 
            return coll
        case _: 
            raise NotImplementedError("Multi-Nested collections not surrently supported")
    

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


def render_named_template(env: jinja2.Environment, template_name: str, **data) -> str:
    return env.get_template(template_name).render(**data)



def update_pages(pages: dict, collection_name: str, page_name: str, page_data: dict) -> dict:
    new_pages = pages.copy()
    name = Path(page_name).stem
    if collection_name:
        new_pages[collection_name][name] = page_data        
    else:
        new_pages[name] = page_data
    return new_pages
        

class HTMLRenderJob(NamedTuple):
    page_path: Path
    page_data: dict
    content_html: str


def extract_pages_data(env, data, pages_dir='./pages', ignore_names: list[str] = ['_index.md']):
    render_data = {'data': data}
    pages = defaultdict(dict)
    page_path: Path
    for page_path in find_pages(pages_dir):
        if page_path.name not in ignore_names:
            page_templated_yaml = read_frontmatter_text(page_path)
            if page_templated_yaml:
                page_yaml = render_in_place(env=env, template_text=page_templated_yaml, **render_data)
                page_data = load_yaml(page_yaml)
            else:
                page_data = {}
            collection_name = get_page_collection(base_path=pages_dir, md_path=page_path)
            pages = update_pages(pages, collection_name=collection_name, page_name=page_path.name, page_data=page_data)
    pages = dict(pages)
    return pages
        



def extract_page_and_content_data(env: jinja2.Environment, page_path: Path, data: dict, pages_data: dict, include_names = ['_index.md']) -> HTMLRenderJob:
        # Render YAML Frontmatter
        page_templated_yaml = read_frontmatter_text(page_path)
        render_data = {'data': data}
        if page_path.name in include_names:
            render_data['pages'] = pages_data
        page_yaml = render_in_place(env=env, template_text=page_templated_yaml, **render_data)

        # Load Frontmatter Data
        page_data = load_yaml(page_yaml)
        render_data['page'] = page_data

        # Render Markdown content
        page_templated_md = read_content_text(md_path=page_path)
        page_md = render_in_place(env=env,template_text=page_templated_md, **render_data)

        # Convert Markdown to HTML
        content_html = load_markdown(page_md)

        job = HTMLRenderJob(
            page_path=page_path,
            page_data=page_data,
            content_html=content_html
        )
        return job
        

def build_environment(template_dir: Path, filters: dict[str, Callable]) -> jinja2.Environment:
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        autoescape=jinja2.select_autoescape()
    )
    for name, fun in filters.items():
        env.filters[name] = fun
    return env


    

def run_render_pipeline():

    env = build_environment(
        template_dir='./templates', 
        filters={
            'resize': redirect_path('./output')(resize_image), 
        },
    )


    data = extract_data('./data')
    pages = extract_pages_data(env, data)
    copydir(src="./static", target="./output/static")
    
    
    for page_path in find_pages('./pages'):
        job: HTMLRenderJob = extract_page_and_content_data(env=env, page_path=page_path, data=data, pages_data=pages)
        
        # Build HTML Page
        collection_name = get_page_collection(base_path='./pages', md_path=job.page_path)
        template_name = get_template_name(collection_name=collection_name, md_name=job.page_path.name)

        render_data = {
            'data': data,
            'content': job.content_html,
            'page': job.page_data,
            'pages': pages
        }
        page_html = render_named_template(
            env=env, 
            template_name=template_name,
            **render_data
        )

        rel_output_path = get_relative_output_path(collection_name=collection_name, md_name=job.page_path.name)
        output_path = Path('./output').joinpath(rel_output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(page_html)







if __name__ == '__main__':
    run_render_pipeline()

