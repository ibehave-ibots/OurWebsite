from __future__ import annotations

import asyncio
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Coroutine, TYPE_CHECKING

from aiopath import AsyncPath
import jinja2

from .utils import copy, write_textfile, loads
from .templates.jinja_renderer import build_jinja_environment
import ibots_db

if TYPE_CHECKING:
    from .config import Config


async def run_render_pipeline(config: Config) -> dict[str, tuple[Coroutine, tuple[Any, ...]]]:
    await copy_static_dirs(basedir=config.base_dir)
    page_builders = await generate_page_builders(config=config)

    await asyncio.gather(*(coro(*args) for coro, args in page_builders.values()))
    return page_builders


async def generate_page_builders(config: Config) -> dict[str, tuple[Coroutine, tuple[Any, ...]]]:
    basedir = config.base_dir
    config_data = config.model_dump(mode='json')
    
    global_data = ibots_db.load(basedir / 'data').model_dump(mode='json')
    
    # Read site-wide data
    env = build_jinja_environment()
    shared_data = await read_and_render_yaml_dir(base_dir=basedir / 'shared/data', env=env, data=global_data)
    
    # Walk through each 'pages' directory and render the pages found inside
    page_build_tasks = {}
    async for page_path in AsyncPath(basedir / 'pages').glob('**/[!_]*.md'):
        if page_path.parent.name.startswith('_'):
            continue

        page_build_tasks[str(PurePosixPath(page_path))] = (build_page, (basedir, config_data, global_data, shared_data, page_path))

    return page_build_tasks
    


async def build_page(basedir, config_data, global_data, shared_data, page_path):
    print(f'Start Rendering: {page_path}')
    subpages_data = defaultdict(dict)
    async for subpage_path in page_path.parent.glob('[!_]*/[!_]*.md'):
        subpage_data = await read_and_render_page_data(basedir / 'pages', subpage_path, config=config_data, data=global_data, site=shared_data)
        subpages_data[subpage_data['type']][subpage_data['id']] = subpage_data
    subpages_data = dict(subpages_data)
        

        # Render HTML Template
    env = build_jinja_environment([basedir / 'shared/templates', page_path.parent])
    template = env.get_template('template.html')
    page_data = await read_and_render_page_data(basedir / 'pages', page_path, config=config_data, data=global_data, site=shared_data)
    page_html = await template.render_async(
            config=config_data,
            data=global_data, 
            site=shared_data, 
            page=page_data,
            subpages=subpages_data,
        )

    output_path = Path(basedir / '_output').joinpath(page_data['url'])
    await write_textfile(path=output_path, text=page_html)
    print(f'Done Rendering: {page_path}')


async def copy_static_dirs(basedir: Path):
    await asyncio.gather(
        copy(basedir / 'shared/static', basedir / '_output/static'),
        copy(basedir / 'theme/assets', basedir / '_output/assets'),
    )



def url_from_path(basedir, page_path: Path):
    url_path = page_path.relative_to(basedir).with_suffix('.html')
    if Path(page_path).with_suffix('').is_dir():
        url_path = url_path.with_suffix('').joinpath('index.html')
    url = str(PurePosixPath(url_path))
    return url


async def read_and_render_page_data(basedir, page_path, **render_data):
    page_text = (await page_path.read_text()).strip()
    env = build_jinja_environment()
    if page_text.startswith('---'):
        _, templated_yaml_text, md_text = page_text.split('---')
        template = env.from_string(templated_yaml_text)
        yaml_text = await template.render_async(**render_data)
        yaml_data = loads(yaml_text, format='yaml')
    else:
        yaml_data = {}
        md_text = page_text

    md_html = loads(md_text, 'md')                
    page_data = yaml_data
    page_data['content'] = md_html
    page_data['url'] = url_from_path(basedir, page_path)
    page_data['id'] = page_path.stem
    page_data['type'] = page_path.parent.name
    return page_data



async def read_and_render_yaml_dir(base_dir: str | Path, env: jinja2.Environment, **render_data):
    data = {}
    async for path in AsyncPath(base_dir).glob('*.yaml'):
        text = await AsyncPath(path).read_text()
        template = env.from_string(text)
        text_to_load = await template.render_async(**render_data)
        data[path.stem] = loads(text_to_load, format='yaml')
    return data


            









        
 