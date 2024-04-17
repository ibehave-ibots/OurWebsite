from typing import Any
import html
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown2 import Markdown
from yaml import load 
import yaml
import shutil
import os
from .extract_collections import extract_collections
from .utils import rmdir, redirect_path
from .image_processing import resize_image


env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)
env.filters['resize'] = redirect_path('output')(resize_image)




def render(env: Environment, content_path: str, template_name: str, data={}) -> None:
    template = env.get_template(f'{template_name}.html')

    with open(content_path) as f:
        text = f.read()


    data = {}
    *yaml_texts, markdown_text = text.split('---')
    if yaml_texts:
        yaml_text = yaml_texts[0]
        yaml_data = load(yaml_text, Loader=yaml.Loader)
        data.update(yaml_data)

    if markdown_text:
        markdowner = Markdown()
        content_html = markdowner.convert(markdown_text)
        data['content'] = content_html

    
    data['collections'] = data
    rendered = template.render(data=data)
    output_path = Path('output') / '/'.join(content_path.with_suffix('.html').parts[1:][-2:])
    output_path.parent.mkdir(exist_ok=True, parents=True)
    with open(output_path, 'w') as f:
        f.write(rendered)



def render_all():
    collections = extract_collections()

    if os.path.exists("output/static"):
        rmdir("output/static")
    shutil.copytree("static", "output/static")
    
    # render all templates found in templates
    # for path in Path('content').glob('*'):
    for path in Path('collections').glob('*'):        
        if path.is_dir():
            for file in path.glob('*.yaml'):
                # render(env, content_path=file, template_name=path.stem, data=collections)
                render(env, content_path=file, template_name="consulting", data=collections)
        else:
            # render(env, content_path=path, template_name=path.stem, data=collections)
            render(env, content_path=path, template_name="consulting", data=collections)


    

if __name__ == '__main__':
    render_all()


## http://127.0.0.1:5500/group.html works!! 
## But we need to stop the code from creating one html file per collection!