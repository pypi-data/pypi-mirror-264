from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet, ChoiceFilter, DateRangeFilter, ModelChoiceFilter


from ..activation import STATUS
from ..fields import import_task_by_ref
from ..models import Process, Task


class ProcessFilter(FilterSet):
    status = ChoiceFilter(help_text='', choices=(
        (None, _('All')),
        (STATUS.NEW, _('Active')),
        (STATUS.CANCELED, _('Canceled')),
        (STATUS.DONE, _('Completed')),
    ))
    created = DateRangeFilter(help_text='')
    finished = DateRangeFilter(help_text='')

    class Meta:
        fields = ['status', 'created', 'finished']
        model = Process


class TaskFilter(FilterSet):
    flow_task = ChoiceFilter(help_text='')
    created = DateRangeFilter(help_text='')
    process = ModelChoiceFilter(queryset=Process.objects.all(), help_text='')

    def __init__(self, data=None, queryset=None, **kwargs):
        super(TaskFilter, self).__init__(data=data, queryset=queryset, **kwargs)

        # All processes in the queryset
        self.filters['process'].field.queryset = Process.objects.filter(
            id__in=queryset.values_list('process', flat=True)
        )

        # All task types in the queryset
        def task_name(task_ref):
            flow_task = import_task_by_ref(task_ref)
            return "{}/{}".format(flow_task.flow_class.process_title, flow_task.name.title())

        tasks = queryset.order_by('flow_task').values_list('flow_task', flat=True).distinct()
        tasks = [(task_ref, task_name(task_ref))
                 for task_ref in tasks]

        self.filters['flow_task'].field.choices = [(None, _('All'))] + tasks

    class Meta:
        fields = ['process', 'flow_task', 'created']
        model = Task
