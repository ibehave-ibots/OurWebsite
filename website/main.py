import os


# Use ipdb as the default debugger, if possible.
try:
    import ipdb
    os.environ['PYTHONBREAKPOINT'] = 'ipdb.set_trace'
except ImportError:
    pass


from argparse import ArgumentParser
import subprocess

from ssg.server import build_server
from ssg.renderer import run_render_pipeline

parser = ArgumentParser()

parser.add_argument('--cmd', choices=['serve', 'render', 'pull-data'], default='serve')

args = parser.parse_args()


run_render_pipeline()

match args.cmd:
    case 'pull-data':
        import dvc
        print('Downloading data...')
        subprocess.run("dvc pull".split(' '))
    case 'serve':
        build_server()
    case 'render':
        run_render_pipeline()
    case _:
        raise ValueError
