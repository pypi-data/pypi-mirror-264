from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Type,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.workflow_state import WorkflowState

if TYPE_CHECKING:
    from ..models.list_phase import ListPhase
    from ..models.list_relationship import ListRelationship
    from ..models.list_review import ListReview
    from ..models.project import Project
    from ..models.relationship import Relationship
    from ..models.workflow_template import WorkflowTemplate


T = TypeVar("T", bound="Workflow")


@_attrs_define
class Workflow:
    """
    Attributes:
        object_ (str):
        id (str):
        created_at (str):
        updated_at (str):
        project (Union['Project', 'Relationship']):
        name (str):
        state (WorkflowState):
        workflow_template (Union['Relationship', 'WorkflowTemplate', None]):
        phases (Union['ListPhase', 'ListRelationship']):
        reviews (Union['ListRelationship', 'ListReview']):
    """

    object_: str
    id: str
    created_at: str
    updated_at: str
    project: Union["Project", "Relationship"]
    name: str
    state: WorkflowState
    workflow_template: Union["Relationship", "WorkflowTemplate", None]
    phases: Union["ListPhase", "ListRelationship"]
    reviews: Union["ListRelationship", "ListReview"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.list_phase import ListPhase
        from ..models.list_review import ListReview
        from ..models.project import Project
        from ..models.relationship import Relationship
        from ..models.workflow_template import WorkflowTemplate

        object_ = self.object_

        id = self.id

        created_at = self.created_at

        updated_at = self.updated_at

        project: Dict[str, Any]
        if isinstance(self.project, Project):
            project = self.project.to_dict()
        else:
            project = self.project.to_dict()

        name = self.name

        state = self.state.value

        workflow_template: Union[Dict[str, Any], None]
        if isinstance(self.workflow_template, WorkflowTemplate):
            workflow_template = self.workflow_template.to_dict()
        elif isinstance(self.workflow_template, Relationship):
            workflow_template = self.workflow_template.to_dict()
        else:
            workflow_template = self.workflow_template

        phases: Dict[str, Any]
        if isinstance(self.phases, ListPhase):
            phases = self.phases.to_dict()
        else:
            phases = self.phases.to_dict()

        reviews: Dict[str, Any]
        if isinstance(self.reviews, ListReview):
            reviews = self.reviews.to_dict()
        else:
            reviews = self.reviews.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "project": project,
                "name": name,
                "state": state,
                "workflow_template": workflow_template,
                "phases": phases,
                "reviews": reviews,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_phase import ListPhase
        from ..models.list_relationship import ListRelationship
        from ..models.list_review import ListReview
        from ..models.project import Project
        from ..models.relationship import Relationship
        from ..models.workflow_template import WorkflowTemplate

        d = src_dict.copy()
        object_ = d.pop("object")

        id = d.pop("id")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        def _parse_project(data: object) -> Union["Project", "Relationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                project_type_0 = Project.from_dict(data)

                return project_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            project_type_1 = Relationship.from_dict(data)

            return project_type_1

        project = _parse_project(d.pop("project"))

        name = d.pop("name")

        state = WorkflowState(d.pop("state"))

        def _parse_workflow_template(
            data: object,
        ) -> Union["Relationship", "WorkflowTemplate", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                workflow_template_type_0 = WorkflowTemplate.from_dict(data)

                return workflow_template_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                workflow_template_type_1 = Relationship.from_dict(data)

                return workflow_template_type_1
            except:  # noqa: E722
                pass
            return cast(Union["Relationship", "WorkflowTemplate", None], data)

        workflow_template = _parse_workflow_template(d.pop("workflow_template"))

        def _parse_phases(data: object) -> Union["ListPhase", "ListRelationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                phases_type_0 = ListPhase.from_dict(data)

                return phases_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            phases_type_1 = ListRelationship.from_dict(data)

            return phases_type_1

        phases = _parse_phases(d.pop("phases"))

        def _parse_reviews(data: object) -> Union["ListRelationship", "ListReview"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                reviews_type_0 = ListReview.from_dict(data)

                return reviews_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            reviews_type_1 = ListRelationship.from_dict(data)

            return reviews_type_1

        reviews = _parse_reviews(d.pop("reviews"))

        workflow = cls(
            object_=object_,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            project=project,
            name=name,
            state=state,
            workflow_template=workflow_template,
            phases=phases,
            reviews=reviews,
        )

        workflow.additional_properties = d
        return workflow

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
