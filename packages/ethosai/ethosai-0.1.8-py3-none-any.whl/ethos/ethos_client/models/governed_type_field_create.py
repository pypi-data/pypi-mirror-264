from typing import (
    Any,
    Dict,
    List,
    Type,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.governed_type_field_create_datatype import GovernedTypeFieldCreateDatatype
from ..models.governed_type_field_create_type_type_0 import (
    GovernedTypeFieldCreateTypeType0,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="GovernedTypeFieldCreate")


@_attrs_define
class GovernedTypeFieldCreate:
    """
    Attributes:
        governed_type_id (str):
        name (str):
        datatype (GovernedTypeFieldCreateDatatype):
        description (Union[None, Unset, str]):
        type (Union[GovernedTypeFieldCreateTypeType0, None, Unset]):
    """

    governed_type_id: str
    name: str
    datatype: GovernedTypeFieldCreateDatatype
    description: Union[None, Unset, str] = UNSET
    type: Union[GovernedTypeFieldCreateTypeType0, None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        governed_type_id = self.governed_type_id

        name = self.name

        datatype = self.datatype.value

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        type: Union[None, Unset, str]
        if isinstance(self.type, Unset):
            type = UNSET
        elif isinstance(self.type, GovernedTypeFieldCreateTypeType0):
            type = self.type.value
        else:
            type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "governed_type_id": governed_type_id,
                "name": name,
                "datatype": datatype,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        governed_type_id = d.pop("governed_type_id")

        name = d.pop("name")

        datatype = GovernedTypeFieldCreateDatatype(d.pop("datatype"))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_type(
            data: object,
        ) -> Union[GovernedTypeFieldCreateTypeType0, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                type_type_0 = GovernedTypeFieldCreateTypeType0(data)

                return type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[GovernedTypeFieldCreateTypeType0, None, Unset], data)

        type = _parse_type(d.pop("type", UNSET))

        governed_type_field_create = cls(
            governed_type_id=governed_type_id,
            name=name,
            datatype=datatype,
            description=description,
            type=type,
        )

        governed_type_field_create.additional_properties = d
        return governed_type_field_create

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
