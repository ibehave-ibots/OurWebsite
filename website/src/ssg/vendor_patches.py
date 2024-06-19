import wrapt


def patch_livereload_to_fix_bug_around_wsgi_support():  

    from livereload.server import WSGIContainer

    @wrapt.patch_function_wrapper('livereload.server', 'LiveScriptContainer.__init__')
    def patched_init(wrapped, instance, args, kwargs):
        print("Patched __init__ called")
        # Call the superclass __init__ first
        wsgi_app = args[0] if args else kwargs['wsgi_app']
        WSGIContainer.__init__(instance, wsgi_application=wsgi_app)
        return wrapped(*args, **kwargs)


    @wrapt.patch_function_wrapper('livereload.server', 'LiveScriptContainer.__call__')
    def patched_call(wrapped, instance, args, kwargs):
        print("Patched __call__ called...............................................")
        wrapped.__globals__['WSGIContainer'] = instance
        return wrapped(*args, **kwargs)

