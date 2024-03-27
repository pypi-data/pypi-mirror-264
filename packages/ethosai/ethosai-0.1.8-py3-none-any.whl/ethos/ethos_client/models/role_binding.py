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

from ..models.role_binding_role_name import RoleBindingRoleName

if TYPE_CHECKING:
    from ..models.folder import Folder
    from ..models.namespace import Namespace
    from ..models.org import Org
    from ..models.relationship import Relationship
    from ..models.user import User


T = TypeVar("T", bound="RoleBinding")


@_attrs_define
class RoleBinding:
    """
    Attributes:
        object_ (str):
        id (str):
        created_at (str):
        updated_at (str):
        role_name (RoleBindingRoleName):
        user (Union['Relationship', 'User']):
        related (Union['Folder', 'Namespace', 'Org', 'Relationship']):
    """

    object_: str
    id: str
    created_at: str
    updated_at: str
    role_name: RoleBindingRoleName
    user: Union["Relationship", "User"]
    related: Union["Folder", "Namespace", "Org", "Relationship"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.folder import Folder
        from ..models.namespace import Namespace
        from ..models.org import Org
        from ..models.user import User

        object_ = self.object_

        id = self.id

        created_at = self.created_at

        updated_at = self.updated_at

        role_name = self.role_name.value

        user: Dict[str, Any]
        if isinstance(self.user, User):
            user = self.user.to_dict()
        else:
            user = self.user.to_dict()

        related: Dict[str, Any]
        if isinstance(self.related, Org):
            related = self.related.to_dict()
        elif isinstance(self.related, Namespace):
            related = self.related.to_dict()
        elif isinstance(self.related, Folder):
            related = self.related.to_dict()
        else:
            related = self.related.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "role_name": role_name,
                "user": user,
                "related": related,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.folder import Folder
        from ..models.namespace import Namespace
        from ..models.org import Org
        from ..models.relationship import Relationship
        from ..models.user import User

        d = src_dict.copy()
        object_ = d.pop("object")

        id = d.pop("id")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        role_name = RoleBindingRoleName(d.pop("role_name"))

        def _parse_user(data: object) -> Union["Relationship", "User"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                user_type_0 = User.from_dict(data)

                return user_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            user_type_1 = Relationship.from_dict(data)

            return user_type_1

        user = _parse_user(d.pop("user"))

        def _parse_related(
            data: object,
        ) -> Union["Folder", "Namespace", "Org", "Relationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                related_type_0 = Org.from_dict(data)

                return related_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                related_type_1 = Namespace.from_dict(data)

                return related_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                related_type_2 = Folder.from_dict(data)

                return related_type_2
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            related_type_3 = Relationship.from_dict(data)

            return related_type_3

        related = _parse_related(d.pop("related"))

        role_binding = cls(
            object_=object_,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            role_name=role_name,
            user=user,
            related=related,
        )

        role_binding.additional_properties = d
        return role_binding

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
