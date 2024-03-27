from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.workflow_template_data_phases import WorkflowTemplateDataPhases


T = TypeVar("T", bound="WorkflowTemplateData")


@_attrs_define
class WorkflowTemplateData:
    """
    Attributes:
        ethos_version (int):
        name (str):
        phases (WorkflowTemplateDataPhases):
    """

    ethos_version: int
    name: str
    phases: "WorkflowTemplateDataPhases"

    def to_dict(self) -> Dict[str, Any]:
        ethos_version = self.ethos_version

        name = self.name

        phases = self.phases.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "ethos_version": ethos_version,
                "name": name,
                "phases": phases,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.workflow_template_data_phases import WorkflowTemplateDataPhases

        d = src_dict.copy()
        ethos_version = d.pop("ethos_version")

        name = d.pop("name")

        phases = WorkflowTemplateDataPhases.from_dict(d.pop("phases"))

        workflow_template_data = cls(
            ethos_version=ethos_version,
            name=name,
            phases=phases,
        )

        return workflow_template_data
