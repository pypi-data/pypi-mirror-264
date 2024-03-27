from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.governed_object import GovernedObject
    from ..models.label import Label
    from ..models.relationship import Relationship


T = TypeVar("T", bound="LabelLink")


@_attrs_define
class LabelLink:
    """
    Attributes:
        object_ (str):
        id (str):
        created_at (str):
        updated_at (str):
        related (Union['GovernedObject', 'Relationship']):
        label (Union['Label', 'Relationship']):
    """

    object_: str
    id: str
    created_at: str
    updated_at: str
    related: Union["GovernedObject", "Relationship"]
    label: Union["Label", "Relationship"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.governed_object import GovernedObject
        from ..models.label import Label

        object_ = self.object_

        id = self.id

        created_at = self.created_at

        updated_at = self.updated_at

        related: Dict[str, Any]
        if isinstance(self.related, GovernedObject):
            related = self.related.to_dict()
        else:
            related = self.related.to_dict()

        label: Dict[str, Any]
        if isinstance(self.label, Label):
            label = self.label.to_dict()
        else:
            label = self.label.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "related": related,
                "label": label,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.governed_object import GovernedObject
        from ..models.label import Label
        from ..models.relationship import Relationship

        d = src_dict.copy()
        object_ = d.pop("object")

        id = d.pop("id")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        def _parse_related(data: object) -> Union["GovernedObject", "Relationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                related_type_0 = GovernedObject.from_dict(data)

                return related_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            related_type_1 = Relationship.from_dict(data)

            return related_type_1

        related = _parse_related(d.pop("related"))

        def _parse_label(data: object) -> Union["Label", "Relationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                label_type_0 = Label.from_dict(data)

                return label_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            label_type_1 = Relationship.from_dict(data)

            return label_type_1

        label = _parse_label(d.pop("label"))

        label_link = cls(
            object_=object_,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            related=related,
            label=label,
        )

        label_link.additional_properties = d
        return label_link

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
