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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.structured_document_data import StructuredDocumentData


T = TypeVar("T", bound="TaskDocumentUpdate")


@_attrs_define
class TaskDocumentUpdate:
    """
    Attributes:
        data (Union['StructuredDocumentData', None, Unset]):
    """

    data: Union["StructuredDocumentData", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.structured_document_data import StructuredDocumentData

        data: Union[Dict[str, Any], None, Unset]
        if isinstance(self.data, Unset):
            data = UNSET
        elif isinstance(self.data, StructuredDocumentData):
            data = self.data.to_dict()
        else:
            data = self.data

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.structured_document_data import StructuredDocumentData

        d = src_dict.copy()

        def _parse_data(data: object) -> Union["StructuredDocumentData", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_type_0 = StructuredDocumentData.from_dict(data)

                return data_type_0
            except:  # noqa: E722
                pass
            return cast(Union["StructuredDocumentData", None, Unset], data)

        data = _parse_data(d.pop("data", UNSET))

        task_document_update = cls(
            data=data,
        )

        task_document_update.additional_properties = d
        return task_document_update

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
