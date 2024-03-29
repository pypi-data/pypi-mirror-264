from django.utils.decorators import method_decorator
from django.utils.timezone import now

from .. import Gateway, mixins, signals
from ..activation import Activation, StartActivation, STATUS
from ..decorators import flow_start_func
from . import func


class StartSubprocessActivation(StartActivation):
    @Activation.status.super()
    def prepare(self, parent_task):
        self.process.parent_task = parent_task
        super(StartSubprocessActivation, self).prepare.original()


class StartSubprocess(func.StartFunction):
    activation_class = StartSubprocessActivation

    shape = {
        'width': 50,
        'height': 50,
        'svg': """
            <circle class="event" cx="25" cy="25" r="25"/>
        """
    }

    bpmn_element = "startEvent"

    @method_decorator(flow_start_func)
    def start_func_default(self, activation, parent_task):
        activation.prepare(parent_task)
        activation.done()
        return activation


class SubprocessActivation(Activation):
    def subprocesses(self):
        subcls = self.flow_task.subflow_task.flow_class.process_class
        return subcls._default_manager.filter(parent_task=self.task)

    @Activation.status.transition(source=STATUS.NEW, target=STATUS.STARTED)
    def start(self):
        with self.exception_guard():
            self.task.started = now()
            self.task.save()

            self.flow_task.subflow_task.run(self.task)

            signals.task_started.send(sender=self.flow_class, process=self.process, task=self.task)

    def is_done(self):
        unfinished = self.subprocesses().exclude(status__in=[STATUS.DONE, STATUS.CANCELED])
        return not unfinished.exists()

    @Activation.status.transition(source=STATUS.STARTED, target=STATUS.DONE)
    def done(self):
        """
        Mark task as done
        .. seealso::
            :data:`viewflow.signals.task_finished`
        """
        self.task.finished = now()
        self.set_status(STATUS.DONE)
        self.task.save()

        signals.task_finished.send(sender=self.flow_class, process=self.process, task=self.task)

        self.activate_next()

    @Activation.status.transition(source=STATUS.DONE)
    def activate_next(self):
        """
        Activate all outgoing edges.
        """
        self.flow_task._next.activate(prev_activation=self, token=self.task.token)

    @classmethod
    def activate(cls, flow_task, prev_activation, token):
        flow_class = flow_task.flow_class
        process = prev_activation.process

        task = flow_class.task_class(
            process=process,
            flow_task=flow_task,
            token=token)

        task.save()
        task.previous.add(prev_activation.task)

        activation = cls()
        activation.initialize(flow_task, task)

        activation.start()

        return activation


class Subprocess(mixins.TaskDescriptionMixin,
                 mixins.NextNodeMixin,
                 mixins.DetailViewMixin,
                 Gateway):
    task_type = 'SUBPROCESS'
    activation_class = SubprocessActivation

    shape = {
        'width': 150,
        'height': 100,
        'text-align': 'middle',
        'svg': """
            <rect class="task" width="150" height="100" rx="5" ry="5" style="stroke-width:5"/>
        """
    }

    bpmn_element = "subProcess"

    def __init__(self, subflow_task, **kwargs):
        self.subflow_task = subflow_task
        super(Subprocess, self).__init__(**kwargs)

    def on_flow_finished(self, **signal_kwargs):
        process = signal_kwargs['process']

        if process.parent_task and process.parent_task.flow_task == self:
            parent_flow_class = process.parent_task.flow_task.flow_class
            lock = parent_flow_class.lock_impl(parent_flow_class.instance)

            with lock(parent_flow_class, process.parent_task.process_id):
                activation = self.activation_class()

                activation.initialize(self, process.parent_task)
                if activation.is_done():
                    activation.done()

    def ready(self):
        signals.flow_finished.connect(self.on_flow_finished, sender=self.subflow_task.flow_class)


class NSubprocessActivation(SubprocessActivation):
    @Activation.status.transition(source=STATUS.NEW, target=STATUS.STARTED)
    def start(self):
        with self.exception_guard():
            self.task.started = now()
            self.task.save()

            for item in self.flow_task.subitem_source(self.process):
                    self.flow_task.subflow_task.run(self.task, item)

            signals.task_started.send(sender=self.flow_class, process=self.process, task=self.task)


class NSubprocess(Subprocess):
    """
    Starts several subprocesses and continues main flow when all subprocess completes
    """
    task_type = 'SUBPROCESS'
    activation_class = NSubprocessActivation

    shape = {
        'width': 150,
        'height': 100,
        'text-align': 'middle',
        'svg': """
            <rect class="task" width="150" height="100" rx="5" ry="5" style="stroke-width:5"/>
        """
    }

    bpmn_element = "subProcess"

    def __init__(self, subflow_task, subitem_source, **kwargs):
        self.subflow_task = subflow_task
        self.subitem_source = subitem_source
        super(NSubprocess, self).__init__(subflow_task, **kwargs)
