import os
from pathlib import Path
from livereload import Server
from flask import Flask, abort, redirect, send_from_directory, make_response
from werkzeug.utils import send_file
from wsgiref.types import WSGIEnvironment

from .vendor_patches import patch_livereload_to_fix_bug_around_wsgi_support
from .renderer import run_render_pipeline



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
    server.watch("templates/**/*", func=run_render_pipeline)
    server.watch("static/**/*", func=run_render_pipeline)
    server.watch("pages/**/*", func=run_render_pipeline)
    server.watch("data/**/*", func=run_render_pipeline)
    server.serve()
