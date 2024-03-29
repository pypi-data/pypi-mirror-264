"""Django backport and compatibility utilities."""

import functools
import inspect
import os
import subprocess
import sys
import six

import django
from django.utils.html import conditional_escape


__all__ = ('simple_tag', '_')


if django.VERSION >= (3, 0):
    from django.utils.translation import gettext_lazy as _

    def python_2_unicode_compatible(cls):
        return cls
else:
    from django.utils.translation import gettext_lazy as _
    from django.utils.encoding import python_2_unicode_compatible

try:
    from django.template.library import Library  # NOQA
    simple_tag = Library.simple_tag
except ImportError:
    # django 1.8
    from django.template import Node
    from django.template.base import parse_bits

    class TagHelperNode(Node):
        """Base class for tag helper nodes such as SimpleNode and InclusionNode.

        Manages the positional and keyword arguments to be passed to
        the decorated function.
        """

        def __init__(self, func, takes_context, args, kwargs):  # noqa: D102
            self.func = func
            self.takes_context = takes_context
            self.args = args
            self.kwargs = kwargs

        def get_resolved_arguments(self, context):
            resolved_args = [var.resolve(context) for var in self.args]
            if self.takes_context:
                resolved_args = [context] + resolved_args
            resolved_kwargs = {
                k: v.resolve(context)
                for k, v in self.kwargs.items()
            }
            return resolved_args, resolved_kwargs

    class SimpleNode(TagHelperNode):
        def __init__(self, func, takes_context, args, kwargs, target_var):
            super(SimpleNode, self).__init__(func, takes_context, args, kwargs)
            self.target_var = target_var

        def render(self, context):
            resolved_args, resolved_kwargs = \
                self.get_resolved_arguments(context)
            output = self.func(*resolved_args, **resolved_kwargs)
            if self.target_var is not None:
                context[self.target_var] = output
                return ''
            if context.autoescape:
                output = conditional_escape(output)
            return output

    def getargspec(func):
        if six.PY2:
            return inspect.getargspec(func)

        sig = inspect.signature(func)
        args = [
            p.name for p in sig.parameters.values()
            if p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
        ]
        varargs = [
            p.name for p in sig.parameters.values()
            if p.kind == inspect.Parameter.VAR_POSITIONAL
        ]
        varargs = varargs[0] if varargs else None
        varkw = [
            p.name for p in sig.parameters.values()
            if p.kind == inspect.Parameter.VAR_KEYWORD
        ]
        varkw = varkw[0] if varkw else None
        defaults = [
            p.default for p in sig.parameters.values()
            if p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
            if p.default is not p.empty
        ] or None
        return args, varargs, varkw, defaults

    def simple_tag(library, func=None, takes_context=None, name=None):
        """
        Register a callable as a compiled template tag.

        Example:
            @register.simple_tag
            def hello(*args, **kwargs):
                return 'world'

        Backport from django 1.9
        """
        def dec(func):
            params, varargs, varkw, defaults = getargspec(func)
            function_name = (
                name or getattr(func, '_decorated_function', func).__name__
            )

            @functools.wraps(func)
            def compile_func(parser, token):
                bits = token.split_contents()[1:]
                target_var = None
                if len(bits) >= 2 and bits[-2] == 'as':
                    target_var = bits[-1]
                    bits = bits[:-2]
                    args, kwargs = parse_bits(
                        parser, bits, params, varargs, varkw,
                        defaults, takes_context, function_name)
                return SimpleNode(
                    func, takes_context, args, kwargs, target_var)
            library.tag(function_name, compile_func)
            return func

        if func is None:
            # @register.simple_tag(...)
            return dec
        elif callable(func):
            # @register.simple_tag
            return dec(func)
        else:
            raise ValueError("Invalid arguments provided to simple_tag")


def context_flatten(context):
    result = {}
    # https://code.djangoproject.com/ticket/24765
    for dict_ in context.dicts:
        if hasattr(dict_, 'flatten'):
            dict_ = context_flatten(dict_)
        result.update(dict_)
    return result


def which(cmd, mode=os.F_OK | os.X_OK, path=None):
    """Given a command, mode, and a PATH string, return the path which
    conforms to the given mode on the PATH, or None if there is no such
    file.

    `mode` defaults to os.F_OK | os.X_OK. `path` defaults to the result
    of os.environ.get("PATH"), or can be overridden with a custom search
    path.

    Backport from Python 3.3
    https://hg.python.org/cpython/file/default/Lib/shutil.py
    """
    # Check that a given file can be accessed with the correct mode.
    # Additionally check that `file` is not a directory, as on Windows
    # directories pass the os.access check.
    def _access_check(fn, mode):
        return (os.path.exists(fn) and os.access(fn, mode) and not os.path.isdir(fn))

    # If we're given a path with a directory part, look it up directly rather
    # than referring to PATH directories. This includes checking relative to the
    # current directory, e.g. ./script
    if os.path.dirname(cmd):
        if _access_check(cmd, mode):
            return cmd
        return None

    if path is None:
        path = os.environ.get("PATH", os.defpath)
    if not path:
        return None
    path = path.split(os.pathsep)

    if sys.platform == "win32":
        # The current directory takes precedence on Windows.
        if os.curdir not in path:
            path.insert(0, os.curdir)

        # PATHEXT is necessary to check on Windows.
        pathext = os.environ.get("PATHEXT", "").split(os.pathsep)
        # See if the given file matches any of the expected path extensions.
        # This will allow us to short circuit when given "python.exe".
        # If it does match, only test that one, otherwise we have to try
        # others.
        if any(cmd.lower().endswith(ext.lower()) for ext in pathext):
            files = [cmd]
        else:
            files = [cmd + ext for ext in pathext]
    else:
        # On other platforms you don't have things like PATHEXT to tell you
        # what file suffixes are executable, so just pass on cmd as-is.
        files = [cmd]

    seen = set()
    for dir in path:
        normdir = os.path.normcase(dir)
        if normdir not in seen:
            seen.add(normdir)
            for thefile in files:
                name = os.path.join(dir, thefile)
                if _access_check(name, mode):
                    return name
    return None


class Popen(subprocess.Popen):
    """Python 2.7 backport."""
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.stdout:
            self.stdout.close()
        if self.stderr:
            self.stderr.close()
        if self.stdin:
            self.stdin.close()
        # Wait for the process to terminate, to avoid zombies.
        self.wait()
