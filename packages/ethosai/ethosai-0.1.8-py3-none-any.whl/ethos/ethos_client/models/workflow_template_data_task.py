from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.workflow_template_data_task_type import WorkflowTemplateDataTaskType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workflow_template_data_task_args_type_0 import (
        WorkflowTemplateDataTaskArgsType0,
    )


T = TypeVar("T", bound="WorkflowTemplateDataTask")


@_attrs_define
class WorkflowTemplateDataTask:
    """
    Attributes:
        type (WorkflowTemplateDataTaskType):
        name (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
        args (Union['WorkflowTemplateDataTaskArgsType0', None, Unset]):
        start_depends_on (Union[List[str], None, Unset]):
        completion_depends_on (Union[List[str], None, Unset]):
        autostart (Union[None, Unset, bool]):
    """

    type: WorkflowTemplateDataTaskType
    name: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    args: Union["WorkflowTemplateDataTaskArgsType0", None, Unset] = UNSET
    start_depends_on: Union[List[str], None, Unset] = UNSET
    completion_depends_on: Union[List[str], None, Unset] = UNSET
    autostart: Union[None, Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        from ..models.workflow_template_data_task_args_type_0 import (
            WorkflowTemplateDataTaskArgsType0,
        )

        type = self.type.value

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        args: Union[Dict[str, Any], None, Unset]
        if isinstance(self.args, Unset):
            args = UNSET
        elif isinstance(self.args, WorkflowTemplateDataTaskArgsType0):
            args = self.args.to_dict()
        else:
            args = self.args

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

        autostart: Union[None, Unset, bool]
        if isinstance(self.autostart, Unset):
            autostart = UNSET
        else:
            autostart = self.autostart

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "type": type,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if args is not UNSET:
            field_dict["args"] = args
        if start_depends_on is not UNSET:
            field_dict["start_depends_on"] = start_depends_on
        if completion_depends_on is not UNSET:
            field_dict["completion_depends_on"] = completion_depends_on
        if autostart is not UNSET:
            field_dict["autostart"] = autostart

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.workflow_template_data_task_args_type_0 import (
            WorkflowTemplateDataTaskArgsType0,
        )

        d = src_dict.copy()
        type = WorkflowTemplateDataTaskType(d.pop("type"))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_args(
            data: object,
        ) -> Union["WorkflowTemplateDataTaskArgsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                args_type_0 = WorkflowTemplateDataTaskArgsType0.from_dict(data)

                return args_type_0
            except:  # noqa: E722
                pass
            return cast(Union["WorkflowTemplateDataTaskArgsType0", None, Unset], data)

        args = _parse_args(d.pop("args", UNSET))

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

        def _parse_autostart(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        autostart = _parse_autostart(d.pop("autostart", UNSET))

        workflow_template_data_task = cls(
            type=type,
            name=name,
            description=description,
            args=args,
            start_depends_on=start_depends_on,
            completion_depends_on=completion_depends_on,
            autostart=autostart,
        )

        return workflow_template_data_task
