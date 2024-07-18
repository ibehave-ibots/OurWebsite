from pathlib import Path
from typing import Any, Literal

import aioshutil
import markdown2
import yaml
from aiopath import AsyncPath


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


async def write_textfile(path, text) -> None:
    apath = AsyncPath(path)
    await apath.parent.mkdir(parents=True, exist_ok=True)
    await apath.write_text(text)



loaders = {
    'md': lambda text: markdown2.Markdown().convert(text),
    'yaml': lambda text: yaml.load(text, yaml.Loader),
}

def loads(text, format: Literal['md', 'yaml']) -> Any:
    try:
        loader = loaders[format]
    except KeyError:
        raise NotImplementedError(f"{format} files not yet supported. Supported formats: {list(loaders.keys())}")
    
    data = loader(text)
    return data
