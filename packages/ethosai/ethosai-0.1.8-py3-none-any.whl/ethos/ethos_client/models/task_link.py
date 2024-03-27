from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.relationship import Relationship
    from ..models.task import Task


T = TypeVar("T", bound="TaskLink")


@_attrs_define
class TaskLink:
    """
    Attributes:
        object_ (str):
        id (str):
        created_at (str):
        updated_at (str):
        parent_task (Union['Relationship', 'Task']):
        child_task (Union['Relationship', 'Task']):
    """

    object_: str
    id: str
    created_at: str
    updated_at: str
    parent_task: Union["Relationship", "Task"]
    child_task: Union["Relationship", "Task"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.task import Task

        object_ = self.object_

        id = self.id

        created_at = self.created_at

        updated_at = self.updated_at

        parent_task: Dict[str, Any]
        if isinstance(self.parent_task, Task):
            parent_task = self.parent_task.to_dict()
        else:
            parent_task = self.parent_task.to_dict()

        child_task: Dict[str, Any]
        if isinstance(self.child_task, Task):
            child_task = self.child_task.to_dict()
        else:
            child_task = self.child_task.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "parent_task": parent_task,
                "child_task": child_task,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.relationship import Relationship
        from ..models.task import Task

        d = src_dict.copy()
        object_ = d.pop("object")

        id = d.pop("id")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        def _parse_parent_task(data: object) -> Union["Relationship", "Task"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                parent_task_type_0 = Task.from_dict(data)

                return parent_task_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            parent_task_type_1 = Relationship.from_dict(data)

            return parent_task_type_1

        parent_task = _parse_parent_task(d.pop("parent_task"))

        def _parse_child_task(data: object) -> Union["Relationship", "Task"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                child_task_type_0 = Task.from_dict(data)

                return child_task_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            child_task_type_1 = Relationship.from_dict(data)

            return child_task_type_1

        child_task = _parse_child_task(d.pop("child_task"))

        task_link = cls(
            object_=object_,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            parent_task=parent_task,
            child_task=child_task,
        )

        task_link.additional_properties = d
        return task_link

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
