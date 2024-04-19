from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

import jinja2

from .utils import load_yaml, load_markdown


class Page(NamedTuple):
    text: str
    extra_data: dict = {}

    @classmethod
    def from_path(cls, path, extra_data: dict = {}) -> Page:
        text = Path(path).read_text()
        return Page(text=text, extra_data=extra_data)
    
    @property
    def data(self) -> dict:
        *yamls, _ = self.text.split('---')
        if not yamls:
            return {}
        
        yaml = yamls[0]
        yaml_with_data = jinja2.Environment().from_string(yaml).render(data=self.extra_data)
        data = load_yaml(yaml_with_data)
        return data

    @property
    def markdown(self) -> str:
        *_, md_text = self.text.split('---')
        return md_text
        
    @property
    def html(self) -> str:
        html = load_markdown(self.markdown)
        return html