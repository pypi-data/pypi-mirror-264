from ..activation import Activation, StartActivation, ViewActivation, STATUS


class ManagedStartViewActivation(StartActivation):
    @Activation.status.super()
    def prepare(self, user=None):
        """Prepare activation for execution."""
        super(ManagedStartViewActivation, self).prepare.original()
        self.task.owner = user


class ManagedViewActivation(ViewActivation):
    @Activation.status.super()
    def prepare(self, user=None):
        """Prepare activation for execution."""
        super(ManagedViewActivation, self).prepare.original()

        if user:
            self.task.owner = user

    @classmethod
    def create_task(cls, flow_task, prev_activation, token):
        """Create a task, calculate owner and permissions."""
        task = ViewActivation.create_task(flow_task, prev_activation, token)

        activation = task.activate()

        # Try to assign permission
        owner_permission = flow_task.calc_owner_permission(activation)
        if owner_permission:
            task.owner_permission = owner_permission
            task.owner_permission_obj = flow_task.calc_owner_permission_obj(activation)

        # Try to assign owner
        owner = flow_task.calc_owner(activation)
        if owner:
            task.owner = owner
            task.status = STATUS.ASSIGNED

        return task
