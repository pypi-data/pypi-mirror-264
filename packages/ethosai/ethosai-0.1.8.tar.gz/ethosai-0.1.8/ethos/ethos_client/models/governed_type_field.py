from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.governed_type_field_datatype import GovernedTypeFieldDatatype
from ..models.governed_type_field_type import GovernedTypeFieldType

if TYPE_CHECKING:
    from ..models.governed_type import GovernedType
    from ..models.relationship import Relationship


T = TypeVar("T", bound="GovernedTypeField")


@_attrs_define
class GovernedTypeField:
    """
    Attributes:
        object_ (str):
        id (str):
        created_at (str):
        updated_at (str):
        governed_type (Union['GovernedType', 'Relationship']):
        type (GovernedTypeFieldType):
        name (str):
        description (Union[None, str]):
        datatype (GovernedTypeFieldDatatype):
        index (int):
    """

    object_: str
    id: str
    created_at: str
    updated_at: str
    governed_type: Union["GovernedType", "Relationship"]
    type: GovernedTypeFieldType
    name: str
    description: Union[None, str]
    datatype: GovernedTypeFieldDatatype
    index: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.governed_type import GovernedType

        object_ = self.object_

        id = self.id

        created_at = self.created_at

        updated_at = self.updated_at

        governed_type: Dict[str, Any]
        if isinstance(self.governed_type, GovernedType):
            governed_type = self.governed_type.to_dict()
        else:
            governed_type = self.governed_type.to_dict()

        type = self.type.value

        name = self.name

        description: Union[None, str]
        description = self.description

        datatype = self.datatype.value

        index = self.index

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "governed_type": governed_type,
                "type": type,
                "name": name,
                "description": description,
                "datatype": datatype,
                "index": index,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.governed_type import GovernedType
        from ..models.relationship import Relationship

        d = src_dict.copy()
        object_ = d.pop("object")

        id = d.pop("id")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        def _parse_governed_type(data: object) -> Union["GovernedType", "Relationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                governed_type_type_0 = GovernedType.from_dict(data)

                return governed_type_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            governed_type_type_1 = Relationship.from_dict(data)

            return governed_type_type_1

        governed_type = _parse_governed_type(d.pop("governed_type"))

        type = GovernedTypeFieldType(d.pop("type"))

        name = d.pop("name")

        def _parse_description(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        description = _parse_description(d.pop("description"))

        datatype = GovernedTypeFieldDatatype(d.pop("datatype"))

        index = d.pop("index")

        governed_type_field = cls(
            object_=object_,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            governed_type=governed_type,
            type=type,
            name=name,
            description=description,
            datatype=datatype,
            index=index,
        )

        governed_type_field.additional_properties = d
        return governed_type_field

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
