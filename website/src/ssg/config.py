from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .data_directory import text_to_data


@dataclass
class Config:
    static_path_map: dict[Path, Path]
    pages_dir: Path = Path('./pages')
    global_data_dir: Path = Path('./data')
    site_data_dir: Path = Path('./site')
    output_dir: Path = Path('./_output')
    page_static_dirname: str = '_static'
    output_static_dir: Path = Path('_output/static')

    @classmethod
    def from_path(cls, path: Path) -> Config:
        assert Path(path).suffix == '.yaml'
        text = Path(path).read_text()
        data = text_to_data(text, format='yaml')
        return Config(
            static_path_map={Path(src): Path(target) for src, target in data.get('static', {}).items()},
            pages_dir=Path(data['pages_dir']),
            global_data_dir=Path(data['global_data_dir']),
            site_data_dir=Path(data['site_data_dir']),
            output_dir=Path(data['output_dir']),
            page_static_dirname=str(data['page_static_dirname']),
            output_static_dir=Path(data['output_static_dir']),
        )