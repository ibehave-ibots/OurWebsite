from pathlib import Path
from typing import Callable
import jinja2


def render_in_place(template_text: str, env: jinja2.Environment = jinja2.Environment(), **data) -> str:
    rendered = env.from_string(template_text).render(**data)
    return rendered


def render_named_template(env: jinja2.Environment, template_name: str, **data) -> str:
    rendered = env.get_template(template_name).render(**data)
    return rendered


def build_environment(template_dir: Path, filters: dict[str, Callable]) -> jinja2.Environment:
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        autoescape=jinja2.select_autoescape()
    )
    for name, fun in filters.items():
        env.filters[name] = fun
    return env