from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.list_relationship import ListRelationship
    from ..models.list_review_action import ListReviewAction
    from ..models.relationship import Relationship
    from ..models.user import User
    from ..models.workflow import Workflow


T = TypeVar("T", bound="Review")


@_attrs_define
class Review:
    """
    Attributes:
        object_ (str):
        id (str):
        created_at (str):
        updated_at (str):
        state (str):
        user (Union['Relationship', 'User']):
        workflow (Union['Relationship', 'Workflow']):
        review_actions (Union['ListRelationship', 'ListReviewAction']):
    """

    object_: str
    id: str
    created_at: str
    updated_at: str
    state: str
    user: Union["Relationship", "User"]
    workflow: Union["Relationship", "Workflow"]
    review_actions: Union["ListRelationship", "ListReviewAction"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.list_review_action import ListReviewAction
        from ..models.user import User
        from ..models.workflow import Workflow

        object_ = self.object_

        id = self.id

        created_at = self.created_at

        updated_at = self.updated_at

        state = self.state

        user: Dict[str, Any]
        if isinstance(self.user, User):
            user = self.user.to_dict()
        else:
            user = self.user.to_dict()

        workflow: Dict[str, Any]
        if isinstance(self.workflow, Workflow):
            workflow = self.workflow.to_dict()
        else:
            workflow = self.workflow.to_dict()

        review_actions: Dict[str, Any]
        if isinstance(self.review_actions, ListReviewAction):
            review_actions = self.review_actions.to_dict()
        else:
            review_actions = self.review_actions.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "state": state,
                "user": user,
                "workflow": workflow,
                "review_actions": review_actions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_relationship import ListRelationship
        from ..models.list_review_action import ListReviewAction
        from ..models.relationship import Relationship
        from ..models.user import User
        from ..models.workflow import Workflow

        d = src_dict.copy()
        object_ = d.pop("object")

        id = d.pop("id")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        state = d.pop("state")

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

        def _parse_workflow(data: object) -> Union["Relationship", "Workflow"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                workflow_type_0 = Workflow.from_dict(data)

                return workflow_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            workflow_type_1 = Relationship.from_dict(data)

            return workflow_type_1

        workflow = _parse_workflow(d.pop("workflow"))

        def _parse_review_actions(
            data: object,
        ) -> Union["ListRelationship", "ListReviewAction"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                review_actions_type_0 = ListReviewAction.from_dict(data)

                return review_actions_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            review_actions_type_1 = ListRelationship.from_dict(data)

            return review_actions_type_1

        review_actions = _parse_review_actions(d.pop("review_actions"))

        review = cls(
            object_=object_,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            state=state,
            user=user,
            workflow=workflow,
            review_actions=review_actions,
        )

        review.additional_properties = d
        return review

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
