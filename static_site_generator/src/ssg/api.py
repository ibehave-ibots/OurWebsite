from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from .renderer import run_render_pipeline
from .server import build_server, TornadoEventLoopCallable, Server

if TYPE_CHECKING:
    from .config import Config


def build_dev_server(config: Config) -> Server:
    # Use ipdb as the default debugger when in dev mode, if possible.
    try:
        import ipdb
        import os
        os.environ['PYTHONBREAKPOINT'] = 'ipdb.set_trace'
    except ImportError:
        pass
    
    page_builders = asyncio.run(run_render_pipeline(config=config))
    server = build_server()
    for md_path, (coro, args) in page_builders.items():
        server.watch(md_path, TornadoEventLoopCallable(coro, args), delay=3)

    return server

        

def build_output(config: Config):
    asyncio.run(run_render_pipeline(config=config))