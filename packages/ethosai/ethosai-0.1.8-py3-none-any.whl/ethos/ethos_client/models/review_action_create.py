from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.review_action_create_action import ReviewActionCreateAction
from ..types import UNSET, Unset

T = TypeVar("T", bound="ReviewActionCreate")


@_attrs_define
class ReviewActionCreate:
    """
    Attributes:
        action (ReviewActionCreateAction):
        related_id (str):
        review_id (str):
        review_thread_id (Union[None, Unset, str]):
        comment (Union[None, Unset, str]):
    """

    action: ReviewActionCreateAction
    related_id: str
    review_id: str
    review_thread_id: Union[None, Unset, str] = UNSET
    comment: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        action = self.action.value

        related_id = self.related_id

        review_id = self.review_id

        review_thread_id: Union[None, Unset, str]
        if isinstance(self.review_thread_id, Unset):
            review_thread_id = UNSET
        else:
            review_thread_id = self.review_thread_id

        comment: Union[None, Unset, str]
        if isinstance(self.comment, Unset):
            comment = UNSET
        else:
            comment = self.comment

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action": action,
                "related_id": related_id,
                "review_id": review_id,
            }
        )
        if review_thread_id is not UNSET:
            field_dict["review_thread_id"] = review_thread_id
        if comment is not UNSET:
            field_dict["comment"] = comment

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        action = ReviewActionCreateAction(d.pop("action"))

        related_id = d.pop("related_id")

        review_id = d.pop("review_id")

        def _parse_review_thread_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        review_thread_id = _parse_review_thread_id(d.pop("review_thread_id", UNSET))

        def _parse_comment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comment = _parse_comment(d.pop("comment", UNSET))

        review_action_create = cls(
            action=action,
            related_id=related_id,
            review_id=review_id,
            review_thread_id=review_thread_id,
            comment=comment,
        )

        review_action_create.additional_properties = d
        return review_action_create

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
