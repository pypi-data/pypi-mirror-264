from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from django_filters import CharFilter, ChoiceFilter, DateRangeFilter, ModelChoiceFilter
from django_filters.rest_framework import FilterSet

from rest_framework.compat import coreapi
from django_filters.rest_framework import DjangoFilterBackend as BaseDjangoFilterBackend

from ..activation import STATUS
from ..fields import import_task_by_ref
from .. import models

DATERANGE_HELP = """
"empty" - Any date<br/>
1 - Today<br/>
2 - Past 7 days<br/>
3 - This month<br/>
4 - This year<br/>
5 - Yesterday<br/>
"""

STATUS_HELP = """
"empty" - All
NEW - Active
CANCELED - Canceled
DONE - Completed
"""


class ProcessFilter(FilterSet):
    flow_class = CharFilter(help_text="'Flow class reference, ex: hellorest/flows.HelloRestFlow")
    status = ChoiceFilter(choices=(
        (None, _('All')),
        (STATUS.NEW, _('Active')),
        (STATUS.CANCELED, _('Canceled')),
        (STATUS.DONE, _('Completed')),
    ), help_text=STATUS_HELP)
    created = DateRangeFilter(help_text=DATERANGE_HELP)
    finished = DateRangeFilter(help_text=DATERANGE_HELP)

    class Meta:
        model = models.Process
        exclude = ['data', ]


class TaskListFilter(ChoiceFilter):
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', None)
        if choices is None:
            choices = (
                (None, _('All')),
                ('INBOX', _('Inbox')),
                ('QUEUE', _('Queue')),
                ('ARCHIVE', _('Archive')),
                ('ACTIVE', _('Active')),
            )

        super(TaskListFilter, self).__init__(choices=choices, *args, **kwargs)

    def filter(self, qs, value):
        """
        Dump stub. All filter logic is in view
        """
        return qs


class TaskFilter(FilterSet):
    flow_task = ChoiceFilter(help_text='Flow task ref, for example: hellorest/flows.HelloRestFlow.approve')
    created = DateRangeFilter(help_text=DATERANGE_HELP)
    process_id = ModelChoiceFilter(queryset=models.Process.objects.all(), help_text='')
    task_list = TaskListFilter(help_text="Empty or one of: INBOX, QUEUE, ARCHIVE, ACTIVE")

    def __init__(self, data=None, queryset=None, **kwargs):
        if queryset is None:
            queryset = models.Task._default_manager.all()

        super(TaskFilter, self).__init__(data=data, queryset=queryset, **kwargs)
        self.filters['process_id'].field.queryset = \
            models.Process.objects.filter(id__in=queryset.values_list('process', flat=True))

        def task_name(task_ref):
            flow_task = import_task_by_ref(task_ref)
            return "{}/{}".format(flow_task.flow_class.process_title, flow_task.name.title())

        tasks = [(task_ref, task_name(task_ref))
                 for task_ref in queryset.order_by('flow_task').distinct().values_list('flow_task', flat=True)]
        if 'flow_task' in self.data and not any(task[0] == self.data['flow_task'] for task in tasks):
            tasks += [(self.data['flow_task'],  self.data['flow_task'])]

        self.filters['flow_task'].field.choices = [(None, 'All')] + tasks
        self.form['flow_task'].field.choices = [(None, 'All')] + tasks

    class Meta:
        fields = ['flow_task', 'created']
        model = models.Task
        exclude = ['data', ]


class DjangoFilterBackend(BaseDjangoFilterBackend):
    def get_fields(self, view):
        filter_class = getattr(view, 'filter_class', None)
        result = []
        for filter_name, filter_field in filter_class().filters.items():
            description = ''
            if hasattr(filter_field.field, 'choices') and filter_field.field.choices:
                description += '\n' + '  '.join(
                    "<br/>{} - {}".format(choice[0] or '"empty"', choice[1])
                    for choice in filter_field.field.choices)
            result.append(
                coreapi.Field(
                    filter_name, required=False, location='query',
                    description=force_str(filter_field.field.help_text)))
        return result
