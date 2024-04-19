from argparse import ArgumentParser

from ssg.server import build_server
from ssg.renderer import run_render_pipeline


parser = ArgumentParser()

parser.add_argument('--cmd', choices=['serve', 'render'], default='serve')

args = parser.parse_args()

match args.cmd:
    case 'serve':
        build_server()
    case 'render':
        run_render_pipeline()
    case _:
        raise ValueError
