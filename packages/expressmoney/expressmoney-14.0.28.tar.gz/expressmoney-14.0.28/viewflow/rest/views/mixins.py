import sys

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator

from .. import serializers


class FlowAPIMixin(object):
    """
    Adds `initkwargs` to the view function.

    Flow view introspection fix.
    """
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(FlowAPIMixin, cls).as_view(**initkwargs)
        view.initkwargs = initkwargs
        return view


class FlowListMixin(FlowAPIMixin):
    """
    Mixin for list views that contains multiple flows
    """

    ns_map = None
    absolute_ns_map = False

    def __init__(self, *args, **kwargs):
        self.ns_map = kwargs.pop('ns_map', {})
        self.ns_map_reversed = {
            flow_class: namespace
            for namespace, flow_class in self.ns_map.items()
        }
        super(FlowListMixin, self).__init__(*args, **kwargs)

    def get_flow_namespace(self, flow_class):
        namespace = self.ns_map_reversed.get(flow_class)
        if self.absolute_ns_map:
            return namespace
        elif namespace:
            base_namespace = self.request.resolver_match.namespace
            if base_namespace:
                namespace = "{}:{}".format(base_namespace, namespace)
        return namespace

    def get_serializer_context(self):
        return {
            'request': self.request,
            'user': self.request.user,
            'get_flowurl_namespace': self.get_flow_namespace,
        }

    @property
    def flows(self):
        return self.ns_map.values()


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class FlowViewPermissionMixin(object):
    """
    Mixin for flow views, check the view permission.
    """
    def initial(self, request, *args, **kwargs):
        self.flow_class = kwargs['flow_class']
        if not request.user.has_perm(self.flow_class._meta.view_permission_name):
            raise PermissionDenied


class TaskActivationMixin(FlowAPIMixin):
    _ignore_model_permissions = True
    _lock = None

    def initial(self, request, *args, **kwargs):
        super(TaskActivationMixin, self).initial(request, *args, **kwargs)

        process_pk, task_pk = kwargs['process_pk'], kwargs['task_pk']
        flow_class, flow_task = kwargs['flow_class'], kwargs['flow_task']

        lock_impl = flow_task.flow_class.lock_impl(flow_class.instance)
        self._lock = lock_impl(flow_class, process_pk)
        self._lock.__enter__()

        task = get_object_or_404(
            flow_task.flow_class.task_class._default_manager, pk=task_pk,
            process_id=process_pk, flow_task=flow_task)
        self.activation = flow_task.activation_class()
        self.activation.initialize(flow_task, task)

        request.activation = self.activation
        request.process = self.activation.process
        request.task = self.activation.task

        if not self.activation.prepare.can_proceed():
            raise PermissionDenied

        if not self.activation.has_perm(request.user):
            raise PermissionDenied

        self.activation.prepare(user=request.user)

    def handle_exception(self, exc):
        if self._lock is not None:
            self._lock.__exit__(*sys.exc_info())
            self._lock = None

        return super(TaskActivationMixin, self).handle_exception(exc)

    def finalize_response(self, request, response, *args, **kwargs):
        super(TaskActivationMixin, self).finalize_response(request, response, *args, **kwargs)
        if self._lock is not None:
            self._lock.__exit__(*sys.exc_info())
        return response


class TaskResponseMixin(FlowAPIMixin):
    """
    Mixin for Flow Views with task instance in response
    """
    task_serializer_class = None

    def get_task_serializer_class(self):
        if self.task_serializer_class is None:
            task_class = self.kwargs['flow_class'].task_class

            class TaskListSerializer(serializers.TaskListSerializer):
                class Meta(serializers.TaskSerializer.Meta):
                    model = task_class

            return TaskListSerializer
        else:
            return self.task_serializer_class

    def get_task_serializer(self, *args, **kwargs):
        task_serializer_class = self.get_task_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return task_serializer_class(*args, **kwargs)


class ProcessViewMixin(FlowAPIMixin):
    fields = None
    serializer_class = None

    def get_serializer_class(self):
        if self.serializer_class is None:
            process_class = self.kwargs['flow_class'].process_class

            class ProcessSerializer(serializers.ProcessSerializer):
                class Meta(serializers.ProcessSerializer.Meta):
                    model = process_class

            return ProcessSerializer
        else:
            return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        if self.fields is not None:
            kwargs['fields'] = self.fields
        return super(ProcessViewMixin, self).get_serializer(*args, **kwargs)


class StartActivationMixin(FlowAPIMixin):
    """
    Mixin for flow start views. Instantiate `self.activation` instance
    """
    _ignore_model_permissions = True
    activation = None

    def initial(self, request, *args, **kwargs):
        super(StartActivationMixin, self).initial(request, *args, **kwargs)

        flow_task = kwargs['flow_task']
        self.activation = flow_task.activation_class()
        self.activation.initialize(flow_task, None)

        request.activation = self.activation
        request.process = self.activation.process
        request.task = self.activation.task

        if not self.activation.prepare.can_proceed():
            raise PermissionDenied

        if not self.activation.has_perm(request.user):
            raise PermissionDenied

        self.activation.prepare(user=request.user)

    def handle_exception(self, exc):
        if self.activation and self.activation.lock:
            self.activation.lock.__exit__(*sys.exc_info())
            self.activation.lock = None

        return super(StartActivationMixin, self).handle_exception(exc)

    def finalize_response(self, request, response, *args, **kwargs):
        super(StartActivationMixin, self).finalize_response(request, response, *args, **kwargs)
        if self.activation and self.activation.lock:
            self.activation.lock.__exit__(*sys.exc_info())
        return response
