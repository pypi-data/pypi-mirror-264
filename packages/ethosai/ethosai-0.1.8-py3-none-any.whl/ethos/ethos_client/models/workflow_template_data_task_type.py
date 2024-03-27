from enum import Enum


class WorkflowTemplateDataTaskType(str, Enum):
    ATTESTATION_TASK = "attestation_task"
    DEMO_TASK = "demo_task"
    DOCUMENT_TASK = "document_task"
    ECHO_TASK = "echo_task"
    FORM_TASK = "form_task"
    MANUAL_TASK = "manual_task"
    UPDATE_INVENTORY_TASK = "update_inventory_task"

    def __str__(self) -> str:
        return str(self.value)
