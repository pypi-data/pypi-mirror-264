from __future__ import unicode_literals

import six

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
try:
    # django 3.0+
    from django.utils.http import url_has_allowed_host_and_scheme as is_safe_url
except ImportError:
    from django.utils.http import is_safe_url

from django.utils.safestring import mark_safe
from django.views import generic
from django.views.generic.base import TemplateResponseMixin

from material.frontend import frontend_url
from material.frontend.views.list import DataTableMixin, FilterMixin

from ..import chart
from ..fields import get_task_ref

from ..compat import _
from ..flow.views.mixins import FlowListMixin, FlowViewPermissionMixin
from ..models import Task
from . import filters


@method_decorator(login_required, name='dispatch')
class BaseTasksActionView(FlowListMixin, generic.FormView):
    """Base for action view for multiple tasks."""

    action_name = None
    success_url = 'viewflow:index'
    template_name = 'viewflow/site_task_action.html'
    model = Task

    def get_tasks(self, user, task_pks):
        raise NotImplementedError

    def get_success_url(self):
        """Continue to the flow index or redirect according `?back` parameter."""
        if 'back' in self.request.GET:
            back_url = self.request.GET['back']
            if not is_safe_url(url=back_url, allowed_hosts={self.request.get_host()}):
                back_url = '/'
            return back_url

        return reverse(self.success_url)

    def get_form_class(self):
        class ActionForm(forms.Form):
            pk = forms.ModelMultipleChoiceField(
                queryset=Task._default_manager.all(),
                widget=forms.MultipleHiddenInput)
        return ActionForm

    def report(self, message, level=messages.INFO, fail_silently=True, **kwargs):
        """Send a notification with link to the tasks.

        :param message: A message template.
        :param level: A level, one of https://docs.djangoproject.com/en/1.10/ref/contrib/messages/#message-levels
        :param fail_silently: Raise a error if messaging framework is not installed.
        :param kwargs: Additional parametes used in format message templates.

        A `message_template` prepared by python `.format()`
        function. In addition to `kwargs`, the `{tasks}` parameter passed.

        Example::

            self.report('{process} has been cancelled.')

        """
        tasks_links = []
        for task in self.tasks:
            task_url = self.get_task_url(task, url_type='detail')
            task_link = '<a href="{task_url}">#{task_pk}</a>'.format(task_url=task_url, task_pk=task.pk)
            tasks_links.append(task_link)

        kwargs.update({
            'tasks': ' '.join(tasks_links)
        })

        message = mark_safe(_(message).format(**kwargs))

        messages.add_message(self.request, level, message, fail_silently=fail_silently)

    def success(self, message, fail_silently=True, **kwargs):
        """Notification about successful operation."""
        self.report(message, level=messages.SUCCESS, fail_silently=fail_silently, **kwargs)

    def error(self, message, fail_silently=True, **kwargs):
        """Notification about an error."""
        self.report(message, level=messages.ERROR, fail_silently=fail_silently, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

    def form_not_confirmed(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        self.form = self.get_form()
        self.tasks = self.get_tasks()

        if self.form.is_valid():
            self.tasks = self.form.cleaned_data['pk']
            if '_confirm' in self.request.POST:
                return self.form_valid(self.form)
            else:
                return self.form_not_confirmed(self.form)
        else:
            return self.form_invalid(self.form)


class TasksUnAssignView(BaseTasksActionView):
    """Deassign multiple tasks."""

    action_name = 'unassign'

    def get_tasks(self):
        """List of tasks assigned to the user."""
        return self.model.objects.inbox(
            self.flows, self.request.user
        ).filter(
            pk__in=self.request.POST.getlist('pk')
        )

    def form_valid(self, form):
        """Deassign tasks from the user."""
        for task in self.tasks:
            lock = task.process.flow_class.lock_impl(task.process.flow_class.instance)
            with lock(task.process.flow_class, task.process_id):
                activation = task.activate()
                activation.unassign()
        self.success('Tasks {tasks} has been unassigned.')
        return HttpResponseRedirect(self.get_success_url())


class TasksAssignView(BaseTasksActionView):
    """Assign multiple tasks."""

    action_name = 'assign'

    def get_tasks(self):
        """List of tasks assigned to the user."""
        return self.model.objects.queue(
            self.flows, self.request.user
        ).filter(
            pk__in=self.request.POST.getlist('pk')
        )

    def form_valid(self, form):
        """Assign tasks to the current user."""
        for task in self.tasks:
            lock = task.process.flow_class.lock_impl(task.process.flow_class.instance)
            with lock(task.process.flow_class, task.process_id):
                activation = task.activate()
                activation.assign(self.request.user)

        self.success('Tasks {tasks} has been assigned.')
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class AllTaskListView(FlowListMixin,
                      TemplateResponseMixin,
                      FilterMixin,
                      DataTableMixin,
                      generic.View):
    model = Task
    list_display = [
        'task_hash', 'description', 'process_summary', 'process_url', 'created'
    ]
    filterset_class = filters.TaskFilter
    template_name = 'viewflow/site_tasks.html'

    @property
    def list_actions(self):
        namespace = self.request.resolver_match.namespace
        return [
            (
                _('Unassign selected tasks'),
                frontend_url(self.request, reverse('{}:unassign'.format(namespace)), back_link='here')
            )
        ]

    def task_hash(self, task):
        task_url = frontend_url(self.request, self.get_task_url(task), back_link='here')
        return mark_safe('<a href="{}">{}/{}</a>'.format(task_url, task.process.id, task.pk))
    task_hash.short_description = _("#")

    def description(self, task):
        summary = task.summary()
        if not summary:
            summary = task.flow_task
        task_url = frontend_url(self.request, self.get_task_url(task), back_link='here')
        return mark_safe('<a href="{}">{}</a>'.format(task_url, summary))
    description.short_description = _('Task Description')

    def process_summary(self, task):
        return task.flow_process.summary()
    process_summary.short_description = _('Process Summary')

    def process_url(self, task):
        process_url = frontend_url(self.request, self.get_process_url(task.process), back_link='here')
        return mark_safe('<a href="{}">{} #{}</a>'.format(
            process_url, task.process.flow_class.process_title, task.process.pk))
    process_url.short_description = _('Process URL')

    def get_queryset(self):
        """Filtered task list."""
        queryset = self.model.objects.inbox(self.flows, self.request.user)
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, six.string_types):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


@method_decorator(login_required, name='dispatch')
class AllQueueListView(
        FlowListMixin,
        TemplateResponseMixin,
        FilterMixin,
        DataTableMixin,
        generic.View):
    list_display = [
        'task_hash', 'description', 'process_summary',
        'process_url', 'created'
    ]
    filterset_class = filters.TaskFilter
    model = Task
    template_name = 'viewflow/site_queue.html'

    @property
    def list_actions(self):
        namespace = self.request.resolver_match.namespace
        return [
            (
                _('Assign selected tasks'),
                frontend_url(self.request, reverse('{}:assign'.format(namespace)), back_link='here')
            )
        ]

    def task_hash(self, task):
        task_url = frontend_url(self.request, self.get_task_url(task), back_link='here')
        return mark_safe('<a href="{}">{}/{}</a>'.format(task_url, task.process.id, task.pk))
    task_hash.short_description = _("#")

    def description(self, task):
        summary = task.summary()
        if not summary:
            summary = task.flow_task
        task_url = frontend_url(self.request, self.get_task_url(task), back_link='here')
        return mark_safe('<a href="{}">{}</a>'.format(task_url, summary))
    description.short_description = _('Task Description')

    def process_summary(self, task):
        return task.flow_process.summary()
    process_summary.short_description = _('Process Summary')

    def process_url(self, task):
        process_url = frontend_url(self.request, self.get_process_url(task.process), back_link='here')
        return mark_safe('<a href="{}">{} #{}</a>'.format(
            process_url, task.process.flow_class.process_title, task.process.pk))
    process_url.short_description = _('Process URL')

    def get_queryset(self):
        """Filtered task list."""
        queryset = self.model.objects.queue(self.flows, self.request.user)
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, six.string_types):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


@method_decorator(login_required, name='dispatch')
class AllArchiveListView(FlowListMixin,
                         TemplateResponseMixin,
                         DataTableMixin,
                         generic.View):
    list_display = [
        'task_hash', 'description', 'started',
        'finished', 'process_title', 'process_summary',
    ]
    model = Task
    template_name = 'viewflow/site_archive.html'

    def task_hash(self, task):
        task_url = frontend_url(self.request, self.get_task_url(task), back_link='here')
        return mark_safe('<a href="{}">{}/{}</a>'.format(task_url, task.process.id, task.pk))
    task_hash.short_description = _("#")

    def description(self, task):
        summary = task.summary()
        if not summary:
            summary = task.flow_task
        task_url = frontend_url(self.request, self.get_task_url(task), back_link='here')
        return mark_safe('<a href="{}">{}</a>'.format(task_url, summary))
    description.short_description = _('Task Description')

    def process_title(self, task):
        process_url = frontend_url(self.request, self.get_process_url(task.process), back_link='here')
        return mark_safe('<a href="{}">{} #{}</a>'.format(
            process_url, task.flow_task.flow_class.process_title, task.process.pk))
    process_title.short_description = _('Process')

    def process_summary(self, task):
        process_url = frontend_url(self.request, self.get_process_url(task.process), back_link='here')
        return mark_safe('<a href="{}">{}</a>'.format(
            process_url, task.flow_process.summary()))
    process_summary.short_description = _('Process Summary')

    def get_queryset(self):
        """All tasks from all processes assigned to the current user."""
        queryset = self.model.objects.archive(self.flows, self.request.user)
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, six.string_types):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


@method_decorator(login_required, name='dispatch')
class ProcessDashboardView(FlowViewPermissionMixin,
                           generic.TemplateView):
    def get_context_data(self, **kwargs):
        sorted_nodes, _ = chart.topsort(self.flow_class)
        nodes = [
            node for node in sorted_nodes
            if node.task_type in ['HUMAN', 'JOB']
        ]
        end_nodes = [
            node for node in sorted_nodes
            if node.task_type in ['END']
        ]

        columns = []
        for node in nodes:
            columns.append({
                'node': node,
                'node_ref': get_task_ref(node),
                'tasks': self.flow_class.task_class._default_manager.filter_available(
                    [self.flow_class], self.request.user
                ).filter(
                    finished__isnull=True,
                    flow_task=node
                )[:26]
            })

        finished = self.flow_class.task_class._default_manager.filter_available(
            [self.flow_class], self.request.user
        ).filter(
            finished__isnull=False,
            flow_task__in=end_nodes
        )[:26]

        return super(ProcessDashboardView, self).get_context_data(
            columns=columns, end_nodes=end_nodes, finished=finished, **kwargs)

    def get_template_names(self):
        """List of template names to be used for an queue list view.

        If `template_name` is None, default value is::

            [<app_label>/<flow_label>/process_dashboard.html,
             'viewflow/flow/process_dashboard.html']
        """
        if self.template_name is None:
            opts = self.flow_class._meta

            return (
                '{}/{}/process_dashboard.html'.format(opts.app_label, opts.flow_label),
                'viewflow/flow/process_dashboard.html')
        else:
            return [self.template_name]


@method_decorator(login_required, name='dispatch')
class ProcessListView(FlowViewPermissionMixin,
                      TemplateResponseMixin,
                      FilterMixin,
                      DataTableMixin,
                      generic.View):
    list_display = [
        'process_id', 'process_summary',
        'created', 'finished', 'active_tasks'
    ]
    filterset_class = filters.ProcessFilter

    def get_process_link(self, process):
        url_name = '{}:detail'.format(self.request.resolver_match.namespace)
        return reverse(url_name, args=[process.pk])

    def process_id(self, process):
        return mark_safe('<a href="{}">{}</a>'.format(
            self.get_process_link(process),
            process.pk)
        )
    process_id.short_description = '#'

    def process_summary(self, process):
        return mark_safe('<a href="{}">{}</a>'.format(
            self.get_process_link(process),
            process.summary())
        )
    process_summary.short_description = 'Summary'

    def active_tasks(self, process):
        if process.finished is None:
            return mark_safe('<a href="{}">{}</a>'.format(
                self.get_process_link(process),
                process.active_tasks().count())
            )
        return ''
    active_tasks.short_description = _('Active Tasks')

    def get_template_names(self):
        """List of template names to be used for an queue list view.

        If `template_name` is None, default value is::

            [<app_label>/<flow_label>/process_list.html,
             'viewflow/flow/process_list.html']
        """
        if self.template_name is None:
            opts = self.flow_class._meta

            return (
                '{}/{}/process_list.html'.format(opts.app_label, opts.flow_label),
                'viewflow/flow/process_list.html')
        else:
            return [self.template_name]

    def get_queryset(self):
        """Filtered process list."""
        process_class = self.flow_class.process_class
        self.model = process_class
        queryset = process_class.objects.filter(flow_class=self.flow_class)
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, six.string_types):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


class TaskListView(FlowViewPermissionMixin,
                   TemplateResponseMixin,
                   FilterMixin,
                   DataTableMixin,
                   generic.View):
    list_display = [
        'task_hash', 'description', 'process_summary', 'process_url', 'created'
    ]
    filterset_class = filters.TaskFilter
    model = Task
    template_name = 'viewflow/flow/tasks_history.html'

    def get_task_url(self, task, url_type=None):
        namespace = self.request.resolver_match.namespace
        return task.flow_task.get_task_url(
            task, url_type=url_type if url_type else 'guess',
            user=self.request.user,
            namespace=namespace)

    def task_hash(self, task):
        task_url = frontend_url(self.request, self.get_task_url(task), back_link='here')
        return mark_safe('<a href="{}">{}/{}</a>'.format(task_url, task.process.id, task.pk))
    task_hash.short_description = "#"

    def description(self, task):
        summary = task.summary()
        if not summary:
            summary = task.flow_task
        task_url = frontend_url(self.request, self.get_task_url(task), back_link='here')
        return mark_safe('<a href="{}">{}</a>'.format(task_url, summary))

    def process_summary(self, task):
        return task.flow_process.summary()

    def process_url(self, task):
        namespace = self.request.resolver_match.namespace
        process_url = reverse('{}:detail'.format(namespace), args=[task.process.pk])
        process_url = frontend_url(self.request, process_url, back_link='here')
        return mark_safe('<a href="{}">{} #{}</a>'.format(
            process_url, task.process.flow_class.process_title, task.process.pk))
    process_url.short_description = 'Process Summary'

    def get_queryset(self):
        """All tasks from all processes assigned to the current user."""
        queryset = Task.objects.filter_available([self.flow_class], self.request.user)
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, six.string_types):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


class FlowChartView(generic.View):
    def get(self, request, *args, **kwargs):
        flow_class = kwargs['flow_class']
        process_pk = kwargs.get('process_pk')

        grid = chart.calc_layout_data(flow_class)
        if process_pk is not None:
            chart.calc_cell_status(flow_class, grid, process_pk)
        svg = chart.grid_to_svg(grid)

        return HttpResponse(svg, content_type="image/svg+xml")
