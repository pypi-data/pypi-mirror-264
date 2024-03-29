from django.conf import settings
from packaging import version


default_app_config = 'viewflow.rest.apps.ViewflowRestConfig'  # NOQA

try:
    import rest_framework  # NOQA
except ImportError:
    raise ImportError('djangorestframework required')

if version.parse(rest_framework.VERSION) <= version.parse('3.7'):
    raise ImportError(
        'djangorestframework>3.7 version required'
        ' {} installed'.format(rest_framework.VERSION))

if version.parse(rest_framework.VERSION) >= version.parse('3.10'):
    schema_class = getattr(settings, 'REST_FRAMEWORK', {}).get('DEFAULT_SCHEMA_CLASS')
    if schema_class != 'rest_framework.schemas.coreapi.AutoSchema':
        raise ValueError(
            "Please set default schema class setting \nREST_FRAMEWORK={\n"
            "  ...\n"
            "  'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'\n"
            "  ...\n"
            "}"
        )


def register(flow_class, viewset_class=None):
    from django.apps import apps
    apps.get_app_config('viewflow_rest').register(flow_class, viewset_class=viewset_class)
    return flow_class
