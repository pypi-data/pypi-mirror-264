from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.namespace import Namespace
    from ..models.relationship import Relationship


T = TypeVar("T", bound="Folder")


@_attrs_define
class Folder:
    """
    Attributes:
        object_ (str):
        id (str):
        created_at (str):
        updated_at (str):
        namespace (Union['Namespace', 'Relationship']):
        parent_folder (Union['Folder', 'Relationship', None]):
        name (str):
        is_default (bool):
    """

    object_: str
    id: str
    created_at: str
    updated_at: str
    namespace: Union["Namespace", "Relationship"]
    parent_folder: Union["Folder", "Relationship", None]
    name: str
    is_default: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.namespace import Namespace
        from ..models.relationship import Relationship

        object_ = self.object_

        id = self.id

        created_at = self.created_at

        updated_at = self.updated_at

        namespace: Dict[str, Any]
        if isinstance(self.namespace, Namespace):
            namespace = self.namespace.to_dict()
        else:
            namespace = self.namespace.to_dict()

        parent_folder: Union[Dict[str, Any], None]
        if isinstance(self.parent_folder, Folder):
            parent_folder = self.parent_folder.to_dict()
        elif isinstance(self.parent_folder, Relationship):
            parent_folder = self.parent_folder.to_dict()
        else:
            parent_folder = self.parent_folder

        name = self.name

        is_default = self.is_default

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "namespace": namespace,
                "parent_folder": parent_folder,
                "name": name,
                "is_default": is_default,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.namespace import Namespace
        from ..models.relationship import Relationship

        d = src_dict.copy()
        object_ = d.pop("object")

        id = d.pop("id")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        def _parse_namespace(data: object) -> Union["Namespace", "Relationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                namespace_type_0 = Namespace.from_dict(data)

                return namespace_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            namespace_type_1 = Relationship.from_dict(data)

            return namespace_type_1

        namespace = _parse_namespace(d.pop("namespace"))

        def _parse_parent_folder(data: object) -> Union["Folder", "Relationship", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                parent_folder_type_0 = Folder.from_dict(data)

                return parent_folder_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                parent_folder_type_1 = Relationship.from_dict(data)

                return parent_folder_type_1
            except:  # noqa: E722
                pass
            return cast(Union["Folder", "Relationship", None], data)

        parent_folder = _parse_parent_folder(d.pop("parent_folder"))

        name = d.pop("name")

        is_default = d.pop("is_default")

        folder = cls(
            object_=object_,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            namespace=namespace,
            parent_folder=parent_folder,
            name=name,
            is_default=is_default,
        )

        folder.additional_properties = d
        return folder

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
