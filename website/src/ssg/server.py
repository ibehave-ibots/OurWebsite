import os
from pathlib import Path
from livereload import Server
from flask import Flask, abort, redirect, send_from_directory, make_response

from .vendor_patches import patch_livereload_to_fix_bug_around_wsgi_support
from .renderer import run_render_pipeline



def build_server() -> Server:

    # os.chdir('./_output')
    STATIC_FOLDER = './_output'
    app = Flask(__name__, root_path='.')


    @app.route('/')
    @app.route('/<path:path>')
    def catch_all(path='/'):
       
        if path.endswith('/'):
            return redirect('index.html')  # appends 'index.html' to the path for directory-style requests (e.g. 'events/' -> 'events/index.html')
        
        if os.path.isfile(os.path.join(STATIC_FOLDER, path)):
            response =  make_response(send_from_directory(STATIC_FOLDER, path ))
            if Path(path).suffix == '.html':
                response.headers['Content-Type'] = 'text/html; charset=UTF-8'
            return response
        else:
            # Return a 404 error if the file does not exist
            print('could not find:', path)
            return send_from_directory(STATIC_FOLDER, '404.html'), 404


    
    patch_livereload_to_fix_bug_around_wsgi_support()
    server = Server(app=app.wsgi_app)
    server.watch("templates/**/*", func=run_render_pipeline)
    server.watch("static/**/*", func=run_render_pipeline)
    server.watch("pages/**/*", func=run_render_pipeline)
    server.watch("data/**/*", func=run_render_pipeline)
    server.serve()
