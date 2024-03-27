from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.governed_type_create_object_classification import (
    GovernedTypeCreateObjectClassification,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="GovernedTypeCreate")


@_attrs_define
class GovernedTypeCreate:
    """
    Attributes:
        namespace_id (str):
        name (str):
        description (Union[None, Unset, str]):
        object_classification (Union[Unset, GovernedTypeCreateObjectClassification]):  Default:
            GovernedTypeCreateObjectClassification.CUSTOM.
    """

    namespace_id: str
    name: str
    description: Union[None, Unset, str] = UNSET
    object_classification: Union[Unset, GovernedTypeCreateObjectClassification] = (
        GovernedTypeCreateObjectClassification.CUSTOM
    )
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        namespace_id = self.namespace_id

        name = self.name

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        object_classification: Union[Unset, str] = UNSET
        if not isinstance(self.object_classification, Unset):
            object_classification = self.object_classification.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "namespace_id": namespace_id,
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if object_classification is not UNSET:
            field_dict["object_classification"] = object_classification

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        namespace_id = d.pop("namespace_id")

        name = d.pop("name")

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        _object_classification = d.pop("object_classification", UNSET)
        object_classification: Union[Unset, GovernedTypeCreateObjectClassification]
        if isinstance(_object_classification, Unset):
            object_classification = UNSET
        else:
            object_classification = GovernedTypeCreateObjectClassification(
                _object_classification
            )

        governed_type_create = cls(
            namespace_id=namespace_id,
            name=name,
            description=description,
            object_classification=object_classification,
        )

        governed_type_create.additional_properties = d
        return governed_type_create

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
