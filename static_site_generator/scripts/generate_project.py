from pathlib import Path
from argparse import ArgumentParser

parser = ArgumentParser(description="Generate iBOTS-SSG Project Template")
parser.add_argument('basedir', help='The base direcgory of the project')

args = parser.parse_args()

basedir = args.basedir

files = [
    ('pages/index.md', '---\ntitle: Homepage\n---\n\n# Welcome to the {{ page.title }}!\n\nPut your content here.'),
    ('pages/templates.html', '<body>\n   {{ page.content }}\n</body>\n'),
    ('data/meta.yaml', 'a: 3\nb: 4\n'),
    ('shared/data', None),
]

for f, text in files:
    path = Path(basedir).joinpath(f)
    if text is not None:
        path.parent.mkdir(exist_ok=True, parents=True)
        path.write_text(text)
    else:
        path.mkdir(exist_ok=True, parents=True)