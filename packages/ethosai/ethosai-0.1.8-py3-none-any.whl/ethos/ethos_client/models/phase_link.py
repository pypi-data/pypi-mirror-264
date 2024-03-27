from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.phase import Phase
    from ..models.relationship import Relationship


T = TypeVar("T", bound="PhaseLink")


@_attrs_define
class PhaseLink:
    """
    Attributes:
        object_ (str):
        id (str):
        created_at (str):
        updated_at (str):
        parent_phase (Union['Phase', 'Relationship']):
        child_phase (Union['Phase', 'Relationship']):
    """

    object_: str
    id: str
    created_at: str
    updated_at: str
    parent_phase: Union["Phase", "Relationship"]
    child_phase: Union["Phase", "Relationship"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.phase import Phase

        object_ = self.object_

        id = self.id

        created_at = self.created_at

        updated_at = self.updated_at

        parent_phase: Dict[str, Any]
        if isinstance(self.parent_phase, Phase):
            parent_phase = self.parent_phase.to_dict()
        else:
            parent_phase = self.parent_phase.to_dict()

        child_phase: Dict[str, Any]
        if isinstance(self.child_phase, Phase):
            child_phase = self.child_phase.to_dict()
        else:
            child_phase = self.child_phase.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "parent_phase": parent_phase,
                "child_phase": child_phase,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.phase import Phase
        from ..models.relationship import Relationship

        d = src_dict.copy()
        object_ = d.pop("object")

        id = d.pop("id")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        def _parse_parent_phase(data: object) -> Union["Phase", "Relationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                parent_phase_type_0 = Phase.from_dict(data)

                return parent_phase_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            parent_phase_type_1 = Relationship.from_dict(data)

            return parent_phase_type_1

        parent_phase = _parse_parent_phase(d.pop("parent_phase"))

        def _parse_child_phase(data: object) -> Union["Phase", "Relationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                child_phase_type_0 = Phase.from_dict(data)

                return child_phase_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            child_phase_type_1 = Relationship.from_dict(data)

            return child_phase_type_1

        child_phase = _parse_child_phase(d.pop("child_phase"))

        phase_link = cls(
            object_=object_,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            parent_phase=parent_phase,
            child_phase=child_phase,
        )

        phase_link.additional_properties = d
        return phase_link

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
