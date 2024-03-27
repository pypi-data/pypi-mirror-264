from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.phase_state import PhaseState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_phase_link import ListPhaseLink
    from ..models.list_relationship import ListRelationship
    from ..models.list_task import ListTask
    from ..models.phase_args import PhaseArgs
    from ..models.relationship import Relationship
    from ..models.user import User
    from ..models.workflow import Workflow


T = TypeVar("T", bound="Phase")


@_attrs_define
class Phase:
    """
    Attributes:
        object_ (str):
        id (str):
        created_at (str):
        updated_at (str):
        key (str):
        name (str):
        state (PhaseState):
        index (int):
        description (Union[None, str]):
        args (PhaseArgs):
        autostart (bool):
        workflow (Union['Relationship', 'Workflow']):
        child_phase_links (Union['ListPhaseLink', 'ListRelationship']):
        parent_phase_links (Union['ListPhaseLink', 'ListRelationship']):
        tasks (Union['ListRelationship', 'ListTask']):
        owner (Union['Relationship', 'User', None, Unset]):
        started_at (Union[None, Unset, str]):
        executed_at (Union[None, Unset, str]):
        executed_by (Union['Relationship', 'User', None, Unset]):
    """

    object_: str
    id: str
    created_at: str
    updated_at: str
    key: str
    name: str
    state: PhaseState
    index: int
    description: Union[None, str]
    args: "PhaseArgs"
    autostart: bool
    workflow: Union["Relationship", "Workflow"]
    child_phase_links: Union["ListPhaseLink", "ListRelationship"]
    parent_phase_links: Union["ListPhaseLink", "ListRelationship"]
    tasks: Union["ListRelationship", "ListTask"]
    owner: Union["Relationship", "User", None, Unset] = UNSET
    started_at: Union[None, Unset, str] = UNSET
    executed_at: Union[None, Unset, str] = UNSET
    executed_by: Union["Relationship", "User", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.list_phase_link import ListPhaseLink
        from ..models.list_task import ListTask
        from ..models.relationship import Relationship
        from ..models.user import User
        from ..models.workflow import Workflow

        object_ = self.object_

        id = self.id

        created_at = self.created_at

        updated_at = self.updated_at

        key = self.key

        name = self.name

        state = self.state.value

        index = self.index

        description: Union[None, str]
        description = self.description

        args = self.args.to_dict()

        autostart = self.autostart

        workflow: Dict[str, Any]
        if isinstance(self.workflow, Workflow):
            workflow = self.workflow.to_dict()
        else:
            workflow = self.workflow.to_dict()

        child_phase_links: Dict[str, Any]
        if isinstance(self.child_phase_links, ListPhaseLink):
            child_phase_links = self.child_phase_links.to_dict()
        else:
            child_phase_links = self.child_phase_links.to_dict()

        parent_phase_links: Dict[str, Any]
        if isinstance(self.parent_phase_links, ListPhaseLink):
            parent_phase_links = self.parent_phase_links.to_dict()
        else:
            parent_phase_links = self.parent_phase_links.to_dict()

        tasks: Dict[str, Any]
        if isinstance(self.tasks, ListTask):
            tasks = self.tasks.to_dict()
        else:
            tasks = self.tasks.to_dict()

        owner: Union[Dict[str, Any], None, Unset]
        if isinstance(self.owner, Unset):
            owner = UNSET
        elif isinstance(self.owner, User):
            owner = self.owner.to_dict()
        elif isinstance(self.owner, Relationship):
            owner = self.owner.to_dict()
        else:
            owner = self.owner

        started_at: Union[None, Unset, str]
        if isinstance(self.started_at, Unset):
            started_at = UNSET
        else:
            started_at = self.started_at

        executed_at: Union[None, Unset, str]
        if isinstance(self.executed_at, Unset):
            executed_at = UNSET
        else:
            executed_at = self.executed_at

        executed_by: Union[Dict[str, Any], None, Unset]
        if isinstance(self.executed_by, Unset):
            executed_by = UNSET
        elif isinstance(self.executed_by, User):
            executed_by = self.executed_by.to_dict()
        elif isinstance(self.executed_by, Relationship):
            executed_by = self.executed_by.to_dict()
        else:
            executed_by = self.executed_by

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "key": key,
                "name": name,
                "state": state,
                "index": index,
                "description": description,
                "args": args,
                "autostart": autostart,
                "workflow": workflow,
                "child_phase_links": child_phase_links,
                "parent_phase_links": parent_phase_links,
                "tasks": tasks,
            }
        )
        if owner is not UNSET:
            field_dict["owner"] = owner
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if executed_at is not UNSET:
            field_dict["executed_at"] = executed_at
        if executed_by is not UNSET:
            field_dict["executed_by"] = executed_by

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_phase_link import ListPhaseLink
        from ..models.list_relationship import ListRelationship
        from ..models.list_task import ListTask
        from ..models.phase_args import PhaseArgs
        from ..models.relationship import Relationship
        from ..models.user import User
        from ..models.workflow import Workflow

        d = src_dict.copy()
        object_ = d.pop("object")

        id = d.pop("id")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        key = d.pop("key")

        name = d.pop("name")

        state = PhaseState(d.pop("state"))

        index = d.pop("index")

        def _parse_description(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        description = _parse_description(d.pop("description"))

        args = PhaseArgs.from_dict(d.pop("args"))

        autostart = d.pop("autostart")

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

        def _parse_child_phase_links(
            data: object,
        ) -> Union["ListPhaseLink", "ListRelationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                child_phase_links_type_0 = ListPhaseLink.from_dict(data)

                return child_phase_links_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            child_phase_links_type_1 = ListRelationship.from_dict(data)

            return child_phase_links_type_1

        child_phase_links = _parse_child_phase_links(d.pop("child_phase_links"))

        def _parse_parent_phase_links(
            data: object,
        ) -> Union["ListPhaseLink", "ListRelationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                parent_phase_links_type_0 = ListPhaseLink.from_dict(data)

                return parent_phase_links_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            parent_phase_links_type_1 = ListRelationship.from_dict(data)

            return parent_phase_links_type_1

        parent_phase_links = _parse_parent_phase_links(d.pop("parent_phase_links"))

        def _parse_tasks(data: object) -> Union["ListRelationship", "ListTask"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                tasks_type_0 = ListTask.from_dict(data)

                return tasks_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            tasks_type_1 = ListRelationship.from_dict(data)

            return tasks_type_1

        tasks = _parse_tasks(d.pop("tasks"))

        def _parse_owner(data: object) -> Union["Relationship", "User", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                owner_type_0 = User.from_dict(data)

                return owner_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                owner_type_1 = Relationship.from_dict(data)

                return owner_type_1
            except:  # noqa: E722
                pass
            return cast(Union["Relationship", "User", None, Unset], data)

        owner = _parse_owner(d.pop("owner", UNSET))

        def _parse_started_at(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        started_at = _parse_started_at(d.pop("started_at", UNSET))

        def _parse_executed_at(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        executed_at = _parse_executed_at(d.pop("executed_at", UNSET))

        def _parse_executed_by(
            data: object,
        ) -> Union["Relationship", "User", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                executed_by_type_0 = User.from_dict(data)

                return executed_by_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                executed_by_type_1 = Relationship.from_dict(data)

                return executed_by_type_1
            except:  # noqa: E722
                pass
            return cast(Union["Relationship", "User", None, Unset], data)

        executed_by = _parse_executed_by(d.pop("executed_by", UNSET))

        phase = cls(
            object_=object_,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            key=key,
            name=name,
            state=state,
            index=index,
            description=description,
            args=args,
            autostart=autostart,
            workflow=workflow,
            child_phase_links=child_phase_links,
            parent_phase_links=parent_phase_links,
            tasks=tasks,
            owner=owner,
            started_at=started_at,
            executed_at=executed_at,
            executed_by=executed_by,
        )

        phase.additional_properties = d
        return phase

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
