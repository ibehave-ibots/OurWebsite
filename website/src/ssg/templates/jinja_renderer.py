from __future__ import annotations

from datetime import date, datetime
from pathlib import Path, PurePosixPath
from typing import Any, Callable, NamedTuple
import jinja2

from . import filters as f



class JinjaRenderer(NamedTuple):
    env: jinja2.Environment
    templates_dir: Path

    @classmethod
    def from_path(cls, templates_dir: Path, filters: dict[str, Callable] = None, globals: dict[str, Any] = None) -> JinjaRenderer:
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(templates_dir),
            autoescape=jinja2.select_autoescape(),
            undefined=jinja2.StrictUndefined,
        )
        env.trim_blocks = True
        env.lstrip_blocks = True

        # Include additional jinja filters
        env.filters.update({
            'copy_to': f.redirect_path('./_output', arg_idx=1)(f.copy_to),
            'flatten_nested': f.flatten_nested_dict,
            'index': f.multi_index,
            'items': f.items,
            'prepend': f.prepend,
            'promote_key': f.promote_key,
            'sort_by': f.sort_by,  
            'resize': f.redirect_path('./_output')(f.resize_image), 
        })
        if filters is not None:
            env.filters.update(filters)

        # Include additional jinja globals
        env.globals.update({
            'today': date.today(),
            'now': datetime.now(),
            'str': str,
        })
        if globals is not None:
            env.globals.update(globals)

        return JinjaRenderer(env=env, templates_dir=Path(templates_dir))

    @property
    def vars(self) -> dict[str, Any]:
        return self.env.globals

    def render_in_place(self, template_text: str, **data) -> str:
        rendered = self.env.from_string(template_text).render(**data)
        return rendered
    
    def render_named_template(self, template_path: Path, **data) -> str:
        template_name = str(PurePosixPath(template_path.relative_to(self.templates_dir)))
        rendered = self.env.get_template(template_name).render(**data)
        return rendered





