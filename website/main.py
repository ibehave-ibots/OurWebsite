

# Use ipdb as the default debugger, if possible.
try:
    import ipdb
    import os
    os.environ['PYTHONBREAKPOINT'] = 'ipdb.set_trace'
except ImportError:
    pass


import asyncio
from dataclasses import dataclass
from typing import Any, Coroutine
from ssg.renderer import run_render_pipeline
from ssg.server import build_server, TornadoEventLoopCallable
import shutil

if not os.path.exists('theme'):
    if not os.path.exists('remote_files/theme.7z'):
        raise FileNotFoundError("Need theme.7z.  Be sure to run dvc pull to get the file.")
    import py7zr
    print('extracting theme.7z to theme...')
    with py7zr.SevenZipFile('remote_files/theme.7z') as f:
        f.extract('.', ['theme'], recursive=True)


if not os.path.exists('../group_data/data'):
    raise FileNotFoundError("Need group database.  Be sure to run dvc pull to get it.")



page_builders = asyncio.run(run_render_pipeline())


# breakpoint()


server = build_server()
for md_path, (coro, args) in page_builders.items():
    server.watch(md_path, TornadoEventLoopCallable(coro, args), delay=3)
    
server.serve()


