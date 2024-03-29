import copy

from django.urls import re_path
from django.urls import reverse

from .. import Node, mixins
from ..activation import Activation, STATUS


class ObsoleteActivation(Activation):
    @Activation.status.transition(
        source='*', target=STATUS.CANCELED,
        conditions=[lambda a: a.task.status != STATUS.CANCELED])
    def cancel(self):
        """
        Cancel existing task
        """
        super(ObsoleteActivation, self).cancel.original()


class Obsolete(mixins.TaskDescriptionMixin, Node):
    activation_class = ObsoleteActivation
    task_type = 'OBSOLETE'

    cancel_view_class = None
    detail_view_class = None

    shape = {
        'width': 0,
        'height': 0,
        'svg': ''
    }

    bpmn_element = None

    def __init__(self, *args, **kwargs):
        self._detail_view = kwargs.pop('detail_view', None)
        self._cancel_view = kwargs.pop('cancel_view', None)
        super(Obsolete, self).__init__(*args, **kwargs)

    def _outgoing(self):
        return
        yield

    @property
    def detail_view(self):
        return self._detail_view if self._detail_view else self.detail_view_class.as_view()

    @property
    def cancel_view(self):
        return self._cancel_view if self._cancel_view else self.cancel_view_class.as_view()

    def get_task_url(self, task, url_type='guess', namespace='', **kwargs):
        if url_type in ['detail', 'guess']:
            url_name = '{}:obsolete__detail'.format(namespace)
            return reverse(url_name, args=[task.process_id, task.pk])
        elif url_type in ['cancel']:
            url_name = '{}:obsolete__cancel'.format(namespace, self.name)
            return reverse(url_name, args=[task.process_id, task.pk])

    def urls(self):
        urls = super(Obsolete, self).urls()
        urls += [
            re_path(
                r'^(?P<process_pk>\d+)/obsolete/(?P<task_pk>\d+)/detail/$',
                self.detail_view, {'flow_task': self}, name="obsolete__detail"),
            re_path(
                r'^(?P<process_pk>\d+)/obsolete/(?P<task_pk>\d+)/cancel/$',
                self.cancel_view, {'flow_task': self}, name="obsolete__cancel")
        ]
        return urls

    def can_view(self, user, task):
        opts = self.flow_class.process_class._meta
        view_perm = "{}.view_{}".format(opts.app_label, opts.model_name)
        return user.has_perm(view_perm)

    def create_node(self, name):
        """
        Create real node instance for missing entry
        """
        obsolete = copy.copy(self)
        obsolete.name = name
        return obsolete
