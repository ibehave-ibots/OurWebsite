from livereload import Server
from .render import run_render_pipeline



def build_server() -> Server:
    server = Server()
    server.watch("templates/*.html", func=run_render_pipeline)
    server.watch("pages/*.md", func=run_render_pipeline)
    server.watch("data/*.md", func=run_render_pipeline)
    server.serve(root='./output')
