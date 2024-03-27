from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workflow import Workflow


T = TypeVar("T", bound="ListWorkflow")


@_attrs_define
class ListWorkflow:
    """
    Attributes:
        has_more (bool):
        data (List['Workflow']):
        object_ (Union[Unset, str]):  Default: 'list'.
    """

    has_more: bool
    data: List["Workflow"]
    object_: Union[Unset, str] = "list"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        has_more = self.has_more

        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        object_ = self.object_

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "has_more": has_more,
                "data": data,
            }
        )
        if object_ is not UNSET:
            field_dict["object"] = object_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.workflow import Workflow

        d = src_dict.copy()
        has_more = d.pop("has_more")

        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = Workflow.from_dict(data_item_data)

            data.append(data_item)

        object_ = d.pop("object", UNSET)

        list_workflow = cls(
            has_more=has_more,
            data=data,
            object_=object_,
        )

        list_workflow.additional_properties = d
        return list_workflow

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
