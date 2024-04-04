from jinja2 import Environment, FileSystemLoader, select_autoescape
import json

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

def render(env: Environment, name: str) -> None:
    template = env.get_template(f'{name}.html')

    with open(f'content/{name}.md') as f:
        text = f.read()
        json_text, _ = text.split('---')
        data = json.loads(json_text)


    rendered = template.render(data=data)
    with open(f'output/{name}.html', 'w') as f:
        f.write(rendered)

def render_all():
    render(env, name="index")


if __name__ == '__main__':
    render_all()