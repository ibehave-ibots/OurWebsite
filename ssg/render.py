from typing import Any
import html
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown2 import Markdown

import shutil
import os
from .extract_collections import extract_collections
from .utils import rmdir, redirect_path, parse_yaml
from .image_processing import resize_image


env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)
env.filters['resize'] = redirect_path('output')(resize_image)


def render(template: str, text: str, data: dict) -> None:
    data = parse_yaml(text)
    rendered = template.render(data=data)
    return rendered



    



def render_all():
    collections = extract_collections()

    if os.path.exists("output/static"):
        rmdir("output/static")
    shutil.copytree("static", "output/static")
    
    # render all templates found in templates
    for path in Path('collections').glob('*'):        
        if path.is_dir():
            for file in path.glob('*.yaml'):
                template = env.get_template(f'consulting.html')
                text = Path(file).read_text()
                rendered = render(template=template, text=text, data=collections)
                output_path = Path('output') / '/'.join(Path(file).with_suffix('.html').parts[1:][-2:])
                output_path.parent.mkdir(exist_ok=True, parents=True)
                with open(output_path, 'w') as f:
                    f.write(rendered)
        else:
            template = env.get_template(f'consulting.html')
            text = Path(path).read_text()
            rendered = render(template=template, text=text, data=collections)
            output_path = Path('output') / '/'.join(Path(path).with_suffix('.html').parts[1:][-2:])
            output_path.parent.mkdir(exist_ok=True, parents=True)
            with open(output_path, 'w') as f:
                f.write(rendered)
    


    

if __name__ == '__main__':
    render_all()

