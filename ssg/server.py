from livereload import Server
from .render import render_all



def build_server() -> Server:
    server = Server()
    server.watch("templates/*.html", func=render_all)
    server.watch("content/*.md", func=render_all)
    server.serve(root='./output')
