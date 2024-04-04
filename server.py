from livereload import Server
from glob import glob
from render import render_all

render_all()
server = Server()
server.watch("templates/*.html", func=render_all)
server.watch("content/*.json", func=render_all)
server.serve(root='./output')
