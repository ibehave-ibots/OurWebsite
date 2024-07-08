

# Use ipdb as the default debugger, if possible.
try:
    import ipdb
    import os
    os.environ['PYTHONBREAKPOINT'] = 'ipdb.set_trace'
except ImportError:
    pass


from ssg.server import build_server
build_server()
