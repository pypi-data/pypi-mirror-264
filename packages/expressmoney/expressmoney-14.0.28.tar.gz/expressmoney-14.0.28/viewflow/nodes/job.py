from .. import Task, mixins


class AbstractJob(mixins.TaskDescriptionMixin,
                  mixins.NextNodeMixin,
                  mixins.UndoViewMixin,
                  mixins.CancelViewMixin,
                  mixins.DetailViewMixin,
                  Task):
    """
    Base class for task that runs in background.

    Example::

        job = (
            flow.Job(task.job)
            .Next(this.end)
        )
    """

    task_type = 'JOB'

    shape = {
        'width': 150,
        'height': 100,
        'text-align': 'middle',
        'svg': """
            <rect class="task" width="150" height="100" rx="5" ry="5"/>
            <path class="task-label"
                  d="M19.43 12.98c.04-.32.07-.64.07-.98s-.03-.66-.07-.98l2.11-1.65
                     c.19-.15.24-.42.12-.64l-2-3.46c-.12-.22-.39-.3-.61-.22l-2.49 1
                     c-.52-.4-1.08-.73-1.69-.98l-.38-2.65 C14.46 2.18 14.25 2 14 2
                     h-4c-.25 0-.46.18-.49.42l-.38 2.65c-.61.25-1.17.59-1.69.98l-2.49-1
                     c-.23-.09-.49 0-.61.22 l-2 3.46c-.13.22-.07.49.12.64l2.11 1.65
                     c-.04.32-.07.65-.07.98s.03.66.07.98l-2.11 1.65c-.19.15-.24.42-.12.64
                     l2 3.46c.12.22.39.3.61.22l2.49-1c.52.4 1.08.73 1.69.98l.38 2.65
                     c.03.24.24.42.49.42h4c.25 0 .46-.18.49-.42l.38-2.65
                     c.61-.25 1.17-.59 1.69-.98l2.49 1c.23.09.49 0 .61-.22l2-3.46
                     c.12-.22.07-.49-.12-.64l-2.11-1.65zM12 15.5c-1.93 0-3.5-1.57-3.5-3.5
                     s1.57-3.5 3.5-3.5 3.5 1.57 3.5 3.5-1.57 3.5-3.5 3.5z"/>
        """
    }

    bpmn_element = 'scriptTask'

    def __init__(self, job, **kwargs):  # noqa D102
        super(AbstractJob, self).__init__(**kwargs)
        self._job = job

    @property
    def job(self):
        """Callable that should start the job in background."""
        return self._job
