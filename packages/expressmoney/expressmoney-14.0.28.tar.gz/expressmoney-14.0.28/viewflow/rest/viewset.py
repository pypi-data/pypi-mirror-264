from django.urls import path, include, re_path

from . import views


class FlowViewSet(object):
    """
    Shortcut for flow urls routing

    Usage::

        urlpatterns = [
            url(r'^', include(FlowRouter(HelloWorldFlow).urls), namespace='helloworld')
        ]
    """
    flow_detail_view = [
        r'^flows/{flow_label}/$',
        views.DetailFlowView.as_view(),
        'flow'
    ]

    flow_chart_view = [
        r'^flows/{flow_label}/chart/$',
        views.FlowChartView.as_view(),
        'chart'
    ]

    process_list_view = [
        r'^processes/{flow_label}/$',
        views.ProcessListView.as_view(),
        'detail'
    ]

    process_detail_view = [
        r'^processes/{flow_label}/(?P<process_pk>\d+)/$',
        views.DetailProcessView.as_view(),
        'detail'
    ]

    task_list_view = [
        '^tasks/{flow_label}/$',
        views.TaskListView.as_view(),
        'task-list'
    ]

    def __init__(self, flow_class):
        self.flow_class = flow_class

    def create_url_entry(self, url_entry):
        regexp_template, view, name = url_entry
        regexp = regexp_template.format(flow_label=self.flow_class._meta.flow_label)
        return re_path(regexp, view, name=name)

    def get_list_urls(self):
        attrs = (getattr(self, attr) for attr in dir(self) if attr.endswith('_view'))
        return [
            self.create_url_entry(value)
            for value in attrs if isinstance(value, (list, tuple))
        ]

    @property
    def urls(self):
        flow_label = self.flow_class._meta.flow_label
        return [
            path('', include(self.get_list_urls()), {'flow_class': self.flow_class}),
            path('tasks/{}/'.format(flow_label), include([self.flow_class.instance.urls]))
        ]
