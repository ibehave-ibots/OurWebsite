import wrapt


def patch_livereload_to_fix_bug_around_wsgi_support():  
    """
    This patch is to fix the error descrbed here: https://stackoverflow.com/questions/78039400/flask-with-livereload-and-tornado-causing-error-when-i-run-my-program

    (Yes, I came up with this solution myself.  Use with caution!)
    """

    from livereload.server import WSGIContainer

    @wrapt.patch_function_wrapper('livereload.server', 'LiveScriptContainer.__init__')
    def patched_init(wrapped, instance, args, kwargs):
        """
        LiveScriptContainer should also call the __init__() from its superclass.
        """
        wsgi_app = args[0] if args else kwargs['wsgi_app']
        WSGIContainer.__init__(instance, wsgi_application=wsgi_app)
        return wrapped(*args, **kwargs)


    @wrapt.patch_function_wrapper('livereload.server', 'LiveScriptContainer.__call__')
    def patched_call(wrapped, instance, args, kwargs):
        """
        LiveScriptContainer.__call__ is trying to call an instance method of its parent class as a static method.
        The problem is that it was changed from a static method in some change, and this is what broke things.
        Here, we trick the __call__ method into using itself instead of WSGIContainer when it references the WSGIContainer name.
        """
        wrapped.__globals__['WSGIContainer'] = instance
        return wrapped(*args, **kwargs)

