from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.review_action_action import ReviewActionAction
from ..models.review_action_state import ReviewActionState

if TYPE_CHECKING:
    from ..models.phase import Phase
    from ..models.relationship import Relationship
    from ..models.review import Review
    from ..models.review_thread import ReviewThread
    from ..models.task import Task
    from ..models.user import User
    from ..models.workflow import Workflow


T = TypeVar("T", bound="ReviewAction")


@_attrs_define
class ReviewAction:
    """
    Attributes:
        object_ (str):
        id (str):
        created_at (str):
        updated_at (str):
        user (Union['Relationship', 'User']):
        action (ReviewActionAction):
        related (Union['Phase', 'Relationship', 'Task', 'Workflow']):
        review (Union['Relationship', 'Review']):
        state (ReviewActionState):
        review_thread (Union['Relationship', 'ReviewThread', None]):
        comment (Union[None, str]):
    """

    object_: str
    id: str
    created_at: str
    updated_at: str
    user: Union["Relationship", "User"]
    action: ReviewActionAction
    related: Union["Phase", "Relationship", "Task", "Workflow"]
    review: Union["Relationship", "Review"]
    state: ReviewActionState
    review_thread: Union["Relationship", "ReviewThread", None]
    comment: Union[None, str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.phase import Phase
        from ..models.relationship import Relationship
        from ..models.review import Review
        from ..models.review_thread import ReviewThread
        from ..models.task import Task
        from ..models.user import User
        from ..models.workflow import Workflow

        object_ = self.object_

        id = self.id

        created_at = self.created_at

        updated_at = self.updated_at

        user: Dict[str, Any]
        if isinstance(self.user, User):
            user = self.user.to_dict()
        else:
            user = self.user.to_dict()

        action = self.action.value

        related: Dict[str, Any]
        if isinstance(self.related, Workflow):
            related = self.related.to_dict()
        elif isinstance(self.related, Phase):
            related = self.related.to_dict()
        elif isinstance(self.related, Task):
            related = self.related.to_dict()
        else:
            related = self.related.to_dict()

        review: Dict[str, Any]
        if isinstance(self.review, Review):
            review = self.review.to_dict()
        else:
            review = self.review.to_dict()

        state = self.state.value

        review_thread: Union[Dict[str, Any], None]
        if isinstance(self.review_thread, ReviewThread):
            review_thread = self.review_thread.to_dict()
        elif isinstance(self.review_thread, Relationship):
            review_thread = self.review_thread.to_dict()
        else:
            review_thread = self.review_thread

        comment: Union[None, str]
        comment = self.comment

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "user": user,
                "action": action,
                "related": related,
                "review": review,
                "state": state,
                "review_thread": review_thread,
                "comment": comment,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.phase import Phase
        from ..models.relationship import Relationship
        from ..models.review import Review
        from ..models.review_thread import ReviewThread
        from ..models.task import Task
        from ..models.user import User
        from ..models.workflow import Workflow

        d = src_dict.copy()
        object_ = d.pop("object")

        id = d.pop("id")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

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

        action = ReviewActionAction(d.pop("action"))

        def _parse_related(
            data: object,
        ) -> Union["Phase", "Relationship", "Task", "Workflow"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                related_type_0 = Workflow.from_dict(data)

                return related_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                related_type_1 = Phase.from_dict(data)

                return related_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                related_type_2 = Task.from_dict(data)

                return related_type_2
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            related_type_3 = Relationship.from_dict(data)

            return related_type_3

        related = _parse_related(d.pop("related"))

        def _parse_review(data: object) -> Union["Relationship", "Review"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                review_type_0 = Review.from_dict(data)

                return review_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            review_type_1 = Relationship.from_dict(data)

            return review_type_1

        review = _parse_review(d.pop("review"))

        state = ReviewActionState(d.pop("state"))

        def _parse_review_thread(
            data: object,
        ) -> Union["Relationship", "ReviewThread", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                review_thread_type_0 = ReviewThread.from_dict(data)

                return review_thread_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                review_thread_type_1 = Relationship.from_dict(data)

                return review_thread_type_1
            except:  # noqa: E722
                pass
            return cast(Union["Relationship", "ReviewThread", None], data)

        review_thread = _parse_review_thread(d.pop("review_thread"))

        def _parse_comment(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        comment = _parse_comment(d.pop("comment"))

        review_action = cls(
            object_=object_,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            user=user,
            action=action,
            related=related,
            review=review,
            state=state,
            review_thread=review_thread,
            comment=comment,
        )

        review_action.additional_properties = d
        return review_action

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
