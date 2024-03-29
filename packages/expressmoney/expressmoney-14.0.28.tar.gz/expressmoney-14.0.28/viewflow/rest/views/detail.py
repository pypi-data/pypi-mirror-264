from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import views, generics
from rest_framework.response import Response

from .. import serializers
from .mixins import FlowAPIMixin, TaskActivationMixin, FlowViewPermissionMixin


class DetailFlowView(FlowAPIMixin, FlowViewPermissionMixin, views.APIView):
    _ignore_model_permissions = True

    def get(self, request, *args, **kwargs):
        response = serializers.FlowClassSerializer(
            self.kwargs['flow_class'], context={
                'request': self.request,
                'user': self.request.user,
                'get_flowurl_namespace': lambda flow_class: self.request.resolver_match.namespace
            }
        ).data
        return Response(response)


class DetailTaskView(generics.RetrieveAPIView):
    _ignore_model_permissions = True

    serializer_class = serializers.TaskListSerializer
    pagination_class = None
    lookup_url_kwarg = 'task_pk'

    def get_serializer_context(self):
        return {
            'request': self.request,
            'user': self.request.user,
            'activation': self.activation,
            'get_flowurl_namespace': lambda flow_class: self.request.resolver_match.namespace
        }

    def get_queryset(self):
        return self.activation.flow_class.task_class._default_manager.filter_available(
            [self.activation.flow_class], self.request.user)

    def get_object(self):
        return self.activation.task

    def initial(self, request, *args, **kwargs):
        super(DetailTaskView, self).initial(request, *args, **kwargs)

        process_pk, task_pk = kwargs['process_pk'], kwargs['task_pk']
        flow_class, flow_task = kwargs['flow_class'], kwargs['flow_task']

        task = get_object_or_404(
            flow_class.task_class._default_manager, pk=task_pk,
            process_id=process_pk, flow_task=flow_task)
        self.activation = flow_task.activation_class()
        self.activation.initialize(flow_task, task)

        request.activation = self.activation
        request.process = self.activation.process
        request.task = self.activation.task

        if not self.activation.flow_task.can_view(request.user, self.activation.task):
            raise PermissionDenied


class DetailSubprocessView(DetailTaskView):
    serializer_class = serializers.SubprocessTaskSerializer


class DetailProcessView(FlowViewPermissionMixin, generics.RetrieveAPIView):
    fields = None
    pagination_class = None
    lookup_url_kwarg = 'process_pk'

    def get_serializer_class(self):
        if self.serializer_class is None:
            process_class = self.flow_class.process_class

            class ProcessSerializer(serializers.ProcessSerializer):
                class Meta(serializers.ProcessSerializer.Meta):
                    model = process_class

            return ProcessSerializer
        else:
            return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        if self.fields:
            kwargs['fields'] = self.fields
        return super(DetailProcessView, self).get_serializer(*args, **kwargs)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'user': self.request.user,
            'get_flowurl_namespace': lambda flow_class: self.request.resolver_match.namespace
        }

    def get_queryset(self):
        flow_class = self.kwargs['flow_class']
        return flow_class.process_class._default_manager.filter_available(
            [flow_class], self.request.user)
