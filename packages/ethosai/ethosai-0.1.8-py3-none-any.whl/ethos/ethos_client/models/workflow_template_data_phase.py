from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workflow_template_data_phase_tasks_type_0 import (
        WorkflowTemplateDataPhaseTasksType0,
    )


T = TypeVar("T", bound="WorkflowTemplateDataPhase")


@_attrs_define
class WorkflowTemplateDataPhase:
    """
    Attributes:
        name (Union[None, Unset, str]):
        tasks (Union['WorkflowTemplateDataPhaseTasksType0', None, Unset]):
        start_depends_on (Union[List[str], None, Unset]):
        completion_depends_on (Union[List[str], None, Unset]):
        description (Union[None, Unset, str]):
    """

    name: Union[None, Unset, str] = UNSET
    tasks: Union["WorkflowTemplateDataPhaseTasksType0", None, Unset] = UNSET
    start_depends_on: Union[List[str], None, Unset] = UNSET
    completion_depends_on: Union[List[str], None, Unset] = UNSET
    description: Union[None, Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        from ..models.workflow_template_data_phase_tasks_type_0 import (
            WorkflowTemplateDataPhaseTasksType0,
        )

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        tasks: Union[Dict[str, Any], None, Unset]
        if isinstance(self.tasks, Unset):
            tasks = UNSET
        elif isinstance(self.tasks, WorkflowTemplateDataPhaseTasksType0):
            tasks = self.tasks.to_dict()
        else:
            tasks = self.tasks

        start_depends_on: Union[List[str], None, Unset]
        if isinstance(self.start_depends_on, Unset):
            start_depends_on = UNSET
        elif isinstance(self.start_depends_on, list):
            start_depends_on = self.start_depends_on

        else:
            start_depends_on = self.start_depends_on

        completion_depends_on: Union[List[str], None, Unset]
        if isinstance(self.completion_depends_on, Unset):
            completion_depends_on = UNSET
        elif isinstance(self.completion_depends_on, list):
            completion_depends_on = self.completion_depends_on

        else:
            completion_depends_on = self.completion_depends_on

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if tasks is not UNSET:
            field_dict["tasks"] = tasks
        if start_depends_on is not UNSET:
            field_dict["start_depends_on"] = start_depends_on
        if completion_depends_on is not UNSET:
            field_dict["completion_depends_on"] = completion_depends_on
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.workflow_template_data_phase_tasks_type_0 import (
            WorkflowTemplateDataPhaseTasksType0,
        )

        d = src_dict.copy()

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_tasks(
            data: object,
        ) -> Union["WorkflowTemplateDataPhaseTasksType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                tasks_type_0 = WorkflowTemplateDataPhaseTasksType0.from_dict(data)

                return tasks_type_0
            except:  # noqa: E722
                pass
            return cast(Union["WorkflowTemplateDataPhaseTasksType0", None, Unset], data)

        tasks = _parse_tasks(d.pop("tasks", UNSET))

        def _parse_start_depends_on(data: object) -> Union[List[str], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                start_depends_on_type_0 = cast(List[str], data)

                return start_depends_on_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None, Unset], data)

        start_depends_on = _parse_start_depends_on(d.pop("start_depends_on", UNSET))

        def _parse_completion_depends_on(data: object) -> Union[List[str], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                completion_depends_on_type_0 = cast(List[str], data)

                return completion_depends_on_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None, Unset], data)

        completion_depends_on = _parse_completion_depends_on(
            d.pop("completion_depends_on", UNSET)
        )

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        workflow_template_data_phase = cls(
            name=name,
            tasks=tasks,
            start_depends_on=start_depends_on,
            completion_depends_on=completion_depends_on,
            description=description,
        )

        return workflow_template_data_phase
