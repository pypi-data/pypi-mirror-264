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

from ..models.dataset_schema_column_error_type_0 import DatasetSchemaColumnErrorType0
from ..models.dataset_schema_column_type import DatasetSchemaColumnType

if TYPE_CHECKING:
    from ..models.dataset_schema import DatasetSchema
    from ..models.relationship import Relationship


T = TypeVar("T", bound="DatasetSchemaColumn")


@_attrs_define
class DatasetSchemaColumn:
    """
    Attributes:
        object_ (str):
        id (str):
        created_at (str):
        updated_at (str):
        dataset_schema (Union['DatasetSchema', 'Relationship']):
        name (str):
        type (DatasetSchemaColumnType):
        error (Union[DatasetSchemaColumnErrorType0, None]):
        dtype (Union[None, str]):
        is_autodetected_dtype (bool):
    """

    object_: str
    id: str
    created_at: str
    updated_at: str
    dataset_schema: Union["DatasetSchema", "Relationship"]
    name: str
    type: DatasetSchemaColumnType
    error: Union[DatasetSchemaColumnErrorType0, None]
    dtype: Union[None, str]
    is_autodetected_dtype: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.dataset_schema import DatasetSchema

        object_ = self.object_

        id = self.id

        created_at = self.created_at

        updated_at = self.updated_at

        dataset_schema: Dict[str, Any]
        if isinstance(self.dataset_schema, DatasetSchema):
            dataset_schema = self.dataset_schema.to_dict()
        else:
            dataset_schema = self.dataset_schema.to_dict()

        name = self.name

        type = self.type.value

        error: Union[None, str]
        if isinstance(self.error, DatasetSchemaColumnErrorType0):
            error = self.error.value
        else:
            error = self.error

        dtype: Union[None, str]
        dtype = self.dtype

        is_autodetected_dtype = self.is_autodetected_dtype

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "dataset_schema": dataset_schema,
                "name": name,
                "type": type,
                "error": error,
                "dtype": dtype,
                "is_autodetected_dtype": is_autodetected_dtype,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.dataset_schema import DatasetSchema
        from ..models.relationship import Relationship

        d = src_dict.copy()
        object_ = d.pop("object")

        id = d.pop("id")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        def _parse_dataset_schema(
            data: object,
        ) -> Union["DatasetSchema", "Relationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                dataset_schema_type_0 = DatasetSchema.from_dict(data)

                return dataset_schema_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            dataset_schema_type_1 = Relationship.from_dict(data)

            return dataset_schema_type_1

        dataset_schema = _parse_dataset_schema(d.pop("dataset_schema"))

        name = d.pop("name")

        type = DatasetSchemaColumnType(d.pop("type"))

        def _parse_error(data: object) -> Union[DatasetSchemaColumnErrorType0, None]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                error_type_0 = DatasetSchemaColumnErrorType0(data)

                return error_type_0
            except:  # noqa: E722
                pass
            return cast(Union[DatasetSchemaColumnErrorType0, None], data)

        error = _parse_error(d.pop("error"))

        def _parse_dtype(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        dtype = _parse_dtype(d.pop("dtype"))

        is_autodetected_dtype = d.pop("is_autodetected_dtype")

        dataset_schema_column = cls(
            object_=object_,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            dataset_schema=dataset_schema,
            name=name,
            type=type,
            error=error,
            dtype=dtype,
            is_autodetected_dtype=is_autodetected_dtype,
        )

        dataset_schema_column.additional_properties = d
        return dataset_schema_column

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
