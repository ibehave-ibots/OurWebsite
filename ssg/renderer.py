from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable, Iterable, NamedTuple
from pathlib import Path
import shutil

import jinja2

from .data import extract_data
from .utils import rmdir
from .filters import redirect_path
from .page import Page



@dataclass(frozen=False)
class Renderer:
    content_path: Path
    template_path: Path
    output_path: Path
    data_dir: Path
    filters: dict
    _data: dict = None
    
        

    @classmethod
    def from_dirs(cls, content_dir, templates_dir, output_dir, data_dir, filters: dict[str, Callable[[str,], str]] = None) -> Iterable[Renderer]:
        
        templates_dir = Path(templates_dir)
        base_content_dir = Path(content_dir)
        for content_path in base_content_dir.glob('**/*.md'):
            if content_path.parent == base_content_dir:
                template_path = templates_dir / content_path.with_suffix('.html').name
                output_path = Path(output_dir) / content_path.with_suffix('.html').name
            elif content_path.name == '_index.md':
                template_path = templates_dir / content_path.parent.with_suffix('.html').name
                output_path = Path(output_dir) / content_path.parent.name / 'index.html'
            else:
                template_path = templates_dir / content_path.parent.parent.with_suffix('.html').with_stem(content_path.parent.stem[:-1])  # drop the 's' from the name
                output_path = Path(output_dir) / content_path.parent.name / content_path.with_suffix('.html').name
                
            assert template_path.exists(), f"Looking for {template_path}"
                 
            yield Renderer(
                content_path = content_path,
                template_path = template_path,
                output_path= output_path,
                data_dir = Path(data_dir),
                filters = filters if filters else {},
            )

    
    def _get_template(self) -> jinja2.Template:
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_path.parent),
            autoescape=jinja2.select_autoescape()
        )
        for name, fun in self.filters.items():
            env.filters[name] = redirect_path(self.output_dir)(fun)

        template = env.get_template(self.template_path.name)
        return template
    
    def extract_page(self, pages_data: dict = None) -> Page:
        if pages_data is None:
            pages_data = {}
        collections_data = extract_data(self.data_dir)
        
        extra_data = {'data': collections_data, 'pages': pages_data}
        page = Page.from_path(self.content_path, extra_data=extra_data)
        return page


    def extract_data(self) -> dict:
        if self._data is None:
            self._data = extract_data(self.data_dir)
        return self._data.copy()


    def render(self, extra_data: dict = None) -> None:
        """Create the rendered html and save to the output path."""
        if extra_data is None:
            extra_data = {}
        
        template = self._get_template()
        html = template.render(**extra_data)
        self.output_path.parent.mkdir(exist_ok=True, parents=True)
        self.output_path.write_text(html)
    

    @staticmethod
    def extract_multiple_pages(renderers: list[Renderer], content_dir: Path) -> dict:
        content_dir = Path(content_dir)
        pages_data = defaultdict(dict)
        for renderer in renderers:
            page = renderer.extract_page()
            page_path = renderer.content_path
            if page_path.parent == content_dir:
                pages_data[page_path.stem] = page.data
            elif page_path.parent.parent == content_dir:
                if page_path.stem == '_index':
                    continue
                pages_data[page_path.parent.name][page_path.stem] = page.data
            else:
                raise IOError("Multi-nested page folders not supported")
        return dict(pages_data)

            

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
    all_pages_data = Renderer.extract_multiple_pages(renderers=renderers, content_dir='./pages')
    for renderer in renderers:
        print("rendering:", renderer.content_path, 'from', renderer.template_path, 'to', renderer.output_path)
        data = renderer.extract_data()        
        page = renderer.extract_page(pages_data=all_pages_data)
        renderer.render(extra_data={'content': page.html, 'page': page.data, 'pages': all_pages_data, 'data': data})
        


    

if __name__ == '__main__':
    run_render_pipeline()

