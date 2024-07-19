import os
from argparse import ArgumentParser

import py7zr

from ssg.api import build_dev_server, build_output
from ssg.config import Config


if not os.path.exists('theme'):
    if not os.path.exists('remote_files/theme.7z'):
        raise FileNotFoundError("Need theme.7z.  Be sure to run dvc pull to get the file.")
    print('extracting theme.7z to theme...')
    with py7zr.SevenZipFile('remote_files/theme.7z') as f:
        f.extract('.', ['theme'], recursive=True)


if not os.path.exists('./data'):
    raise FileNotFoundError("Need group database.  Be sure to run dvc pull to get it.")


parser = ArgumentParser()
parser.add_argument('command', choices=['serve', 'render'])
parser.add_argument('--base_url', default='', type=str)
args = parser.parse_args()

config = Config(base_url=args.base_url)

if args.command == 'serve':
    server = build_dev_server(config=config)
    server.serve()
elif args.command == 'render':
    build_output(config=config)
else:
    raise ValueError("not a valid option.")


