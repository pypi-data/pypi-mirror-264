from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WorkflowCreate")


@_attrs_define
class WorkflowCreate:
    """
    Attributes:
        project_id (str):
        name (str):
        workflow_template_id (str):
    """

    project_id: str
    name: str
    workflow_template_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        project_id = self.project_id

        name = self.name

        workflow_template_id = self.workflow_template_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "name": name,
                "workflow_template_id": workflow_template_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        project_id = d.pop("project_id")

        name = d.pop("name")

        workflow_template_id = d.pop("workflow_template_id")

        workflow_create = cls(
            project_id=project_id,
            name=name,
            workflow_template_id=workflow_template_id,
        )

        workflow_create.additional_properties = d
        return workflow_create

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
