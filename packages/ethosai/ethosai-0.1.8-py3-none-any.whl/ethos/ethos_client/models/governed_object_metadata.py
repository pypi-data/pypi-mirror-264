from typing import (
    TYPE_CHECKING,
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

from ..models.governed_object_metadata_type import GovernedObjectMetadataType

if TYPE_CHECKING:
    from ..models.governed_object import GovernedObject
    from ..models.governed_object_metadata_data import GovernedObjectMetadataData
    from ..models.relationship import Relationship
    from ..models.user import User


T = TypeVar("T", bound="GovernedObjectMetadata")


@_attrs_define
class GovernedObjectMetadata:
    """
    Attributes:
        object_ (str):
        id (str):
        base_id (str): The base ID of this object without the version tag suffix.
        version_number (int):
        version_tags (List[str]):
        version_tag (str): The primary version tag for this version, such as v0, v1, etc.
        version_updated_fields (List[str]): A list of which fields were updated in this version from the previous
            version.
        version_updated_by (Union['Relationship', 'User', None]): The user who updated the versioned object to this
            version.
        type (GovernedObjectMetadataType):
        governed_object (Union['GovernedObject', 'Relationship', None]):
        data (GovernedObjectMetadataData):
    """

    object_: str
    id: str
    base_id: str
    version_number: int
    version_tags: List[str]
    version_tag: str
    version_updated_fields: List[str]
    version_updated_by: Union["Relationship", "User", None]
    type: GovernedObjectMetadataType
    governed_object: Union["GovernedObject", "Relationship", None]
    data: "GovernedObjectMetadataData"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.governed_object import GovernedObject
        from ..models.relationship import Relationship
        from ..models.user import User

        object_ = self.object_

        id = self.id

        base_id = self.base_id

        version_number = self.version_number

        version_tags = self.version_tags

        version_tag = self.version_tag

        version_updated_fields = self.version_updated_fields

        version_updated_by: Union[Dict[str, Any], None]
        if isinstance(self.version_updated_by, User):
            version_updated_by = self.version_updated_by.to_dict()
        elif isinstance(self.version_updated_by, Relationship):
            version_updated_by = self.version_updated_by.to_dict()
        else:
            version_updated_by = self.version_updated_by

        type = self.type.value

        governed_object: Union[Dict[str, Any], None]
        if isinstance(self.governed_object, GovernedObject):
            governed_object = self.governed_object.to_dict()
        elif isinstance(self.governed_object, Relationship):
            governed_object = self.governed_object.to_dict()
        else:
            governed_object = self.governed_object

        data = self.data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "id": id,
                "base_id": base_id,
                "version_number": version_number,
                "version_tags": version_tags,
                "version_tag": version_tag,
                "version_updated_fields": version_updated_fields,
                "version_updated_by": version_updated_by,
                "type": type,
                "governed_object": governed_object,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.governed_object import GovernedObject
        from ..models.governed_object_metadata_data import GovernedObjectMetadataData
        from ..models.relationship import Relationship
        from ..models.user import User

        d = src_dict.copy()
        object_ = d.pop("object")

        id = d.pop("id")

        base_id = d.pop("base_id")

        version_number = d.pop("version_number")

        version_tags = cast(List[str], d.pop("version_tags"))

        version_tag = d.pop("version_tag")

        version_updated_fields = cast(List[str], d.pop("version_updated_fields"))

        def _parse_version_updated_by(
            data: object,
        ) -> Union["Relationship", "User", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                version_updated_by_type_0 = User.from_dict(data)

                return version_updated_by_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                version_updated_by_type_1 = Relationship.from_dict(data)

                return version_updated_by_type_1
            except:  # noqa: E722
                pass
            return cast(Union["Relationship", "User", None], data)

        version_updated_by = _parse_version_updated_by(d.pop("version_updated_by"))

        type = GovernedObjectMetadataType(d.pop("type"))

        def _parse_governed_object(
            data: object,
        ) -> Union["GovernedObject", "Relationship", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                governed_object_type_0 = GovernedObject.from_dict(data)

                return governed_object_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                governed_object_type_1 = Relationship.from_dict(data)

                return governed_object_type_1
            except:  # noqa: E722
                pass
            return cast(Union["GovernedObject", "Relationship", None], data)

        governed_object = _parse_governed_object(d.pop("governed_object"))

        data = GovernedObjectMetadataData.from_dict(d.pop("data"))

        governed_object_metadata = cls(
            object_=object_,
            id=id,
            base_id=base_id,
            version_number=version_number,
            version_tags=version_tags,
            version_tag=version_tag,
            version_updated_fields=version_updated_fields,
            version_updated_by=version_updated_by,
            type=type,
            governed_object=governed_object,
            data=data,
        )

        governed_object_metadata.additional_properties = d
        return governed_object_metadata

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
