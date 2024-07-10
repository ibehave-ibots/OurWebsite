from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Coroutine, Iterator

import aioshutil
from aiopath import AsyncPath
import jinja2

from .data_directory import extract_global_data, text_to_data
from .templates.jinja_renderer import build_jinja_environment



async def run_render_pipeline():
    
    # Copy Static Files
    await asyncio.gather(
        copy('./site/static', './_output/static'),
        copy('./theme/assets', './_output/assets'),
    )

    # Read Shared Data (no templating allowed)
    global_data = extract_global_data(base_path='./data')
    
    # Read site-wide data
    env = build_jinja_environment()
    site_data = await read_and_render_yaml_dir(base_dir='./site/data', env=env, data=global_data)
    
    # Walk through each 'pages' directory and render the pages found inside
    async for page_path in AsyncPath('./pages').glob('[!_]*/[!_]*.md'):
        page_text = (await page_path.read_text()).strip()

        print(f'Rendering: {page_path}')
        if page_text.startswith('---'):
            _, templated_yaml_text, md_text = page_text.split('---')
            template = env.from_string(templated_yaml_text)
            yaml_text = await template.render_async( data=global_data, site=site_data)
            yaml_data = text_to_data(yaml_text, format='yaml')
        else:
            yaml_data = {}
            md_text = page_text

        md_html = text_to_data(md_text, 'md')                
        page_data = {'data': yaml_data, 'content': md_html}



        # Render HTML Template
        env = build_jinja_environment(['./site/templates', page_path.parent])
        template = env.get_template('template.html')
        url_path = page_path.relative_to('./pages').with_suffix('.html')
        if url_path.name == 'index.html':
            url_path = url_path.parent.with_suffix('.html')
            
        page_html = await template.render_async(
            data=global_data, 
            site=site_data, 
            page=page_data,
            url=str(PurePosixPath(url_path))
        )

        output_path = Path('./_output').joinpath(url_path)
        await write_textfile(path=output_path, text=page_html)



    # for renderfile_path in config.pages_dir.glob('[!_]*/_render.yaml'):

    #     for static_dir in renderfile_path.parent.glob(config.page_static_dirname):
    #         await copy(static_dir, config.output_static_dir)

    #     for page_render_data in big_r.page_instructions:
    #         page_data = {}
    #         for name, rel_path in page_render_data.page_data_files.items():
    #             data_path = renderfile_path.parent.joinpath(rel_path)
    #             data = await read_and_render_page_data(data_path, renderer, data=global_data)
    #             page_data[name] = data

    #         page_html = await renderer.render_named_template(
    #             template_path=renderfile_path.parent.joinpath(page_render_data.template),
    #             **dict(
    #                 data=global_data,
    #                 site=site_data,
    #                 page=page_data | page_render_data.data | {'url': page_render_data.url}
    #             )
    #         )

    #         await write_textfile(path=url_path, text=page_html)


async def read_and_render_yaml_dir(base_dir: str | Path, env: jinja2.Environment, **render_data):
    data = {}
    async for path in AsyncPath(base_dir).glob('*.yaml'):
        text = await AsyncPath(path).read_text()
        template = env.from_string(text)
        text_to_load = await template.render_async(**render_data)
        data[path.stem] = text_to_data(text_to_load, format='yaml')
    return data



async def read_and_render_page_data(path, renderer: JinjaRenderer, **render_data):
    text = await AsyncPath(path).read_text()
    rendered_text = await renderer.render_in_place(text, **render_data)
    data = text_to_data(rendered_text, format=path.suffix.lstrip('.'))
    return data
            



####### UTILS #####################


async def write_textfile(path, text) -> None:
    apath = AsyncPath(path)
    await apath.parent.mkdir(parents=True, exist_ok=True)
    await apath.write_text(text)





async def copy(src: Path, target: Path, skip_if_exists: bool = True) -> None:
    
    if skip_if_exists and Path(target).exists():
        print(f'Skipping Copying: {src}')
        return
    
    print(f"Copying: {src}")
    if Path(src).is_dir():

        await aioshutil.copytree(src, target, dirs_exist_ok=True)
        return
    
    await AsyncPath(target).parent.mkdir(parents=True, exist_ok=True)
    await aioshutil.copy2(src=src, dst=target)


        
 