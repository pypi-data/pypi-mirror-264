from rest_framework import mixins, generics
from rest_framework.response import Response

from .mixins import TaskActivationMixin, TaskResponseMixin, ProcessViewMixin


class BaseFlowView(TaskActivationMixin,
                   mixins.UpdateModelMixin,
                   generics.GenericAPIView):
    """
    Base class for generic flow views
    """
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

    def perform_update(self, serializer):
        serializer.save()
        self.activation.done()


class UpdateProcessView(TaskResponseMixin,
                        ProcessViewMixin,
                        BaseFlowView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            instance=self.activation.process)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        task_serializer = self.get_task_serializer(instance=self.activation.task)
        return Response(task_serializer.data)
