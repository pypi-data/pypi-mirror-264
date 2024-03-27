from enum import Enum


class EventAction(str, Enum):
    GOVERNED_OBJECT_CREATED = "governed_object_created"
    GOVERNED_OBJECT_UPDATED = "governed_object_updated"
    LABEL_LINK_CREATED = "label_link_created"
    LABEL_LINK_DELETED = "label_link_deleted"
    PHASE_COMPLETED = "phase_completed"
    PHASE_FAILED = "phase_failed"
    PHASE_INITIALIZED = "phase_initialized"
    PHASE_OWNER_UPDATED = "phase_owner_updated"
    PHASE_READY = "phase_ready"
    PHASE_SKIPPED = "phase_skipped"
    PHASE_STARTED = "phase_started"
    PHASE_WAITING_ON_DEPENDENCIES = "phase_waiting_on_dependencies"
    ROLE_BINDING_CREATED = "role_binding_created"
    ROLE_BINDING_DELETED = "role_binding_deleted"
    ROLE_BINDING_UPDATED = "role_binding_updated"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    TASK_INITIALIZED = "task_initialized"
    TASK_OWNER_UPDATED = "task_owner_updated"
    TASK_READY = "task_ready"
    TASK_SKIPPED = "task_skipped"
    TASK_STARTED = "task_started"
    TASK_WAITING_ON_DEPENDENCIES = "task_waiting_on_dependencies"
    WORKFLOW_COMPLETED = "workflow_completed"
    WORKFLOW_CREATED = "workflow_created"
    WORKFLOW_FAILED = "workflow_failed"
    WORKFLOW_STARTED = "workflow_started"

    def __str__(self) -> str:
        return str(self.value)
