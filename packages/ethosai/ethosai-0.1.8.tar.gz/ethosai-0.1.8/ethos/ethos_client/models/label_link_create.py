from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LabelLinkCreate")


@_attrs_define
class LabelLinkCreate:
    """
    Attributes:
        related_id (str):
        label_id (str):
    """

    related_id: str
    label_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        related_id = self.related_id

        label_id = self.label_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "related_id": related_id,
                "label_id": label_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        related_id = d.pop("related_id")

        label_id = d.pop("label_id")

        label_link_create = cls(
            related_id=related_id,
            label_id=label_id,
        )

        label_link_create.additional_properties = d
        return label_link_create

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
