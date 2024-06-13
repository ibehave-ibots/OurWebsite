from pathlib import Path
from typing import Any

import markdown2

from .templates import JinjaRenderer
from . import utils


## YAML Frontmatter ##

def parse_jinja_yaml_frontmatter(renderer: JinjaRenderer, page_path: Path, **render_data) -> dict:
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


