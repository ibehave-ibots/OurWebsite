

# Use ipdb as the default debugger, if possible.
try:
    import ipdb
    import os
    os.environ['PYTHONBREAKPOINT'] = 'ipdb.set_trace'
except ImportError:
    pass


import asyncio
from ssg.server import build_server
from ssg.renderer import run_render_pipeline
import shutil

if not os.path.exists("stats/"):
    os.makedirs('stats')
shutil.copy("../consulting_analysis/consult_repo/consulting_statistics.yaml", "stats/")



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

