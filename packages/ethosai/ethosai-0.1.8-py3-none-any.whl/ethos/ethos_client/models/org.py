from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.list_namespace import ListNamespace
    from ..models.list_relationship import ListRelationship
    from ..models.list_user import ListUser


T = TypeVar("T", bound="Org")


@_attrs_define
class Org:
    """
    Attributes:
        object_ (str):
        id (str):
        created_at (str):
        updated_at (str):
        name (str):
        namespaces (Union['ListNamespace', 'ListRelationship']):
        users (Union['ListRelationship', 'ListUser']):
    """

    object_: str
    id: str
    created_at: str
    updated_at: str
    name: str
    namespaces: Union["ListNamespace", "ListRelationship"]
    users: Union["ListRelationship", "ListUser"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.list_namespace import ListNamespace
        from ..models.list_user import ListUser

        object_ = self.object_

        id = self.id

        created_at = self.created_at

        updated_at = self.updated_at

        name = self.name

        namespaces: Dict[str, Any]
        if isinstance(self.namespaces, ListNamespace):
            namespaces = self.namespaces.to_dict()
        else:
            namespaces = self.namespaces.to_dict()

        users: Dict[str, Any]
        if isinstance(self.users, ListUser):
            users = self.users.to_dict()
        else:
            users = self.users.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "name": name,
                "namespaces": namespaces,
                "users": users,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_namespace import ListNamespace
        from ..models.list_relationship import ListRelationship
        from ..models.list_user import ListUser

        d = src_dict.copy()
        object_ = d.pop("object")

        id = d.pop("id")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        name = d.pop("name")

        def _parse_namespaces(
            data: object,
        ) -> Union["ListNamespace", "ListRelationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                namespaces_type_0 = ListNamespace.from_dict(data)

                return namespaces_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            namespaces_type_1 = ListRelationship.from_dict(data)

            return namespaces_type_1

        namespaces = _parse_namespaces(d.pop("namespaces"))

        def _parse_users(data: object) -> Union["ListRelationship", "ListUser"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                users_type_0 = ListUser.from_dict(data)

                return users_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            users_type_1 = ListRelationship.from_dict(data)

            return users_type_1

        users = _parse_users(d.pop("users"))

        org = cls(
            object_=object_,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            name=name,
            namespaces=namespaces,
            users=users,
        )

        org.additional_properties = d
        return org

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
