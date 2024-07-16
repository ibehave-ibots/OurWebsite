from argparse import ArgumentParser

from ssg import build_server, run_render_pipeline
import asyncio
import shutil


parser = ArgumentParser(description='Launches a Dev Server to serve the website and reload it when changes are detected.')
parser.add_argument('basedir', help='The base directory of the website project.')

args = parser.parse_args()


async def build_output():
    await run_render_pipeline()

asyncio.run(build_output())


# async def build_output(config: Config):
#     tasks = []
#     tasks += list(copy_static_files(config=config, skip_if_exists=True))
#     tasks += [run_render_pipeline(config=config)]
#     await asyncio.gather(*tasks)

# config = Config.from_path('config.yaml')
# asyncio.run(build_output(config=config))



# server = build_server()
# server.watch('pages/**/*', lambda: asyncio.ensure_future(build_output(config)), delay=3)
# server.watch('data/**/*', lambda: asyncio.ensure_future(build_output(config)), delay=3, )
# server.serve()

# asyncio.run(build_server())

