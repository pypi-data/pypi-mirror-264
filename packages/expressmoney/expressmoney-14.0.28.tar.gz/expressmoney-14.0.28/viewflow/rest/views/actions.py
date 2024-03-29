import sys

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import views
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from .. import serializers
from .mixins import TaskResponseMixin


class BaseTaskActionView(TaskResponseMixin, views.APIView):
    _ignore_model_permissions = True
    serializer_class = None

    def get_serializer_class(self):
        if self.serializer_class is None:
            return serializers.EmptyInputSerializer
        return self.serializer_class

    def get_serializer_context(self):
        """
        Extra context provided to the action input serializer.
        """
        return {
            'request': self.request,
            'user': self.request.user,
            'view': self,
            'get_flowurl_namespace': lambda flow_class: self.request.resolver_match.namespace
        }

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for
        validation/deserialization input, and output serialization .
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_success_headers(self, data):
        return {}

    def can_proceed(self):
        raise NotImplementedError

    def perform(self, serializer):
        raise NotImplementedError

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            instance=self.activation.process)
        serializer.is_valid(raise_exception=True)
        self.perform(serializer)

        task_serializer = self.get_task_serializer(instance=self.activation.task)
        headers = self.get_success_headers(task_serializer.data)
        return Response(task_serializer.data, status=HTTP_201_CREATED, headers=headers)

    def initial(self, request, *args, **kwargs):
        super(BaseTaskActionView, self).initial(request, *args, **kwargs)

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

        if not self.can_proceed():
            raise PermissionDenied

    def finalize_response(self, request, response, *args, **kwargs):
        super(BaseTaskActionView, self).finalize_response(request, response, *args, **kwargs)
        self._lock.__exit__(*sys.exc_info())
        return response


class ActivateNextTaskView(BaseTaskActionView):
    def can_proceed(self):
        return self.activation.activate_next.can_proceed()

    def perform(self, serializer):
        self.activation.activate_next()


class AssignTaskView(BaseTaskActionView):
    """
    Assign task to the current user
    """
    def can_proceed(self):
        return self.activation.assign.can_proceed()

    def perform(self, serializer):
        self.activation.assign(self.request.user)


class CancelTaskView(BaseTaskActionView):
    def can_proceed(self):
        return self.activation.cancel.can_proceed()

    def perform(self, serializer):
        self.activation.cancel()


class PerformTaskView(BaseTaskActionView):
    def can_proceed(self):
        return self.activation.perform.can_proceed()

    def perform(self, serializer):
        self.activation.perform()


class UnassignTaskView(BaseTaskActionView):
    def can_proceed(self):
        return self.activation.unassign.can_proceed()

    def perform(self, serializer):
        self.activation.unassign()


class UndoTaskView(BaseTaskActionView):
    def can_proceed(self):
        return self.activation.undo.can_proceed()

    def perform(self, serializer):
        self.activation.undo()
