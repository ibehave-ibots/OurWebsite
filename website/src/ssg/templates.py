from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, NamedTuple
import jinja2



class JinjaRenderer(NamedTuple):
    env: jinja2.Environment

    @classmethod
    def from_path(cls, templates_dir: Path, filters: dict[str, Callable], globals: dict[str, Any]) -> JinjaRenderer:
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(templates_dir),
            autoescape=jinja2.select_autoescape(),
            undefined=jinja2.StrictUndefined,
        )
        env.filters.update(filters)
        env.globals.update(globals)
        env.trim_blocks = True
        env.lstrip_blocks = True
        return JinjaRenderer(env=env)

    def render_in_place(self, template_text: str, **data) -> str:
        rendered = self.env.from_string(template_text).render(**data)
        return rendered
    
    def render_named_template(self, template_name: str, **data) -> str:
        rendered = self.env.get_template(template_name).render(**data)
        return rendered





