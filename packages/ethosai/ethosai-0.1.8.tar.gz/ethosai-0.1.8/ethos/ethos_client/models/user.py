from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_relationship import ListRelationship
    from ..models.org import Org


T = TypeVar("T", bound="User")


@_attrs_define
class User:
    """
    Attributes:
        object_ (str):
        id (str):
        created_at (str):
        updated_at (str):
        email (str):
        name (Union[None, str]):
        orgs (Union['ListRelationship', List['Org']]):
        is_active (Union[Unset, bool]):  Default: True.
        is_superuser (Union[Unset, bool]):  Default: False.
        is_verified (Union[Unset, bool]):  Default: False.
    """

    object_: str
    id: str
    created_at: str
    updated_at: str
    email: str
    name: Union[None, str]
    orgs: Union["ListRelationship", List["Org"]]
    is_active: Union[Unset, bool] = True
    is_superuser: Union[Unset, bool] = False
    is_verified: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_

        id = self.id

        created_at = self.created_at

        updated_at = self.updated_at

        email = self.email

        name: Union[None, str]
        name = self.name

        orgs: Union[Dict[str, Any], List[Dict[str, Any]]]
        if isinstance(self.orgs, list):
            orgs = []
            for orgs_type_0_item_data in self.orgs:
                orgs_type_0_item = orgs_type_0_item_data.to_dict()
                orgs.append(orgs_type_0_item)

        else:
            orgs = self.orgs.to_dict()

        is_active = self.is_active

        is_superuser = self.is_superuser

        is_verified = self.is_verified

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "email": email,
                "name": name,
                "orgs": orgs,
            }
        )
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if is_superuser is not UNSET:
            field_dict["is_superuser"] = is_superuser
        if is_verified is not UNSET:
            field_dict["is_verified"] = is_verified

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_relationship import ListRelationship
        from ..models.org import Org

        d = src_dict.copy()
        object_ = d.pop("object")

        id = d.pop("id")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        email = d.pop("email")

        def _parse_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        name = _parse_name(d.pop("name"))

        def _parse_orgs(data: object) -> Union["ListRelationship", List["Org"]]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                orgs_type_0 = []
                _orgs_type_0 = data
                for orgs_type_0_item_data in _orgs_type_0:
                    orgs_type_0_item = Org.from_dict(orgs_type_0_item_data)

                    orgs_type_0.append(orgs_type_0_item)

                return orgs_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            orgs_type_1 = ListRelationship.from_dict(data)

            return orgs_type_1

        orgs = _parse_orgs(d.pop("orgs"))

        is_active = d.pop("is_active", UNSET)

        is_superuser = d.pop("is_superuser", UNSET)

        is_verified = d.pop("is_verified", UNSET)

        user = cls(
            object_=object_,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            email=email,
            name=name,
            orgs=orgs,
            is_active=is_active,
            is_superuser=is_superuser,
            is_verified=is_verified,
        )

        user.additional_properties = d
        return user

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
