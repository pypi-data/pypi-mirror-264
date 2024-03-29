from rest_framework import permissions, views, generics
from rest_framework.response import Response

from ... import models
from .. import filters, serializers
from .mixins import FlowListMixin, FlowAPIMixin, FlowViewPermissionMixin


class FlowListView(FlowListMixin, views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        response = []
        for flow_class in self.flows:
            if self.request.user.has_perm(flow_class._meta.view_permission_name):
                serializer = serializers.FlowClassSerializer(
                    flow_class, context=self.get_serializer_context())
                response.append(serializer.data)

        return Response(response)


class AllProcessListView(FlowListMixin, generics.ListAPIView):
    serializer_class = serializers.ProcessSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = filters.ProcessFilter

    def get_queryset(self):
        return models.Process.objects.filter_available(self.flows, self.request.user)


class AllTaskListView(FlowListMixin, generics.ListAPIView):
    serializer_class = serializers.TaskListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = filters.TaskFilter

    def get_queryset(self):
        queryset = models.Task._default_manager.all()
        task_list = self.request.GET.get('task_list')
        if task_list == 'INBOX':
            queryset = queryset.inbox(self.flows, self.request.user)
        elif task_list == 'QUEUE':
            queryset = queryset.queue(self.flows, self.request.user)
        elif task_list == 'ARCHIVE':
            queryset = queryset.archive(self.flows, self.request.user)
        else:
            queryset = queryset.filter_available(self.flows, self.request.user)
        return queryset


class ProcessListView(FlowAPIMixin, FlowViewPermissionMixin, generics.ListAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = filters.ProcessFilter

    def get_serializer_class(self):
        if self.serializer_class is None:
            process_class = self.flow_class.process_class

            class ProcessSerializer(serializers.ProcessSerializer):
                class Meta(serializers.ProcessSerializer.Meta):
                    model = process_class

            return ProcessSerializer
        else:
            return self.serializer_class

    def get_flow_namespace(self, flow_class):
        return self.request.resolver_match.namespace

    def get_serializer_context(self):
        return {
            'request': self.request,
            'user': self.request.user,
            'get_flowurl_namespace': self.get_flow_namespace,
        }

    def get_queryset(self):
        flow_class = self.kwargs['flow_class']
        return flow_class.process_class.objects.filter(
            flow_class=flow_class
        )


class TaskListView(FlowAPIMixin, FlowViewPermissionMixin, generics.ListAPIView):
    serializer_class = serializers.TaskListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = filters.TaskFilter

    def get_flow_namespace(self, flow_class):
        return self.request.resolver_match.namespace

    def get_serializer_context(self):
        return {
            'request': self.request,
            'user': self.request.user,
            'get_flowurl_namespace': self.get_flow_namespace,
        }

    def get_queryset(self):
        flow_class = self.kwargs['flow_class']
        queryset = flow_class.task_class.objects.filter(
            process__flow_class=flow_class
        )
        task_list = self.request.GET.get('task_list')
        if task_list == 'INBOX':
            queryset = queryset.inbox([flow_class], self.request.user)
        elif task_list == 'QUEUE':
            queryset = queryset.queue([flow_class], self.request.user)
        elif task_list == 'ARCHIVE':
            queryset = queryset.archive([flow_class], self.request.user)
        elif task_list == 'ACTIVE':
            queryset = queryset.filter_available(
                [self.flow_class], self.request.user
            ).filter(
                finished__isnull=True
            )
        return queryset
