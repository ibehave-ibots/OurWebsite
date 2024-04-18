from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

from .utils import load_yaml, load_markdown


class Page(NamedTuple):
    text: str

    @classmethod
    def from_path(cls, path) -> Page:
        text = Path(path).read_text()
        return Page(text=text)
    
    @property
    def data(self) -> dict:
        *yamls, _ = self.text.split('---')
        return load_yaml(yamls[0]) if yamls else {}

    @property
    def markdown(self) -> str:
        *_, md_text = self.text.split('---')
        return md_text
        
    @property
    def html(self) -> str:
        html = load_markdown(self.markdown)
        return html