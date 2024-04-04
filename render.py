from jinja2 import Environment, FileSystemLoader, select_autoescape
import json

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

def render(env: Environment, name: str, output_fmt='html') -> None:
    template = env.get_template(f'{name}.{output_fmt}')

    with open(f'content/{name}.json') as f:
        data = json.load(f)

    rendered = template.render(data=data)
    with open(f'output/{name}.{output_fmt}', 'w') as f:
        f.write(rendered)

def render_all():
    render(env, name="hello", output_fmt="txt")
    render(env, name="index")
