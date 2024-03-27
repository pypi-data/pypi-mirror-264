import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.resource_create_type import ResourceCreateType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dataset_schema_create import DatasetSchemaCreate
    from ..models.resource_blob_link_create import ResourceBlobLinkCreate
    from ..models.resource_create_meta_type_0 import ResourceCreateMetaType0


T = TypeVar("T", bound="ResourceCreate")


@_attrs_define
class ResourceCreate:
    """
    Attributes:
        name (str):
        type (ResourceCreateType):
        related_id (str):
        version_tags (Union[List[str], None, Unset]):
        tags (Union[List[str], None, Unset]):
        meta (Union['ResourceCreateMetaType0', None, Unset]):
        value (Union[List[float], List[str], None, Unset, bool, datetime.datetime, float, int, str]):
        resource_blob_links (Union[List['ResourceBlobLinkCreate'], None, Unset]):
        dataset_schema (Union['DatasetSchemaCreate', None, Unset]):
    """

    name: str
    type: ResourceCreateType
    related_id: str
    version_tags: Union[List[str], None, Unset] = UNSET
    tags: Union[List[str], None, Unset] = UNSET
    meta: Union["ResourceCreateMetaType0", None, Unset] = UNSET
    value: Union[
        List[float], List[str], None, Unset, bool, datetime.datetime, float, int, str
    ] = UNSET
    resource_blob_links: Union[List["ResourceBlobLinkCreate"], None, Unset] = UNSET
    dataset_schema: Union["DatasetSchemaCreate", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.dataset_schema_create import DatasetSchemaCreate
        from ..models.resource_create_meta_type_0 import ResourceCreateMetaType0

        name = self.name

        type = self.type.value

        related_id = self.related_id

        version_tags: Union[List[str], None, Unset]
        if isinstance(self.version_tags, Unset):
            version_tags = UNSET
        elif isinstance(self.version_tags, list):
            version_tags = self.version_tags

        else:
            version_tags = self.version_tags

        tags: Union[List[str], None, Unset]
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        meta: Union[Dict[str, Any], None, Unset]
        if isinstance(self.meta, Unset):
            meta = UNSET
        elif isinstance(self.meta, ResourceCreateMetaType0):
            meta = self.meta.to_dict()
        else:
            meta = self.meta

        value: Union[List[float], List[str], None, Unset, bool, float, int, str]
        if isinstance(self.value, Unset):
            value = UNSET
        elif isinstance(self.value, datetime.datetime):
            value = self.value.isoformat()
        elif isinstance(self.value, list):
            value = self.value

        elif isinstance(self.value, list):
            value = self.value

        else:
            value = self.value

        resource_blob_links: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.resource_blob_links, Unset):
            resource_blob_links = UNSET
        elif isinstance(self.resource_blob_links, list):
            resource_blob_links = []
            for resource_blob_links_type_0_item_data in self.resource_blob_links:
                resource_blob_links_type_0_item = (
                    resource_blob_links_type_0_item_data.to_dict()
                )
                resource_blob_links.append(resource_blob_links_type_0_item)

        else:
            resource_blob_links = self.resource_blob_links

        dataset_schema: Union[Dict[str, Any], None, Unset]
        if isinstance(self.dataset_schema, Unset):
            dataset_schema = UNSET
        elif isinstance(self.dataset_schema, DatasetSchemaCreate):
            dataset_schema = self.dataset_schema.to_dict()
        else:
            dataset_schema = self.dataset_schema

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "type": type,
                "related_id": related_id,
            }
        )
        if version_tags is not UNSET:
            field_dict["version_tags"] = version_tags
        if tags is not UNSET:
            field_dict["tags"] = tags
        if meta is not UNSET:
            field_dict["meta"] = meta
        if value is not UNSET:
            field_dict["value"] = value
        if resource_blob_links is not UNSET:
            field_dict["resource_blob_links"] = resource_blob_links
        if dataset_schema is not UNSET:
            field_dict["dataset_schema"] = dataset_schema

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.dataset_schema_create import DatasetSchemaCreate
        from ..models.resource_blob_link_create import ResourceBlobLinkCreate
        from ..models.resource_create_meta_type_0 import ResourceCreateMetaType0

        d = src_dict.copy()
        name = d.pop("name")

        type = ResourceCreateType(d.pop("type"))

        related_id = d.pop("related_id")

        def _parse_version_tags(data: object) -> Union[List[str], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                version_tags_type_0 = cast(List[str], data)

                return version_tags_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None, Unset], data)

        version_tags = _parse_version_tags(d.pop("version_tags", UNSET))

        def _parse_tags(data: object) -> Union[List[str], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(List[str], data)

                return tags_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None, Unset], data)

        tags = _parse_tags(d.pop("tags", UNSET))

        def _parse_meta(data: object) -> Union["ResourceCreateMetaType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                meta_type_0 = ResourceCreateMetaType0.from_dict(data)

                return meta_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ResourceCreateMetaType0", None, Unset], data)

        meta = _parse_meta(d.pop("meta", UNSET))

        def _parse_value(
            data: object,
        ) -> Union[
            List[float],
            List[str],
            None,
            Unset,
            bool,
            datetime.datetime,
            float,
            int,
            str,
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                value_type_4 = isoparse(data)

                return value_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_5 = cast(List[str], data)

                return value_type_5
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_6 = cast(List[float], data)

                return value_type_6
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    List[float],
                    List[str],
                    None,
                    Unset,
                    bool,
                    datetime.datetime,
                    float,
                    int,
                    str,
                ],
                data,
            )

        value = _parse_value(d.pop("value", UNSET))

        def _parse_resource_blob_links(
            data: object,
        ) -> Union[List["ResourceBlobLinkCreate"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                resource_blob_links_type_0 = []
                _resource_blob_links_type_0 = data
                for resource_blob_links_type_0_item_data in _resource_blob_links_type_0:
                    resource_blob_links_type_0_item = ResourceBlobLinkCreate.from_dict(
                        resource_blob_links_type_0_item_data
                    )

                    resource_blob_links_type_0.append(resource_blob_links_type_0_item)

                return resource_blob_links_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["ResourceBlobLinkCreate"], None, Unset], data)

        resource_blob_links = _parse_resource_blob_links(
            d.pop("resource_blob_links", UNSET)
        )

        def _parse_dataset_schema(
            data: object,
        ) -> Union["DatasetSchemaCreate", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                dataset_schema_type_0 = DatasetSchemaCreate.from_dict(data)

                return dataset_schema_type_0
            except:  # noqa: E722
                pass
            return cast(Union["DatasetSchemaCreate", None, Unset], data)

        dataset_schema = _parse_dataset_schema(d.pop("dataset_schema", UNSET))

        resource_create = cls(
            name=name,
            type=type,
            related_id=related_id,
            version_tags=version_tags,
            tags=tags,
            meta=meta,
            value=value,
            resource_blob_links=resource_blob_links,
            dataset_schema=dataset_schema,
        )

        resource_create.additional_properties = d
        return resource_create

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
