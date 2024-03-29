try:
    from django.urls import (  # noqa
        URLPattern,
        URLResolver,
    )
except ImportError:
    # Will be removed in Django 2.0
    from django.urls import (  # noqa
        RegexURLPattern as URLPattern,
        RegexURLResolver as URLResolver,
    )


from rest_framework.request import clone_request
from rest_framework.schemas import (    
    SchemaGenerator as BaseSchemaGenerator,
)
from rest_framework.schemas.generators import (
    EndpointEnumerator as BaseEndpointEnumerator
)

try:
    from rest_framework.schemas.coreapi import insert_into, LinkNode
except ImportError:
    from rest_framework.schemas.generators import insert_into, LinkNode

from ..activation import Activation


def get_regex_pattern(urlpattern):
    if hasattr(urlpattern, 'pattern'):
        # Django 2.0
        return urlpattern.pattern.regex.pattern
    else:
        # Django < 2.0
        return urlpattern.regex.pattern


class EndpointEnumerator(BaseEndpointEnumerator):
    def get_api_endpoints(self, patterns=None, prefix='', default_kwargs=None):
        """
        Return a list of all available API endpoints by inspecting the URL conf.
        """
        if patterns is None:
            patterns = self.patterns

        if default_kwargs is None:
            default_kwargs = {}

        api_endpoints = []

        for pattern in patterns:
            path_regex = prefix + get_regex_pattern(pattern)
            if isinstance(pattern, URLPattern):
                default_kwargs = default_kwargs.copy()
                default_kwargs.update(pattern.default_args)

                path = self.get_path_from_regex(path_regex)
                callback = pattern.callback
                if self.should_include_endpoint(path, callback):
                    for method in self.get_allowed_methods(callback):
                        endpoint = (path, method, callback, default_kwargs)
                        api_endpoints.append(endpoint)

            elif isinstance(pattern, URLResolver):
                default_kwargs = default_kwargs.copy()
                default_kwargs.update(pattern.default_kwargs)
                nested_endpoints = self.get_api_endpoints(
                    patterns=pattern.url_patterns,
                    prefix=path_regex,
                    default_kwargs=default_kwargs
                )
                api_endpoints.extend(nested_endpoints)

        return api_endpoints


class SchemaGenerator(BaseSchemaGenerator):
    endpoint_inspector_cls = EndpointEnumerator

    def get_links(self, request=None):
        """
        Return a dictionary containing all the links that should be
        included in the API schema.
        """
        links = LinkNode()

        # Generate (path, method, view) given (path, method, callback).
        paths = []
        view_endpoints = []
        for path, method, callback, kwargs in self.endpoints:
            view = self.create_view(callback, method, kwargs, request)
            path = self.coerce_path(path, method, view)
            paths.append(path)
            view_endpoints.append((path, method, callback, view))

        # Only generate the path prefix for paths that will be included
        if not paths:
            return None
        prefix = self.determine_path_prefix(paths)

        for path, method, callback, view in view_endpoints:
            if not self.has_view_permissions(path, method, view):
                continue
            link = view.schema.get_link(path, method, base_url=self.url)
            subpath = path[len(prefix):]
            keys = self.get_keys(subpath, method, callback, view)
            insert_into(links, keys, link)

        return links

    def create_view(self, callback, method, kwargs, request=None):
        """
        Given a callback, return an actual view instance.
        """
        view = callback.cls()
        for attr, val in getattr(callback, 'initkwargs', {}).items():
            setattr(view, attr, val)
        view.args = ()
        view.kwargs = kwargs
        view.format_kwarg = None
        view.request = None
        view.action_map = getattr(callback, 'actions', None)

        actions = getattr(callback, 'actions', None)
        if actions is not None:
            if method == 'OPTIONS':
                view.action = 'metadata'
            else:
                view.action = actions.get(method.lower())

        if request is not None:
            view.request = clone_request(request, method)
            if 'flow_class' in kwargs and 'flow_task' in kwargs:
                view.request.activation = Activation()
                view.request.activation.flow_class = kwargs['flow_class']
                view.request.activation.flow_task = kwargs['flow_task']

        return view

    def get_keys(self, subpath, method, callback, view):
        prefix = ''
        if hasattr(callback, 'cls'):
            if 'ns_map' in callback.initkwargs:
                return ["__all__", str(view)]
            elif 'flow_class' in view.kwargs:
                prefix = '{}/{}/'.format(
                    subpath.split('/')[1],
                    "tasks")
                if 'flow_task' in view.kwargs:
                    return (
                        prefix + view.kwargs['flow_task'].name,
                        str(view)
                    )
                else:
                    return ("{}/".format(view.kwargs['flow_class']._meta.flow_label), str(view))

        return super(SchemaGenerator, self).get_keys(subpath, method, view)
