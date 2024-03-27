from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WorkflowTemplateCreate")


@_attrs_define
class WorkflowTemplateCreate:
    """
    Attributes:
        namespace_id (str):
        name (str):
        yaml (str):
    """

    namespace_id: str
    name: str
    yaml: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        namespace_id = self.namespace_id

        name = self.name

        yaml = self.yaml

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "namespace_id": namespace_id,
                "name": name,
                "yaml": yaml,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        namespace_id = d.pop("namespace_id")

        name = d.pop("name")

        yaml = d.pop("yaml")

        workflow_template_create = cls(
            namespace_id=namespace_id,
            name=name,
            yaml=yaml,
        )

        workflow_template_create.additional_properties = d
        return workflow_template_create

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
