from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
import jinja2

from . import filters as f


def build_jinja_environment(paths: list[Path|str]) -> jinja2.Environment:
    env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(paths),
            autoescape=jinja2.select_autoescape(),
            undefined=jinja2.StrictUndefined,
            enable_async=True,
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

    # Include additional jinja globals
    env.globals.update({
        'today': date.today(),
        'now': datetime.now(),
        'str': str,
    })
    return env



