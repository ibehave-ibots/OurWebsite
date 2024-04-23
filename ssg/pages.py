from pathlib import Path
from typing import Any, Iterable

import markdown2

from .templates import JinjaRenderer
from . import utils


def find_pages(base_path: Path) -> Iterable[Path]:
    for path in Path(base_path).glob('**/*.md'):
        yield path


def read_frontmatter_text(md_path: Path) -> str:
    text = Path(md_path).read_text()
    *frontmatters, _ = text.split('---')
    frontmatter = frontmatters[0] if frontmatters else ''
    return frontmatter


def load_frontmatter(text: str) -> Any:
    return utils.load_yaml(text=text)


def render_frontmatter(renderer: JinjaRenderer, page_path: Path, **render_data) -> dict:
    templated_yaml = read_frontmatter_text(md_path=page_path)
    if not templated_yaml:
        return {}
    
    yaml = renderer.render_in_place(template_text=templated_yaml, **render_data)
    page_data = load_frontmatter(yaml)
    return page_data
    
        


def read_content_text(md_path: Path) -> str:
    text = Path(md_path).read_text()
    *_, md_text = text.split('---')
    content = md_text if md_text.strip() else ''
    return content


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



def load_markdown(text: str):
    return markdown2.Markdown().convert(text)

