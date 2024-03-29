import itertools

from django.apps import AppConfig
from django.urls import path, include, reverse

from material.frontend.apps import ModuleMixin
from material.frontend.urlconf import ModuleURLResolver

from django.utils.module_loading import autodiscover_modules


class ViewflowRestConfig(ModuleMixin, AppConfig):
    name = 'viewflow.rest'
    label = 'viewflow_rest'
    verbose_name = "Workflow API"
    icon = '<i class="material-icons">settings_input_component</i>'

    def __init__(self, app_name, app_module):
        super(ViewflowRestConfig, self).__init__(app_name, app_module)
        self._registry = {}

    def has_perm(self, user):
        return user.is_superuser

    def register(self, flow_class, viewset_class=None):
        from .viewset import FlowViewSet

        if flow_class not in self._registry:
            if viewset_class is None:
                viewset_class = FlowViewSet

            self._registry[flow_class] = viewset_class(flow_class=flow_class)

    def ready(self):
        autodiscover_modules('flows', register_to=self)

    def index_url(self):
        return reverse('viewflow_rest:index')

    @property
    def urls(self):
        from . import views

        base_url = '^workflow/api/'

        patterns = [
            path('flows/', views.FlowListView.as_view(ns_map=self.ns_map), name="flow_list"),
            path('processes/', views.AllProcessListView.as_view(ns_map=self.ns_map), name="process_list"),
            path('tasks/', views.AllTaskListView.as_view(ns_map=self.ns_map), name="task_list"),
        ]

        for flow_class, flow_router in self._registry.items():
            flow_label = flow_class._meta.app_label
            patterns += [
                path('', include((flow_router.urls, flow_label)))
            ]

        patterns += [
            path('', views.SchemaView.as_view(patterns=patterns, ns_map=self.ns_map), name="index"),
        ]

        patterns = [
            path('', (patterns, self.label, self.label))
        ]

        return ModuleURLResolver(
            base_url, patterns, module=self)

    @property
    def ns_map(self):
        return {
            flow_class._meta.app_label: flow_class for flow_class, flow_site in self._registry.items()
        }


class ViewflowRestNSConfig(ViewflowRestConfig):
    @property
    def urls(self):
        from . import views

        base_url = '^workflow/api/'

        patterns = [
            path('flows/', views.FlowListView.as_view(ns_map=self.ns_map), name="flow_list"),
            path('processes/', views.AllProcessListView.as_view(ns_map=self.ns_map), name="process_list"),
            path('tasks/', views.AllTaskListView.as_view(ns_map=self.ns_map), name="task_list"),
        ]

        items = sorted(self._registry.items(), key=lambda item: item[0]._meta.app_label)
        app_flows = itertools.groupby(
            items, lambda item: item[0]._meta.app_label)

        for app_label, items in app_flows:
            app_views = []
            for flow_class, flow_router in items:
                flow_label = flow_class._meta.flow_label
                app_views.append(
                    path('{}/'.format(flow_label), include((flow_router.urls, flow_label)))
                )

            patterns.append(
                path('{}/'.format(app_label), include((app_views, app_label)))
            )

        patterns += [
            path('', views.SchemaView.as_view(patterns=patterns, ns_map=self.ns_map), name="index"),
        ]

        patterns = [
            path('', (patterns, self.label, self.label))
        ]

        return ModuleURLResolver(
            base_url, patterns, module=self)

    @property
    def ns_map(self):
        return {
            "{}:{}".format(
                flow_class._meta.app_label,
                flow_class._meta.flow_label): flow_class
            for flow_class, flow_site in self._registry.items()
        }
