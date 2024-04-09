from .server import build_server
from .render import render_all


def launch_app():
    render_all()
    build_server()