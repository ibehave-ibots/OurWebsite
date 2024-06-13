from livereload import Server
from .renderer import run_render_pipeline



def build_server() -> Server:
    server = Server()
    server.watch("templates/**/*", func=run_render_pipeline)
    server.watch("static/**/*", func=run_render_pipeline)
    server.watch("pages/**/*", func=run_render_pipeline)
    server.watch("data/**/*", func=run_render_pipeline)
    server.serve(root='./_output')
