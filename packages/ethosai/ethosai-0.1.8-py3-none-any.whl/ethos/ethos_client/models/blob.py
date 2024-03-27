from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.datasource import Datasource
    from ..models.relationship import Relationship
    from ..models.user import User


T = TypeVar("T", bound="Blob")


@_attrs_define
class Blob:
    """
    Attributes:
        object_ (str):
        id (str):
        created_at (str):
        updated_at (str):
        datasource (Union['Datasource', 'Relationship']):
        bucket_name (str):
        filename (str):
        datasource_filename (str):
        mimetype (str):
        state (str):
        state_reason (Union[None, str]):
        last_synced_at (Union[None, str]):
        hash_ (Union[None, str]):
        hash_type (Union[None, str]):
        size (Union[None, int]):
        created_by (Union['Relationship', 'User', None]):
        signed_upload_url (Union[None, Unset, str]):
        signed_download_url (Union[None, Unset, str]):
    """

    object_: str
    id: str
    created_at: str
    updated_at: str
    datasource: Union["Datasource", "Relationship"]
    bucket_name: str
    filename: str
    datasource_filename: str
    mimetype: str
    state: str
    state_reason: Union[None, str]
    last_synced_at: Union[None, str]
    hash_: Union[None, str]
    hash_type: Union[None, str]
    size: Union[None, int]
    created_by: Union["Relationship", "User", None]
    signed_upload_url: Union[None, Unset, str] = UNSET
    signed_download_url: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.datasource import Datasource
        from ..models.relationship import Relationship
        from ..models.user import User

        object_ = self.object_

        id = self.id

        created_at = self.created_at

        updated_at = self.updated_at

        datasource: Dict[str, Any]
        if isinstance(self.datasource, Datasource):
            datasource = self.datasource.to_dict()
        else:
            datasource = self.datasource.to_dict()

        bucket_name = self.bucket_name

        filename = self.filename

        datasource_filename = self.datasource_filename

        mimetype = self.mimetype

        state = self.state

        state_reason: Union[None, str]
        state_reason = self.state_reason

        last_synced_at: Union[None, str]
        last_synced_at = self.last_synced_at

        hash_: Union[None, str]
        hash_ = self.hash_

        hash_type: Union[None, str]
        hash_type = self.hash_type

        size: Union[None, int]
        size = self.size

        created_by: Union[Dict[str, Any], None]
        if isinstance(self.created_by, User):
            created_by = self.created_by.to_dict()
        elif isinstance(self.created_by, Relationship):
            created_by = self.created_by.to_dict()
        else:
            created_by = self.created_by

        signed_upload_url: Union[None, Unset, str]
        if isinstance(self.signed_upload_url, Unset):
            signed_upload_url = UNSET
        else:
            signed_upload_url = self.signed_upload_url

        signed_download_url: Union[None, Unset, str]
        if isinstance(self.signed_download_url, Unset):
            signed_download_url = UNSET
        else:
            signed_download_url = self.signed_download_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "datasource": datasource,
                "bucket_name": bucket_name,
                "filename": filename,
                "datasource_filename": datasource_filename,
                "mimetype": mimetype,
                "state": state,
                "state_reason": state_reason,
                "last_synced_at": last_synced_at,
                "hash": hash_,
                "hash_type": hash_type,
                "size": size,
                "created_by": created_by,
            }
        )
        if signed_upload_url is not UNSET:
            field_dict["signed_upload_url"] = signed_upload_url
        if signed_download_url is not UNSET:
            field_dict["signed_download_url"] = signed_download_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.datasource import Datasource
        from ..models.relationship import Relationship
        from ..models.user import User

        d = src_dict.copy()
        object_ = d.pop("object")

        id = d.pop("id")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        def _parse_datasource(data: object) -> Union["Datasource", "Relationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                datasource_type_0 = Datasource.from_dict(data)

                return datasource_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            datasource_type_1 = Relationship.from_dict(data)

            return datasource_type_1

        datasource = _parse_datasource(d.pop("datasource"))

        bucket_name = d.pop("bucket_name")

        filename = d.pop("filename")

        datasource_filename = d.pop("datasource_filename")

        mimetype = d.pop("mimetype")

        state = d.pop("state")

        def _parse_state_reason(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        state_reason = _parse_state_reason(d.pop("state_reason"))

        def _parse_last_synced_at(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        last_synced_at = _parse_last_synced_at(d.pop("last_synced_at"))

        def _parse_hash_(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        hash_ = _parse_hash_(d.pop("hash"))

        def _parse_hash_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        hash_type = _parse_hash_type(d.pop("hash_type"))

        def _parse_size(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        size = _parse_size(d.pop("size"))

        def _parse_created_by(data: object) -> Union["Relationship", "User", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                created_by_type_0 = User.from_dict(data)

                return created_by_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                created_by_type_1 = Relationship.from_dict(data)

                return created_by_type_1
            except:  # noqa: E722
                pass
            return cast(Union["Relationship", "User", None], data)

        created_by = _parse_created_by(d.pop("created_by"))

        def _parse_signed_upload_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        signed_upload_url = _parse_signed_upload_url(d.pop("signed_upload_url", UNSET))

        def _parse_signed_download_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        signed_download_url = _parse_signed_download_url(
            d.pop("signed_download_url", UNSET)
        )

        blob = cls(
            object_=object_,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            datasource=datasource,
            bucket_name=bucket_name,
            filename=filename,
            datasource_filename=datasource_filename,
            mimetype=mimetype,
            state=state,
            state_reason=state_reason,
            last_synced_at=last_synced_at,
            hash_=hash_,
            hash_type=hash_type,
            size=size,
            created_by=created_by,
            signed_upload_url=signed_upload_url,
            signed_download_url=signed_download_url,
        )

        blob.additional_properties = d
        return blob

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
