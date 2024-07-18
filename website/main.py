

# Use ipdb as the default debugger, if possible.
try:
    import ipdb
    import os
    os.environ['PYTHONBREAKPOINT'] = 'ipdb.set_trace'
except ImportError:
    pass


import asyncio
from ssg.renderer import run_render_pipeline
import shutil

if not os.path.exists('theme'):
    if not os.path.exists('remote_files/theme.7z'):
        raise FileNotFoundError("Need theme.7z.  Be sure to run dvc pull to get the file.")
    import py7zr
    print('extracting theme.7z to theme...')
    with py7zr.SevenZipFile('remote_files/theme.7z') as f:
        f.extract('.', ['theme'], recursive=True)


if not os.path.exists('../group_data/data'):
    raise FileNotFoundError("Need group database.  Go over to the group_data folder and run dvc pull to get it.")
shutil.copytree('../group_data/data', './data', dirs_exist_ok=True)



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

