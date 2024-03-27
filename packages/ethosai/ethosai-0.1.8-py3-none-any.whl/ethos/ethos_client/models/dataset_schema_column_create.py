from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.dataset_schema_column_create_type import DatasetSchemaColumnCreateType
from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetSchemaColumnCreate")


@_attrs_define
class DatasetSchemaColumnCreate:
    """
    Attributes:
        name (str):
        type (Union[Unset, DatasetSchemaColumnCreateType]):  Default: DatasetSchemaColumnCreateType.DEFAULT.
        dtype (Union[None, Unset, str]):
    """

    name: str
    type: Union[Unset, DatasetSchemaColumnCreateType] = (
        DatasetSchemaColumnCreateType.DEFAULT
    )
    dtype: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        dtype: Union[None, Unset, str]
        if isinstance(self.dtype, Unset):
            dtype = UNSET
        else:
            dtype = self.dtype

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if type is not UNSET:
            field_dict["type"] = type
        if dtype is not UNSET:
            field_dict["dtype"] = dtype

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        _type = d.pop("type", UNSET)
        type: Union[Unset, DatasetSchemaColumnCreateType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = DatasetSchemaColumnCreateType(_type)

        def _parse_dtype(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        dtype = _parse_dtype(d.pop("dtype", UNSET))

        dataset_schema_column_create = cls(
            name=name,
            type=type,
            dtype=dtype,
        )

        dataset_schema_column_create.additional_properties = d
        return dataset_schema_column_create

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
