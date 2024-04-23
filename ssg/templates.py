from __future__ import annotations

from pathlib import Path
from datetime import datetime, date
from typing import Callable, NamedTuple
import jinja2


## Public Interface

class JinjaRenderer(NamedTuple):
    env: jinja2.Environment

    @classmethod
    def from_path(cls, templates_dir: Path, filters: dict[str, Callable]) -> JinjaRenderer:
        env = _build_environment(template_dir=templates_dir, filters=filters)
        
        return JinjaRenderer(env=env)

    def render_in_place(self, template_text: str, **data) -> str:
        return _render_in_place(env=self.env, template_text=template_text, **data)
    
    def render_named_template(self, template_name: str, **data) -> str:
        return _render_named_template(env=self.env, template_name=template_name, **data)


## Util Functions

def _render_in_place(template_text: str, env: jinja2.Environment = jinja2.Environment(), **data) -> str:
    rendered = env.from_string(template_text).render(**data)
    return rendered


def _render_named_template(env: jinja2.Environment, template_name: str, **data) -> str:
    rendered = env.get_template(template_name).render(**data)
    return rendered


def _build_environment(template_dir: Path, filters: dict[str, Callable]) -> jinja2.Environment:
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        autoescape=jinja2.select_autoescape()
    )
    for name, fun in filters.items():
        env.filters[name] = fun
    env.globals['today'] = date.today()
    env.globals['now'] = datetime.now()
    env.trim_blocks = True
    env.lstrip_blocks = True
    
    return env


