from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, Coroutine, Generator, Iterator, Literal

import markdown2
import yaml
import aioshutil
from aiopath import AsyncPath

from .templates.jinja_renderer import JinjaRenderer
from .data_directory import extract_global_data


@dataclass
class Config:
    static_path_map: dict[Path, Path]
    pages_dir: Path = Path('./pages')
    global_data_dir: Path = Path('./data')
    site_data_dir: Path = Path('./site')
    output_dir: Path = Path('./_output')

    @classmethod
    def from_path(cls, path: Path) -> Config:
        assert Path(path).suffix == '.yaml'
        data = yaml.load(Path(path).read_text(), Loader=yaml.Loader)
        return Config(
            static_path_map={Path(src): Path(target) for src, target in data.get('static', {}).items()},
            pages_dir=Path(data['pages_dir']),
            global_data_dir=Path(data['global_data_dir']),
            site_data_dir=Path(data['site_data_dir']),
            output_dir=Path(data['output_dir']),
        )


@dataclass
class RenderInstructions:
    template: Path
    page_data_files: dict[str, Path]
    url: str
    data: dict[str, Any]
    
    @classmethod
    def from_renderdata(cls, render_data) -> Iterator[RenderInstructions]:
        data_filenames = render_data.get('data', {})
        for page in render_data.get('pages', []):
            folder = page.get('folder', '')
            data_paths = {name: Path(folder).joinpath(fname) for name, fname in data_filenames.items()}
            yield RenderInstructions(
                template=render_data['template'],
                page_data_files=data_paths,
                url=page['url'],
                data=page.get('data', {})
            )
            


async def run_render_pipeline(config: Config):
    global_data = extract_global_data(base_path=config.global_data_dir)
    renderer = JinjaRenderer.from_path(templates_dir=config.pages_dir)
    site_data = {path.stem: await read_yaml(path, renderer, data=global_data) for path in config.site_data_dir.glob('*.yaml')}

    
    for renderfile_path in config.pages_dir.glob('[!_]*/_render.yaml'):
        render_data = await read_yaml(renderfile_path, renderer=renderer, data=global_data)
        
        await copyfiles(file_destinations=render_data.get('files', {}), basedir=renderfile_path.parent)
        for page_render_data in RenderInstructions.from_renderdata(render_data=render_data):

            page_data = {}
            for name, rel_path in page_render_data.page_data_files.items():
                data_path = renderfile_path.parent.joinpath(rel_path)
                data = await read_and_render_page_data(data_path, renderer, data=global_data)
                page_data[name] = data

            page_html = renderer.render_named_template(
                template_path=renderfile_path.parent.joinpath(page_render_data.template),
                **dict(
                    data=global_data,
                    site=site_data,
                    page=page_data | page_render_data.data | {'url': page_render_data.url}
                )
            )

            url_path = Path('./_output').joinpath(page_render_data.url.lstrip('/'))
            await write_textfile(path=url_path, text=page_html)


async def read_and_render_page_data(path, renderer: JinjaRenderer, **render_data):
    text = await AsyncPath(path).read_text()
    rendered_text = renderer.render_in_place(text, **render_data)
    data = text_to_data(rendered_text, format=path.suffix.lstrip('.'))
    return data
            


def copy_static_files(config: Config, skip_if_exists: bool = False) -> Iterator[Coroutine]:
    for src, target in config.static_path_map.items():
        if skip_if_exists and target.exists():
            continue
        yield copytree(src, target)


####### UTILS #####################

def text_to_data(text, format: Literal['md', 'yaml']) -> Any:
    loaders = {
        'md': lambda text: markdown2.Markdown().convert(text),
        'yaml': lambda text: yaml.load(text, yaml.Loader),
    }
    try:
        loader = loaders[format]
    except KeyError:
        raise NotImplementedError(f"{format} files not yet supported. Supported formats: {list(loaders.keys())}")
    
    data = loader(text)
    return data
    


async def write_textfile(path, text) -> None:
    apath = AsyncPath(path)
    await apath.parent.mkdir(parents=True, exist_ok=True)
    print(f"Writing: {path}")
    await apath.write_text(text)


async def read_yaml(path: Path, renderer: JinjaRenderer = None,  **render_data):
    text = await AsyncPath(path).read_text()
    if renderer is not None:
        text_to_load = renderer.render_in_place(template_text=text, **render_data)
    else:
        text_to_load = text
    data = yaml.load(text_to_load, yaml.Loader)
    return data


async def copyfile(src_path: Path, target_path: Path):
    src_path = AsyncPath(src_path)
    if not await src_path.exists():
            raise FileNotFoundError(f"Could not find file {src_path}.")
    await AsyncPath(target_path).parent.mkdir(parents=True, exist_ok=True)
    await aioshutil.copy2(src=src_path, dst=target_path)


async def copyfiles(file_destinations: dict[str, str], basedir: Path) -> None:
    basedir = Path(basedir)
    tasks = []

    for src, target in file_destinations.items():
        src_path = basedir.joinpath(src)
        
        if target.startswith('/'):
            target = target[1:]
        target_path = Path('./_output') / Path(target)
        print(f'Copying File: {src_path} -> {target_path}')
        # Add the file copy task with mkdir dependency to the tasks list
        tasks.append(copyfile(src_path, target_path))

    # Wait for all tasks to complete
    await asyncio.gather(*tasks)


async def copytree(src, target) -> None:
        await aioshutil.copytree(src, target, dirs_exist_ok=True)
        print(f"Copied {src}")
        
