from pathlib import Path
from typing import Any, Iterable

import markdown2

from .templates import JinjaRenderer
from . import utils


def find_pages(base_path: Path) -> Iterable[Path]:
    for path in Path(base_path).glob('**/*.md'):
        yield path


## YAML Frontmatter ##

def render_frontmatter(renderer: JinjaRenderer, page_path: Path, **render_data) -> dict:
    templated_yaml = _read_frontmatter_text(path=page_path)
    if not templated_yaml:
        return {}
    
    yaml = renderer.render_in_place(template_text=templated_yaml, **render_data)
    page_data = _load_frontmatter(yaml)
    return page_data


def _read_frontmatter_text(path: Path) -> str:
    text = Path(path).read_text()
    if path.suffix in ['.yaml', '.yml']:
        return text
    
    *frontmatters, _ = text.split('---')
    frontmatter = frontmatters[0] if frontmatters else ''
    return frontmatter


def _load_frontmatter(text: str) -> Any:
    return utils.load_yaml(text=text)


## Markdown Content ##

def render_content_to_html(renderer: JinjaRenderer, page_path: Path, **render_data) -> str:
    page_md = _read_content_text(md_path=page_path)
    content_html = _load_markdown(page_md)
    return content_html


def _read_content_text(md_path: Path) -> str:
    text = Path(md_path).read_text()
    *_, md_text = text.split('---')
    content = md_text if md_text.strip() else ''
    return content


def _load_markdown(text: str):
    return markdown2.Markdown().convert(text)


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


def update_pages_data(pages: dict, collection_name: str, page_name: str, page_data: dict) -> dict:
    new_pages = pages.copy()
    name = Path(page_name).stem
    if collection_name:
        new_pages[collection_name][name] = page_data
    else:
        new_pages[name] = page_data
    return new_pages





