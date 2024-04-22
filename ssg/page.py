from __future__ import annotations

from pathlib import Path
from typing import NamedTuple
from dataclasses import dataclass, field

import jinja2

from .utils import load_yaml, load_markdown


@dataclass(frozen=True)
class Page:
    text: str
    extra_data: dict = field(default_factory=dict)

    @classmethod
    def from_path(cls, path, extra_data: dict = None) -> Page:
        path = Path(path)
        if extra_data is None:
            extra_data = {}
        text = path.read_text()
        return Page(text=text, extra_data=extra_data, )
    

    @property
    def data(self) -> dict:
        *yamls, _ = self.text.split('---')
        if not yamls:
            return {}
        
        yaml = yamls[0]
        yaml_with_data = jinja2.Environment().from_string(yaml).render(**self.extra_data)
        data = load_yaml(yaml_with_data)
        return data

    @property
    def markdown(self) -> str:
        *_, md_text = self.text.split('---')
        md_text_with_data = jinja2.Environment().from_string(md_text).render(**self.extra_data)
        return md_text_with_data.strip()
        
    @property
    def html(self) -> str:
        html = load_markdown(self.markdown)
        return html