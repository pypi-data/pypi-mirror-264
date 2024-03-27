from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.task_update_state_type_0 import TaskUpdateStateType0
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.task_update_data_type_0 import TaskUpdateDataType0


T = TypeVar("T", bound="TaskUpdate")


@_attrs_define
class TaskUpdate:
    """
    Attributes:
        state (Union[None, TaskUpdateStateType0, Unset]): The target state of the task. For a task in state 'ready', set
            this to 'in_progress' to start the task. For a task in state 'in_progress', set this to 'done' to push the task
            to completion.
        data (Union['TaskUpdateDataType0', None, Unset]):
        owner_id (Union[None, Unset, str]):
    """

    state: Union[None, TaskUpdateStateType0, Unset] = UNSET
    data: Union["TaskUpdateDataType0", None, Unset] = UNSET
    owner_id: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.task_update_data_type_0 import TaskUpdateDataType0

        state: Union[None, Unset, str]
        if isinstance(self.state, Unset):
            state = UNSET
        elif isinstance(self.state, TaskUpdateStateType0):
            state = self.state.value
        else:
            state = self.state

        data: Union[Dict[str, Any], None, Unset]
        if isinstance(self.data, Unset):
            data = UNSET
        elif isinstance(self.data, TaskUpdateDataType0):
            data = self.data.to_dict()
        else:
            data = self.data

        owner_id: Union[None, Unset, str]
        if isinstance(self.owner_id, Unset):
            owner_id = UNSET
        else:
            owner_id = self.owner_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if state is not UNSET:
            field_dict["state"] = state
        if data is not UNSET:
            field_dict["data"] = data
        if owner_id is not UNSET:
            field_dict["owner_id"] = owner_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.task_update_data_type_0 import TaskUpdateDataType0

        d = src_dict.copy()

        def _parse_state(data: object) -> Union[None, TaskUpdateStateType0, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                state_type_0 = TaskUpdateStateType0(data)

                return state_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, TaskUpdateStateType0, Unset], data)

        state = _parse_state(d.pop("state", UNSET))

        def _parse_data(data: object) -> Union["TaskUpdateDataType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_type_0 = TaskUpdateDataType0.from_dict(data)

                return data_type_0
            except:  # noqa: E722
                pass
            return cast(Union["TaskUpdateDataType0", None, Unset], data)

        data = _parse_data(d.pop("data", UNSET))

        def _parse_owner_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        owner_id = _parse_owner_id(d.pop("owner_id", UNSET))

        task_update = cls(
            state=state,
            data=data,
            owner_id=owner_id,
        )

        task_update.additional_properties = d
        return task_update

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
