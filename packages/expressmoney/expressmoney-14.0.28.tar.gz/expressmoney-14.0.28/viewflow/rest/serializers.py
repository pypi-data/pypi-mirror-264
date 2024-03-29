from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.urls import reverse

from .. import models
from ..fields import get_flow_ref, get_task_ref


class EmptyInputSerializer(serializers.Serializer):
    """
    Serializer that expects no input
    """


class FlowURLSerializerMixin(object):
    def __init__(self, *args, **kwargs):
        super(FlowURLSerializerMixin, self).__init__(*args, **kwargs)
        self.user = self.context.get('user')
        self.request = self.context.get('request')
        self.get_flowurl_namespace = self.context.get('get_flowurl_namespace')

    def get_flowurl(self, flow_class, url_name):
        namespace = self.get_flowurl_namespace(flow_class)
        return reverse('{}:{}'.format(namespace, url_name))

    def get_flowprocess_url(self, process, url_type=None):
        namespace = self.get_flowurl_namespace(process.flow_class)
        url = reverse('{}:{}'.format(namespace, url_type), kwargs={
            'process_pk': process.pk
        })
        return self.request.build_absolute_uri(url)

    def get_flowtask_url(self, task, url_type=None, kwargs=None):
        flow_class, flow_task = task.flow_task.flow_class, task.flow_task
        namespace = self.get_flowurl_namespace(flow_class)

        url = flow_task.get_task_url(
            task, url_type=url_type if url_type else 'guess',
            user=self.user, namespace=namespace)
        if url:
            return self.request.build_absolute_uri(url)


class FlowClassSerializer(FlowURLSerializerMixin, object):
    def __init__(self, instance, context=None):
        self.instance = instance
        self.context = context or {}
        self.user = self.context.get('user', None)
        super(FlowClassSerializer, self).__init__()

    def get_start_actions(self):
        actions = []
        for node in self.instance._meta.nodes():
            from .flow import Start
            if isinstance(node, Start):
                if(self.user is None or node.can_execute(self.user)):
                    actions.append({
                        "name": node.name,
                        "flow_task": get_task_ref(node),
                        "title": node.task_title or node.name.title(),
                        "description": node.task_description,
                        "url": self.get_flowurl(self.instance, node.name),
                    })
        actions.sort(key=lambda action: action["name"])

        return actions

    @property
    def data(self):
        return {
            "flow_class": get_flow_ref(self.instance),
            "title": self.instance.process_title,
            "description": self.instance.process_description,
            "start_actions": self.get_start_actions(),
            "url": self.get_flowurl(self.instance, 'flow'),
        }


class ProcessSerializer(FlowURLSerializerMixin, serializers.ModelSerializer):
    flow_class = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(ProcessSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed, existing = set(fields), set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_flow_class(self, process):
        return get_flow_ref(process.flow_class)

    def get_url(self, process):
        return self.get_flowprocess_url(process, 'detail')

    def get_title(self, process):
        return process.flow_class.process_title

    def get_description(self, process):
        return process.flow_class.process_description

    class Meta:
        model = models.Process
        read_only_fields = ['status', 'finished']
        fields = '__all__'


class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class TaskOwnerSerializer(serializers.ModelSerializer):
    short_name = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    def get_short_name(self, user):
        return user.get_short_name() if hasattr(user, 'get_short_name') else None

    def get_full_name(self, user):
        return user.get_full_name() if hasattr(user, 'get_full_name') else None

    class Meta:
        @classproperty
        def model(cls):
            return get_user_model()

        @classproperty
        def fields(cls):
            return tuple(cls.model.REQUIRED_FIELDS) + (
                cls.model._meta.pk.name,
                cls.model.USERNAME_FIELD,
                "short_name",
                "full_name")


class LinkedTaskSerializer(FlowURLSerializerMixin, serializers.ModelSerializer):
    flow_task = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    owner = TaskOwnerSerializer()

    def get_flow_task(self, task):
        return get_task_ref(task.flow_task)

    def get_url(self, task):
        return self.get_flowtask_url(
            task, "detail",
            kwargs={
                'process_pk': task.process_id,
                'task_pk': task.pk
            })

    def get_title(self, task):
        return task.flow_task.task_title or task.flow_task.name.title()

    def get_description(self, task):
        return task.flow_task.task_description

    class Meta:
        model = models.Task
        fields = ['id', 'flow_task', 'url', 'title', 'description', 'owner', 'status']


class TaskSerializer(FlowURLSerializerMixin, serializers.ModelSerializer):
    flow_task = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()
    process_summary = serializers.SerializerMethodField()
    actions = serializers.SerializerMethodField()
    owner = TaskOwnerSerializer()

    def get_flow_task(self, task):
        return get_task_ref(task.flow_task)

    def get_url(self, task):
        return self.get_flowtask_url(
            task, "detail",
            kwargs={
                'process_pk': task.process_id,
                'task_pk': task.pk
            })

    def get_title(self, task):
        return task.flow_task.task_title or task.flow_task.name.title()

    def get_description(self, task):
        return task.flow_task.task_description

    def get_summary(self, task):
        return task.summary()

    def get_process_summary(self, task):
        return task.flow_process.summary()

    def get_actions(self, task):
        response = []
        user = self.context.get('user', None)

        if user and user.has_perm(task.flow_task.flow_class._meta.manage_permission_name):
            activation = task.activate()
            for transition in activation.get_available_transitions():
                url = self.get_flowtask_url(
                        task, transition.name,
                        kwargs={
                            'process_pk': task.process_id,
                            'task_pk': task.pk
                        })
                if url:
                    response.append({
                        "name": transition.name,
                        "url": url
                    })

            if hasattr(activation, 'prepare') and activation.prepare.can_proceed():
                response.append({'name': "execute", "url": self.get_flowtask_url(
                    task, 'execute',
                    kwargs={
                        'process_pk': task.process_id,
                        'task_pk': task.pk
                    })})

        return response

    class Meta:
        model = models.Task
        fields = '__all__'


class TaskListSerializer(TaskSerializer):
    def __init__(self, *args, **kwargs):
        super(TaskListSerializer, self).__init__(*args, **kwargs)
        self.fields['process'] = ProcessSerializer(context=self.context)
        self.fields['previous'] = LinkedTaskSerializer(many=True, context=self.context)
        self.fields['leading'] = LinkedTaskSerializer(many=True, context=self.context)


class ProcessDetailSerializer(ProcessSerializer):
    def __init__(self, *args, **kwargs):
        super(ProcessDetailSerializer, self).__init__(*args, **kwargs)
        self.fields['tasks'] = TaskSerializer(source='task_set', many=True, context=self.context)


class SubprocessTaskSerializer(TaskListSerializer):
    subprocesses = serializers.SerializerMethodField()

    def get_subprocesses(self, task):
        activation = self.context.get('activation')
        if activation:
            return [
                ProcessSerializer(instance=subprocess, context=self.context).data
                for subprocess in activation.subprocesses()
            ]
