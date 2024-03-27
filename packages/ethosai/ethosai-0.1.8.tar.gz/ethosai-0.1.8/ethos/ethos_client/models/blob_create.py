from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BlobCreate")


@_attrs_define
class BlobCreate:
    """
    Attributes:
        datasource_id (str):
        filename (str):
        mimetype (str):
        bucket_name (Union[None, Unset, str]):
    """

    datasource_id: str
    filename: str
    mimetype: str
    bucket_name: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        datasource_id = self.datasource_id

        filename = self.filename

        mimetype = self.mimetype

        bucket_name: Union[None, Unset, str]
        if isinstance(self.bucket_name, Unset):
            bucket_name = UNSET
        else:
            bucket_name = self.bucket_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "datasource_id": datasource_id,
                "filename": filename,
                "mimetype": mimetype,
            }
        )
        if bucket_name is not UNSET:
            field_dict["bucket_name"] = bucket_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        datasource_id = d.pop("datasource_id")

        filename = d.pop("filename")

        mimetype = d.pop("mimetype")

        def _parse_bucket_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        bucket_name = _parse_bucket_name(d.pop("bucket_name", UNSET))

        blob_create = cls(
            datasource_id=datasource_id,
            filename=filename,
            mimetype=mimetype,
            bucket_name=bucket_name,
        )

        blob_create.additional_properties = d
        return blob_create

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
