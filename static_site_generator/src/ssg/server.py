
import asyncio
from dataclasses import dataclass, field
from typing import Any, Coroutine

from flask import Flask, redirect, send_from_directory
from livereload import Server
from tornado.ioloop import IOLoop

from .vendor_patches import patch_livereload_to_fix_bug_around_wsgi_support


def build_server() -> Server:

    app = Flask(__name__, root_path='.', static_folder='.')

    @app.route('/')
    @app.route('/<path:path>')
    def catch_all(path='/'):
        if path.endswith('/'):
            return redirect('index.html')  # appends 'index.html' to the path for directory-style requests (e.g. 'events/' -> 'events/index.html')
        
        return send_from_directory('_output', path=path)

    @app.errorhandler(404)
    def page_not_found(e):
        return send_from_directory('_output', '404.html'), 404
    

    patch_livereload_to_fix_bug_around_wsgi_support()
    server = Server(app=app.wsgi_app)
    return server


@dataclass
class TornadoEventLoopCallable:
    coro: Coroutine
    args: tuple[Any, ...] = field(default_factory=tuple, repr=False)
    kwargs: dict[str, Any] = field(default_factory=dict, repr=False)

    def __call__(self):
        loop = IOLoop.current().asyncio_loop
        awaitable = self.coro(*self.args, **self.kwargs)
        result = asyncio.run_coroutine_threadsafe(awaitable, loop)
        return True


