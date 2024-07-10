from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Coroutine, Iterator

import aioshutil
from aiopath import AsyncPath

from .config import Config
from .data_directory import extract_global_data, text_to_data
from .templates.jinja_renderer import JinjaRenderer


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
            
@dataclass            
class TemplateRendering:
    base_path: Path
    page_instructions: list[RenderInstructions]

    @classmethod
    async def from_file(cls, renderfile_path: Path, renderer: JinjaRenderer, **render_data) -> TemplateRendering:
        render_data = await read_yaml(renderfile_path, renderer=renderer, **render_data)
        return TemplateRendering(
            base_path=renderfile_path.parent,
            page_instructions=list(RenderInstructions.from_renderdata(render_data)),
        )


async def run_render_pipeline(config: Config):
    global_data = extract_global_data(base_path=config.global_data_dir)
    renderer = JinjaRenderer.from_path(templates_dir=config.pages_dir)
    site_data = await read_and_render_dir(base_dir=config.site_data_dir, renderer=renderer, data=global_data)

    
    for renderfile_path in config.pages_dir.glob('[!_]*/_render.yaml'):
        big_r = await TemplateRendering.from_file(renderfile_path, renderer, data=global_data)

        for static_dir in renderfile_path.parent.glob(config.page_static_dirname):
            await copy(static_dir, config.output_static_dir)

        for page_render_data in big_r.page_instructions:
            page_data = {}
            for name, rel_path in page_render_data.page_data_files.items():
                data_path = renderfile_path.parent.joinpath(rel_path)
                data = await read_and_render_page_data(data_path, renderer, data=global_data)
                page_data[name] = data

            page_html = await renderer.render_named_template(
                template_path=renderfile_path.parent.joinpath(page_render_data.template),
                **dict(
                    data=global_data,
                    site=site_data,
                    page=page_data | page_render_data.data | {'url': page_render_data.url}
                )
            )

            url_path = Path('./_output').joinpath(page_render_data.url.lstrip('/'))
            await write_textfile(path=url_path, text=page_html)


async def read_and_render_dir(base_dir: Path, renderer: JinjaRenderer, **render_data):
    data = {}
    async for path in AsyncPath(base_dir).glob('*.yaml'):
        data[path.stem] = await read_yaml(path, renderer, **render_data)
    return data



async def read_and_render_page_data(path, renderer: JinjaRenderer, **render_data):
    text = await AsyncPath(path).read_text()
    rendered_text = await renderer.render_in_place(text, **render_data)
    data = text_to_data(rendered_text, format=path.suffix.lstrip('.'))
    return data
            


def copy_static_files(config: Config, skip_if_exists: bool = False) -> Iterator[Coroutine]:
    for src, target in config.static_path_map.items():
        if skip_if_exists and target.exists():
            continue
        yield copy(src, target)


####### UTILS #####################


async def write_textfile(path, text) -> None:
    apath = AsyncPath(path)
    await apath.parent.mkdir(parents=True, exist_ok=True)
    await apath.write_text(text)


async def read_yaml(path: Path, renderer: JinjaRenderer = None,  **render_data):
    text = await AsyncPath(path).read_text()
    text_to_load = await renderer.render_in_place(template_text=text, **render_data) if renderer is not None else text
    data = text_to_data(text_to_load, format='yaml')
    return data



async def copy(src: Path, target: Path) -> None:
    print(f"Copying: {src}")
    if Path(src).is_dir():
        await aioshutil.copytree(src, target, dirs_exist_ok=True)
        return
    
    await AsyncPath(target).parent.mkdir(parents=True, exist_ok=True)
    await aioshutil.copy2(src=src, dst=target)


        
