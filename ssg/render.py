from __future__ import annotations

from functools import lru_cache
from pprint import pprint
from typing import Any, Callable, Iterable, NamedTuple
import html
from pathlib import Path

import jinja2


import shutil
import os

from .collections import extract_data
from .utils import rmdir, redirect_path
from .image_processing import resize_image
from .parsers import Content



class Renderer(NamedTuple):
    content_path: Path
    template_path: Path
    output_dir: Path
    data_dir: Path
    filters: dict

    @classmethod
    def from_dirs(cls, content_dir, templates_dir, output_dir, data_dir, filters: dict[str, Callable[[str,], str]] = None) -> Iterable[Renderer]:
        
        for content_path in Path(content_dir).glob('*.md'):
            templates_dir = Path(templates_dir)
            template_path = templates_dir / content_path.with_suffix('.html').name
            assert templates_dir.exists()
                 
            yield Renderer(
                content_path = content_path,
                template_path = template_path,
                output_dir = Path(output_dir),
                data_dir = Path(data_dir),
                filters = filters if filters else {},
            )

    @property
    def output_path(self) -> Path:
        return self.output_dir / self.content_path.with_suffix('.html').name
    
    def _get_template(self) -> jinja2.Template:
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_path.parent),
            autoescape=jinja2.select_autoescape()
        )
        for name, fun in self.filters.items():
            env.filters[name] = redirect_path(self.output_dir)(fun)

        template = env.get_template(self.template_path.name)
        return template
    
    def _extract_data(self) -> dict:
        """Extract data from content file (both yaml and markdown) and yaml data collections."""
        content = Content.from_path(self.content_path)
        collections_data = extract_data(self.data_dir)
        data = {} | content.data | collections_data | {'content': content.html}
        return data
    

    def render(self) -> str:
        """Create the rendered html."""
        data = self._extract_data()
        template = self._get_template()
        html = template.render(**data)
        return html
    


def run_render_pipeline():

    rmdir("output/static")
    if Path('static').exists():
        shutil.copytree("static", "output/static")


    renderers = list(Renderer.from_dirs(
        content_dir='./pages', 
        templates_dir='./templates', 
        output_dir='./output', 
        data_dir='./data',
    ))
    for renderer in renderers:
        rendered_html = renderer.render()
        renderer.output_path.parent.mkdir(exist_ok=True, parents=True)
        renderer.output_path.write_text(rendered_html)
        


    

if __name__ == '__main__':
    run_render_pipeline()

