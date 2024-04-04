from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown2 import Markdown
from yaml import load 
import yaml

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

def render(env: Environment, name: str) -> None:
    template = env.get_template(f'{name}.html')

    with open(f'content/{name}.md') as f:
        text = f.read()
        yaml_text, markdown_text = text.split('---')
        data = load(yaml_text, Loader=yaml.Loader)
        markdowner = Markdown()
        content_html = markdowner.convert(markdown_text)
        data['content'] = content_html


    rendered = template.render(data=data)
    with open(f'output/{name}.html', 'w') as f:
        f.write(rendered)

def render_all():
    render(env, name="index")


if __name__ == '__main__':
    render_all()