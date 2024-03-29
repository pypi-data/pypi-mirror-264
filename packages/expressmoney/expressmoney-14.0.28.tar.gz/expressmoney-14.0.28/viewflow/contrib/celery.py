from __future__ import absolute_import

from django.db import connection
from django.urls import re_path
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from celery.result import AsyncResult

from ..activation import Activation, AbstractJobActivation, STATUS
from ..fields import get_task_ref
from ..flow import AbstractJob
from ..flow.views.actions import BaseTaskActionView
from ..flow.views.mixins import FlowTaskManagePermissionMixin


class RetryTaskView(FlowTaskManagePermissionMixin, BaseTaskActionView):
    """Retry the celery task."""

    action_name = 'retry'
    action_title = _('Retry')

    def can_proceed(self):
        """Check that node can be undone."""
        return self.activation.retry.can_proceed()

    def perform(self):
        """Undo the node."""
        self.activation.retry()
        self.success(_('Task {task} has been retried.'))


class RetryViewMixin(object):
    """Retry a celery task."""

    retry_view_class = RetryTaskView

    def __init__(self, *args, **kwargs):  # noqa D102
        self._retry_view = kwargs.pop('retry_view', None)
        super(RetryViewMixin, self).__init__(*args, **kwargs)

    @property
    def retry_view(self):
        """View for the admin to retry a task."""
        return self._retry_view if self._retry_view else self.retry_view_class.as_view()

    def urls(self):
        """Add `/<process_pk>/<task_pk>/retry/` url."""
        urls = super(RetryViewMixin, self).urls()
        urls.append(
            re_path(r'^(?P<process_pk>\d+)/{}/(?P<task_pk>\d+)/retry/$'.format(self.name),
                self.retry_view, {'flow_task': self}, name="{}__retry".format(self.name))
        )
        return urls

    def get_task_url(self, task, url_type='guess', namespace='', **kwargs):
        """Handle for url_type='retry'."""
        if url_type in ['retry']:
            url_name = '{}:{}__retry'.format(namespace, self.name)
            return reverse(url_name, args=[task.process_id, task.pk])
        return super(RetryViewMixin, self).get_task_url(task, url_type, namespace=namespace, **kwargs)


class JobActivation(AbstractJobActivation):
    @Activation.status.transition(
        source=[STATUS.NEW, STATUS.ASSIGNED, STATUS.SCHEDULED],
        target=STATUS.CANCELED)
    def cancel(self):
        """
        Cancel existing task
        """
        # Since we should have process lock grabbed at this place,
        # even if celery starts executing the task on a worker,
        # the task not started, so I think it's safe to terminate it
        AsyncResult(self.task.external_task_id).revoke(terminate=True)
        super(AbstractJobActivation, self).cancel.original()

    @Activation.status.transition(source=STATUS.ASSIGNED)
    def schedule(self):
        app = self.flow_task.job._get_app()
        eager = (
            getattr(app.conf, 'CELERY_ALWAYS_EAGER', False) or
            getattr(app.conf, 'task_always_eager', False)
        )
        if eager:
            self.set_status(STATUS.SCHEDULED)
            self.task.save()
            self.flow_task.job.apply(
                args=[get_task_ref(self.flow_task), self.task.process_id, self.task.pk],
                task_id=self.task.external_task_id)
        else:
            super(JobActivation, self).schedule.original()

    def run_async(self):
        """
        Async task schedule
        """
        apply_kwargs = {}
        if self.flow_task._eta is not None:
            apply_kwargs['eta'] = self.flow_task._eta(self.task)
        elif self.flow_task._delay is not None:
            delay = self.flow_task._delay
            if callable(delay):
                delay = delay(self.task)
            apply_kwargs['countdown'] = delay
        else:
            apply_kwargs['countdown'] = 1

        args = [get_task_ref(self.flow_task), self.task.process_id, self.task.pk]
        connection.on_commit(lambda: self.flow_task.job.apply_async(
            args=args, task_id=self.task.external_task_id, **apply_kwargs))


class Job(RetryViewMixin, AbstractJob):
    """
    Run celery a task in background

    Example.

    tasks.py::

        from celery import shared_task
        from viewflow.flow import flow_job


        @shared_task
        @flow_job
        def sample_task(activation):
             ...

    flows.py::

        from viewflow.contrib import celery

        class MyFlow(Flow):
            ...
            task = celery.Job(tasks.sample_task)
            ....

    .. note::
        With Django 1.8 you need to enable `django-transaction-hooks
        <https://pypi.python.org/pypi/django-transaction-hooks>`_
    """
    activation_class = JobActivation

    def __init__(self, *args, **kwargs):
        self._eta = None
        self._delay = None
        super(Job, self).__init__(*args, **kwargs)

    def Eta(self, eta_callable):
        """
        Expects callable that would get the task and return datetime for
        task execution
        """
        self._eta = eta_callable
        return self

    def Delay(self, delay):
        """
        Async task execution delay
        """
        self._delay = delay
        return self


try:
    from ..rest import views as rest

    class RJob(Job):
        """
        Run celery a task in background, REST-friendly views.
        """
        cancel_view_class = rest.CancelTaskView
        detail_view_class = rest.DetailTaskView
        perform_view_class = rest.PerformTaskView
        undo_view_class = rest.UndoTaskView
except:  # NOQA
    pass
