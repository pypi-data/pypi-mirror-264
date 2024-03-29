from django.conf import settings
from django.shortcuts import render
from packaging import version

from rest_framework import permissions, views, response
from rest_framework.renderers import BaseRenderer

try:
    import rest_framework_swagger
    from rest_framework_swagger.renderers import SwaggerUIRenderer

    if version.parse(rest_framework_swagger.__version__) <= version.parse('2.1'):
        raise ImportError(
            'django-rest-swagger>2.1 version required'
            ' {} installed'.format(rest_framework_swagger.VERSION))            

except ImportError:
    class SwaggerUIRenderer(object):
        def __init__(self, *args, **kwargs):
            try:
                import rest_framework_swagger  # NOQA
            except ImportError:
                raise ImportError('django-rest-swagger required')

from .mixins import LoginRequiredMixin, FlowListMixin
from .. import schemas


class OpenAPIRenderer(BaseRenderer):
    media_type = 'application/openapi+json'
    charset = None
    format = 'openapi'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context['response'].status_code != status.HTTP_200_OK:
            return JSONRenderer().render(data)
        options = self.get_customizations()

        return OpenAPICodec().encode(data, **options)

    def get_customizations(self):
        """
        Adds settings, overrides, etc. to the specification.
        """
        data = {}
        if settings.SECURITY_DEFINITIONS:
            data['securityDefinitions'] = settings.SECURITY_DEFINITIONS

        return data


class ViewflowUIRenderer(SwaggerUIRenderer):
    def get_template(self):
        if 'material.frontend' in settings.INSTALLED_APPS:
            return 'viewflow/rest/swagger.html'
        return self.template

    def render(self, data, accepted_media_type=None, renderer_context=None):
        self.set_context(data, renderer_context)
        return render(
            renderer_context['request'],
            self.get_template(),
            renderer_context
        )


class SchemaView(LoginRequiredMixin, FlowListMixin, views.APIView):
    renderer_classes = [ViewflowUIRenderer, OpenAPIRenderer]
    schema_generator_class = schemas.SchemaGenerator
    permission_classes = [permissions.IsAuthenticated]
    exclude_from_schema = True

    title = 'Viewflow API'
    patterns = None

    def get(self, request, format=None):
        generator = self.schema_generator_class(
            title=self.title,
            url=self.request.path,
            patterns=self.patterns)
        schema = generator.get_schema(request=self.request)
        return response.Response(schema)
