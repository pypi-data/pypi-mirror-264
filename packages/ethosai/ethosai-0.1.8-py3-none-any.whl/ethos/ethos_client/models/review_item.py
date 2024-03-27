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

from ..models.review_item_state import ReviewItemState
from ..models.review_item_state_reason import ReviewItemStateReason

if TYPE_CHECKING:
    from ..models.list_relationship import ListRelationship
    from ..models.list_review_thread import ListReviewThread
    from ..models.phase import Phase
    from ..models.relationship import Relationship
    from ..models.task import Task
    from ..models.workflow import Workflow


T = TypeVar("T", bound="ReviewItem")


@_attrs_define
class ReviewItem:
    """
    Attributes:
        object_ (str):
        id (str):
        created_at (str):
        updated_at (str):
        state (ReviewItemState):
        state_reason (ReviewItemStateReason):
        related (Union['Phase', 'Relationship', 'Task', 'Workflow']):
        review_threads (Union['ListRelationship', 'ListReviewThread']):
    """

    object_: str
    id: str
    created_at: str
    updated_at: str
    state: ReviewItemState
    state_reason: ReviewItemStateReason
    related: Union["Phase", "Relationship", "Task", "Workflow"]
    review_threads: Union["ListRelationship", "ListReviewThread"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.list_review_thread import ListReviewThread
        from ..models.phase import Phase
        from ..models.task import Task
        from ..models.workflow import Workflow

        object_ = self.object_

        id = self.id

        created_at = self.created_at

        updated_at = self.updated_at

        state = self.state.value

        state_reason = self.state_reason.value

        related: Dict[str, Any]
        if isinstance(self.related, Workflow):
            related = self.related.to_dict()
        elif isinstance(self.related, Phase):
            related = self.related.to_dict()
        elif isinstance(self.related, Task):
            related = self.related.to_dict()
        else:
            related = self.related.to_dict()

        review_threads: Dict[str, Any]
        if isinstance(self.review_threads, ListReviewThread):
            review_threads = self.review_threads.to_dict()
        else:
            review_threads = self.review_threads.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "state": state,
                "state_reason": state_reason,
                "related": related,
                "review_threads": review_threads,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_relationship import ListRelationship
        from ..models.list_review_thread import ListReviewThread
        from ..models.phase import Phase
        from ..models.relationship import Relationship
        from ..models.task import Task
        from ..models.workflow import Workflow

        d = src_dict.copy()
        object_ = d.pop("object")

        id = d.pop("id")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        state = ReviewItemState(d.pop("state"))

        state_reason = ReviewItemStateReason(d.pop("state_reason"))

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

        def _parse_review_threads(
            data: object,
        ) -> Union["ListRelationship", "ListReviewThread"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                review_threads_type_0 = ListReviewThread.from_dict(data)

                return review_threads_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            review_threads_type_1 = ListRelationship.from_dict(data)

            return review_threads_type_1

        review_threads = _parse_review_threads(d.pop("review_threads"))

        review_item = cls(
            object_=object_,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            state=state,
            state_reason=state_reason,
            related=related,
            review_threads=review_threads,
        )

        review_item.additional_properties = d
        return review_item

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
