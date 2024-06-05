from livereload import Server
from .renderer import run_render_pipeline



def build_server() -> Server:
    server = Server()
    server.watch("templates/**/*.html", func=run_render_pipeline)
    server.watch("static/**/*.css", func=run_render_pipeline)
    server.watch("pages/**/*.md", func=run_render_pipeline)
    server.watch("data/**/*.yaml", func=run_render_pipeline)
    server.serve(root='./output')
