from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.event_action import EventAction
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.document import Document
    from ..models.event_from_data import EventFromData
    from ..models.event_to_data import EventToData
    from ..models.governed_object import GovernedObject
    from ..models.label import Label
    from ..models.relationship import Relationship
    from ..models.role_binding import RoleBinding
    from ..models.user import User


T = TypeVar("T", bound="Event")


@_attrs_define
class Event:
    """
    Attributes:
        id (str):
        timestamp (str):
        action (EventAction):
        related (Union['Document', 'GovernedObject', 'Relationship', 'RoleBinding']):
        related_trigger (Union['Label', 'Relationship', None]):
        user (Union['Relationship', 'User', None]):
        from_data (EventFromData):
        to_data (EventToData):
        object_ (Union[Unset, str]):  Default: 'event'.
    """

    id: str
    timestamp: str
    action: EventAction
    related: Union["Document", "GovernedObject", "Relationship", "RoleBinding"]
    related_trigger: Union["Label", "Relationship", None]
    user: Union["Relationship", "User", None]
    from_data: "EventFromData"
    to_data: "EventToData"
    object_: Union[Unset, str] = "event"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.document import Document
        from ..models.governed_object import GovernedObject
        from ..models.label import Label
        from ..models.relationship import Relationship
        from ..models.role_binding import RoleBinding
        from ..models.user import User

        id = self.id

        timestamp = self.timestamp

        action = self.action.value

        related: Dict[str, Any]
        if isinstance(self.related, GovernedObject):
            related = self.related.to_dict()
        elif isinstance(self.related, Document):
            related = self.related.to_dict()
        elif isinstance(self.related, RoleBinding):
            related = self.related.to_dict()
        else:
            related = self.related.to_dict()

        related_trigger: Union[Dict[str, Any], None]
        if isinstance(self.related_trigger, Label):
            related_trigger = self.related_trigger.to_dict()
        elif isinstance(self.related_trigger, Relationship):
            related_trigger = self.related_trigger.to_dict()
        else:
            related_trigger = self.related_trigger

        user: Union[Dict[str, Any], None]
        if isinstance(self.user, User):
            user = self.user.to_dict()
        elif isinstance(self.user, Relationship):
            user = self.user.to_dict()
        else:
            user = self.user

        from_data = self.from_data.to_dict()

        to_data = self.to_data.to_dict()

        object_ = self.object_

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "timestamp": timestamp,
                "action": action,
                "related": related,
                "related_trigger": related_trigger,
                "user": user,
                "from_data": from_data,
                "to_data": to_data,
            }
        )
        if object_ is not UNSET:
            field_dict["object"] = object_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.document import Document
        from ..models.event_from_data import EventFromData
        from ..models.event_to_data import EventToData
        from ..models.governed_object import GovernedObject
        from ..models.label import Label
        from ..models.relationship import Relationship
        from ..models.role_binding import RoleBinding
        from ..models.user import User

        d = src_dict.copy()
        id = d.pop("id")

        timestamp = d.pop("timestamp")

        action = EventAction(d.pop("action"))

        def _parse_related(
            data: object,
        ) -> Union["Document", "GovernedObject", "Relationship", "RoleBinding"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                related_type_0 = GovernedObject.from_dict(data)

                return related_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                related_type_1 = Document.from_dict(data)

                return related_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                related_type_2 = RoleBinding.from_dict(data)

                return related_type_2
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            related_type_3 = Relationship.from_dict(data)

            return related_type_3

        related = _parse_related(d.pop("related"))

        def _parse_related_trigger(
            data: object,
        ) -> Union["Label", "Relationship", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                related_trigger_type_0 = Label.from_dict(data)

                return related_trigger_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                related_trigger_type_1 = Relationship.from_dict(data)

                return related_trigger_type_1
            except:  # noqa: E722
                pass
            return cast(Union["Label", "Relationship", None], data)

        related_trigger = _parse_related_trigger(d.pop("related_trigger"))

        def _parse_user(data: object) -> Union["Relationship", "User", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                user_type_0 = User.from_dict(data)

                return user_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                user_type_1 = Relationship.from_dict(data)

                return user_type_1
            except:  # noqa: E722
                pass
            return cast(Union["Relationship", "User", None], data)

        user = _parse_user(d.pop("user"))

        from_data = EventFromData.from_dict(d.pop("from_data"))

        to_data = EventToData.from_dict(d.pop("to_data"))

        object_ = d.pop("object", UNSET)

        event = cls(
            id=id,
            timestamp=timestamp,
            action=action,
            related=related,
            related_trigger=related_trigger,
            user=user,
            from_data=from_data,
            to_data=to_data,
            object_=object_,
        )

        event.additional_properties = d
        return event

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
