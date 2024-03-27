from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.task_state import TaskState
from ..models.task_type import TaskType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.document import Document
    from ..models.list_document import ListDocument
    from ..models.list_relationship import ListRelationship
    from ..models.list_task_link import ListTaskLink
    from ..models.phase import Phase
    from ..models.relationship import Relationship
    from ..models.task_args import TaskArgs
    from ..models.task_data import TaskData
    from ..models.user import User


T = TypeVar("T", bound="Task")


@_attrs_define
class Task:
    """
    Attributes:
        object_ (str):
        id (str):
        created_at (str):
        updated_at (str):
        key (str):
        name (str):
        state (TaskState):
        index (int):
        description (Union[None, str]):
        args (TaskArgs):
        autostart (bool):
        phase (Union['Phase', 'Relationship']):
        type (TaskType):
        data (TaskData):
        child_task_links (Union['ListRelationship', 'ListTaskLink']):
        parent_task_links (Union['ListRelationship', 'ListTaskLink']):
        latest_documents (Union['ListDocument', 'ListRelationship']):
        primary_document (Union['Document', 'Relationship', None]):
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
    state: TaskState
    index: int
    description: Union[None, str]
    args: "TaskArgs"
    autostart: bool
    phase: Union["Phase", "Relationship"]
    type: TaskType
    data: "TaskData"
    child_task_links: Union["ListRelationship", "ListTaskLink"]
    parent_task_links: Union["ListRelationship", "ListTaskLink"]
    latest_documents: Union["ListDocument", "ListRelationship"]
    primary_document: Union["Document", "Relationship", None]
    owner: Union["Relationship", "User", None, Unset] = UNSET
    started_at: Union[None, Unset, str] = UNSET
    executed_at: Union[None, Unset, str] = UNSET
    executed_by: Union["Relationship", "User", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.document import Document
        from ..models.list_document import ListDocument
        from ..models.list_task_link import ListTaskLink
        from ..models.phase import Phase
        from ..models.relationship import Relationship
        from ..models.user import User

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

        phase: Dict[str, Any]
        if isinstance(self.phase, Phase):
            phase = self.phase.to_dict()
        else:
            phase = self.phase.to_dict()

        type = self.type.value

        data = self.data.to_dict()

        child_task_links: Dict[str, Any]
        if isinstance(self.child_task_links, ListTaskLink):
            child_task_links = self.child_task_links.to_dict()
        else:
            child_task_links = self.child_task_links.to_dict()

        parent_task_links: Dict[str, Any]
        if isinstance(self.parent_task_links, ListTaskLink):
            parent_task_links = self.parent_task_links.to_dict()
        else:
            parent_task_links = self.parent_task_links.to_dict()

        latest_documents: Dict[str, Any]
        if isinstance(self.latest_documents, ListDocument):
            latest_documents = self.latest_documents.to_dict()
        else:
            latest_documents = self.latest_documents.to_dict()

        primary_document: Union[Dict[str, Any], None]
        if isinstance(self.primary_document, Document):
            primary_document = self.primary_document.to_dict()
        elif isinstance(self.primary_document, Relationship):
            primary_document = self.primary_document.to_dict()
        else:
            primary_document = self.primary_document

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
                "phase": phase,
                "type": type,
                "data": data,
                "child_task_links": child_task_links,
                "parent_task_links": parent_task_links,
                "latest_documents": latest_documents,
                "primary_document": primary_document,
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
        from ..models.document import Document
        from ..models.list_document import ListDocument
        from ..models.list_relationship import ListRelationship
        from ..models.list_task_link import ListTaskLink
        from ..models.phase import Phase
        from ..models.relationship import Relationship
        from ..models.task_args import TaskArgs
        from ..models.task_data import TaskData
        from ..models.user import User

        d = src_dict.copy()
        object_ = d.pop("object")

        id = d.pop("id")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        key = d.pop("key")

        name = d.pop("name")

        state = TaskState(d.pop("state"))

        index = d.pop("index")

        def _parse_description(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        description = _parse_description(d.pop("description"))

        args = TaskArgs.from_dict(d.pop("args"))

        autostart = d.pop("autostart")

        def _parse_phase(data: object) -> Union["Phase", "Relationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                phase_type_0 = Phase.from_dict(data)

                return phase_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            phase_type_1 = Relationship.from_dict(data)

            return phase_type_1

        phase = _parse_phase(d.pop("phase"))

        type = TaskType(d.pop("type"))

        data = TaskData.from_dict(d.pop("data"))

        def _parse_child_task_links(
            data: object,
        ) -> Union["ListRelationship", "ListTaskLink"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                child_task_links_type_0 = ListTaskLink.from_dict(data)

                return child_task_links_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            child_task_links_type_1 = ListRelationship.from_dict(data)

            return child_task_links_type_1

        child_task_links = _parse_child_task_links(d.pop("child_task_links"))

        def _parse_parent_task_links(
            data: object,
        ) -> Union["ListRelationship", "ListTaskLink"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                parent_task_links_type_0 = ListTaskLink.from_dict(data)

                return parent_task_links_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            parent_task_links_type_1 = ListRelationship.from_dict(data)

            return parent_task_links_type_1

        parent_task_links = _parse_parent_task_links(d.pop("parent_task_links"))

        def _parse_latest_documents(
            data: object,
        ) -> Union["ListDocument", "ListRelationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                latest_documents_type_0 = ListDocument.from_dict(data)

                return latest_documents_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            latest_documents_type_1 = ListRelationship.from_dict(data)

            return latest_documents_type_1

        latest_documents = _parse_latest_documents(d.pop("latest_documents"))

        def _parse_primary_document(
            data: object,
        ) -> Union["Document", "Relationship", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                primary_document_type_0 = Document.from_dict(data)

                return primary_document_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                primary_document_type_1 = Relationship.from_dict(data)

                return primary_document_type_1
            except:  # noqa: E722
                pass
            return cast(Union["Document", "Relationship", None], data)

        primary_document = _parse_primary_document(d.pop("primary_document"))

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

        task = cls(
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
            phase=phase,
            type=type,
            data=data,
            child_task_links=child_task_links,
            parent_task_links=parent_task_links,
            latest_documents=latest_documents,
            primary_document=primary_document,
            owner=owner,
            started_at=started_at,
            executed_at=executed_at,
            executed_by=executed_by,
        )

        task.additional_properties = d
        return task

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
