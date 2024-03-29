from rest_framework import mixins, generics
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from .mixins import StartActivationMixin, TaskResponseMixin, ProcessViewMixin


class BaseStartFlowView(StartActivationMixin,
                        mixins.CreateModelMixin,
                        generics.GenericAPIView):
    """
    Base class for generic start views
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

    def perform_create(self, serializer):
        serializer.save()
        self.activation.done()


class CreateProcessView(TaskResponseMixin,
                        ProcessViewMixin,
                        BaseStartFlowView):
    _ignore_model_permissions = True

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            instance=self.activation.process)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        task_serializer = self.get_task_serializer(instance=self.activation.task)
        headers = self.get_success_headers(task_serializer.data)
        return Response(task_serializer.data, status=HTTP_201_CREATED, headers=headers)
