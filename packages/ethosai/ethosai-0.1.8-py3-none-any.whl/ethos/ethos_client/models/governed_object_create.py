from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.governed_object_data import GovernedObjectData


T = TypeVar("T", bound="GovernedObjectCreate")


@_attrs_define
class GovernedObjectCreate:
    """
    Attributes:
        namespace_id (str):
        governed_type_id (str):
        data (GovernedObjectData):
        folder_id (Union[None, Unset, str]):
    """

    namespace_id: str
    governed_type_id: str
    data: "GovernedObjectData"
    folder_id: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        namespace_id = self.namespace_id

        governed_type_id = self.governed_type_id

        data = self.data.to_dict()

        folder_id: Union[None, Unset, str]
        if isinstance(self.folder_id, Unset):
            folder_id = UNSET
        else:
            folder_id = self.folder_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "namespace_id": namespace_id,
                "governed_type_id": governed_type_id,
                "data": data,
            }
        )
        if folder_id is not UNSET:
            field_dict["folder_id"] = folder_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.governed_object_data import GovernedObjectData

        d = src_dict.copy()
        namespace_id = d.pop("namespace_id")

        governed_type_id = d.pop("governed_type_id")

        data = GovernedObjectData.from_dict(d.pop("data"))

        def _parse_folder_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        folder_id = _parse_folder_id(d.pop("folder_id", UNSET))

        governed_object_create = cls(
            namespace_id=namespace_id,
            governed_type_id=governed_type_id,
            data=data,
            folder_id=folder_id,
        )

        governed_object_create.additional_properties = d
        return governed_object_create

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
