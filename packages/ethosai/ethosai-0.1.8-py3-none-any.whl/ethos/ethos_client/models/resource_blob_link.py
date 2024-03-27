from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Type,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.blob import Blob
    from ..models.relationship import Relationship
    from ..models.resource import Resource


T = TypeVar("T", bound="ResourceBlobLink")


@_attrs_define
class ResourceBlobLink:
    """
    Attributes:
        object_ (str):
        id (str):
        created_at (str):
        updated_at (str):
        resource (Union['Relationship', 'Resource']):
        blob (Union['Blob', 'Relationship']):
    """

    object_: str
    id: str
    created_at: str
    updated_at: str
    resource: Union["Relationship", "Resource"]
    blob: Union["Blob", "Relationship"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.blob import Blob
        from ..models.resource import Resource

        object_ = self.object_

        id = self.id

        created_at = self.created_at

        updated_at = self.updated_at

        resource: Dict[str, Any]
        if isinstance(self.resource, Resource):
            resource = self.resource.to_dict()
        else:
            resource = self.resource.to_dict()

        blob: Dict[str, Any]
        if isinstance(self.blob, Blob):
            blob = self.blob.to_dict()
        else:
            blob = self.blob.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "resource": resource,
                "blob": blob,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.blob import Blob
        from ..models.relationship import Relationship
        from ..models.resource import Resource

        d = src_dict.copy()
        object_ = d.pop("object")

        id = d.pop("id")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        def _parse_resource(data: object) -> Union["Relationship", "Resource"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                resource_type_0 = Resource.from_dict(data)

                return resource_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            resource_type_1 = Relationship.from_dict(data)

            return resource_type_1

        resource = _parse_resource(d.pop("resource"))

        def _parse_blob(data: object) -> Union["Blob", "Relationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                blob_type_0 = Blob.from_dict(data)

                return blob_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            blob_type_1 = Relationship.from_dict(data)

            return blob_type_1

        blob = _parse_blob(d.pop("blob"))

        resource_blob_link = cls(
            object_=object_,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            resource=resource,
            blob=blob,
        )

        resource_blob_link.additional_properties = d
        return resource_blob_link

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
