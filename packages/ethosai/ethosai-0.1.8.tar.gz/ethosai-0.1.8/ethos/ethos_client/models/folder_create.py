from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FolderCreate")


@_attrs_define
class FolderCreate:
    """
    Attributes:
        namespace_id (str):
        name (str):
        parent_folder_id (Union[None, str]):
        is_default (Union[Unset, bool]):  Default: False.
    """

    namespace_id: str
    name: str
    parent_folder_id: Union[None, str]
    is_default: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        namespace_id = self.namespace_id

        name = self.name

        parent_folder_id: Union[None, str]
        parent_folder_id = self.parent_folder_id

        is_default = self.is_default

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "namespace_id": namespace_id,
                "name": name,
                "parent_folder_id": parent_folder_id,
            }
        )
        if is_default is not UNSET:
            field_dict["is_default"] = is_default

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        namespace_id = d.pop("namespace_id")

        name = d.pop("name")

        def _parse_parent_folder_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        parent_folder_id = _parse_parent_folder_id(d.pop("parent_folder_id"))

        is_default = d.pop("is_default", UNSET)

        folder_create = cls(
            namespace_id=namespace_id,
            name=name,
            parent_folder_id=parent_folder_id,
            is_default=is_default,
        )

        folder_create.additional_properties = d
        return folder_create

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
