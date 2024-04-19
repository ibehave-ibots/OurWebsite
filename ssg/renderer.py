from __future__ import annotations

from typing import Any, Callable, Iterable, NamedTuple
from pathlib import Path
import shutil

import jinja2

from .data import extract_data
from .utils import rmdir
from .filters import redirect_path
from .page import Page



class Renderer(NamedTuple):
    content_path: Path
    template_path: Path
    output_path: Path
    data_dir: Path
    filters: dict

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
    
    def _extract_data(self) -> dict:
        """Extract data from content file (both yaml and markdown) and yaml data collections."""
        collections_data = extract_data(self.data_dir)
        content = Page.from_path(self.content_path, extra_data={'data': collections_data})
        data = {}
        data['page'] = content.data | {'content': content.html}
        data['data'] = collections_data
        return data
    

    def render(self) -> None:
        """Create the rendered html and save to the output path."""
        data = self._extract_data()
        template = self._get_template()
        html = template.render(**data)
        self.output_path.parent.mkdir(exist_ok=True, parents=True)
        self.output_path.write_text(html)
    


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
        print("rendering:", renderer.content_path, 'from', renderer.template_path, 'to', renderer.output_path)
        renderer.render()
        


    

if __name__ == '__main__':
    run_render_pipeline()

