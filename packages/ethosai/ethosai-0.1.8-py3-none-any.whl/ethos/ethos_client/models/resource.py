import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.resource_type import ResourceType

if TYPE_CHECKING:
    from ..models.dataset_schema import DatasetSchema
    from ..models.governed_object import GovernedObject
    from ..models.list_relationship import ListRelationship
    from ..models.list_resource_blob_link import ListResourceBlobLink
    from ..models.namespace import Namespace
    from ..models.project import Project
    from ..models.relationship import Relationship
    from ..models.resource_meta import ResourceMeta
    from ..models.task import Task
    from ..models.user import User


T = TypeVar("T", bound="Resource")


@_attrs_define
class Resource:
    """
    Attributes:
        object_ (str):
        id (str):
        created_at (str):
        updated_at (str):
        name (str):
        type (ResourceType):
        version_tags (List[str]):
        tags (List[str]):
        meta (ResourceMeta):
        related (Union['GovernedObject', 'Namespace', 'Project', 'Relationship', 'Task']):
        created_by (Union['Relationship', 'User', None]):
        value (Union[List[float], List[str], None, bool, datetime.datetime, float, int, str]):
        resource_blob_links (Union['ListRelationship', 'ListResourceBlobLink']):
        dataset_schema (Union['DatasetSchema', 'Relationship', None]):
    """

    object_: str
    id: str
    created_at: str
    updated_at: str
    name: str
    type: ResourceType
    version_tags: List[str]
    tags: List[str]
    meta: "ResourceMeta"
    related: Union["GovernedObject", "Namespace", "Project", "Relationship", "Task"]
    created_by: Union["Relationship", "User", None]
    value: Union[List[float], List[str], None, bool, datetime.datetime, float, int, str]
    resource_blob_links: Union["ListRelationship", "ListResourceBlobLink"]
    dataset_schema: Union["DatasetSchema", "Relationship", None]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.dataset_schema import DatasetSchema
        from ..models.governed_object import GovernedObject
        from ..models.list_resource_blob_link import ListResourceBlobLink
        from ..models.namespace import Namespace
        from ..models.project import Project
        from ..models.relationship import Relationship
        from ..models.task import Task
        from ..models.user import User

        object_ = self.object_

        id = self.id

        created_at = self.created_at

        updated_at = self.updated_at

        name = self.name

        type = self.type.value

        version_tags = self.version_tags

        tags = self.tags

        meta = self.meta.to_dict()

        related: Dict[str, Any]
        if isinstance(self.related, Namespace):
            related = self.related.to_dict()
        elif isinstance(self.related, Project):
            related = self.related.to_dict()
        elif isinstance(self.related, Task):
            related = self.related.to_dict()
        elif isinstance(self.related, GovernedObject):
            related = self.related.to_dict()
        else:
            related = self.related.to_dict()

        created_by: Union[Dict[str, Any], None]
        if isinstance(self.created_by, User):
            created_by = self.created_by.to_dict()
        elif isinstance(self.created_by, Relationship):
            created_by = self.created_by.to_dict()
        else:
            created_by = self.created_by

        value: Union[List[float], List[str], None, bool, float, int, str]
        if isinstance(self.value, datetime.datetime):
            value = self.value.isoformat()
        elif isinstance(self.value, list):
            value = self.value

        elif isinstance(self.value, list):
            value = self.value

        else:
            value = self.value

        resource_blob_links: Dict[str, Any]
        if isinstance(self.resource_blob_links, ListResourceBlobLink):
            resource_blob_links = self.resource_blob_links.to_dict()
        else:
            resource_blob_links = self.resource_blob_links.to_dict()

        dataset_schema: Union[Dict[str, Any], None]
        if isinstance(self.dataset_schema, DatasetSchema):
            dataset_schema = self.dataset_schema.to_dict()
        elif isinstance(self.dataset_schema, Relationship):
            dataset_schema = self.dataset_schema.to_dict()
        else:
            dataset_schema = self.dataset_schema

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "name": name,
                "type": type,
                "version_tags": version_tags,
                "tags": tags,
                "meta": meta,
                "related": related,
                "created_by": created_by,
                "value": value,
                "resource_blob_links": resource_blob_links,
                "dataset_schema": dataset_schema,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.dataset_schema import DatasetSchema
        from ..models.governed_object import GovernedObject
        from ..models.list_relationship import ListRelationship
        from ..models.list_resource_blob_link import ListResourceBlobLink
        from ..models.namespace import Namespace
        from ..models.project import Project
        from ..models.relationship import Relationship
        from ..models.resource_meta import ResourceMeta
        from ..models.task import Task
        from ..models.user import User

        d = src_dict.copy()
        object_ = d.pop("object")

        id = d.pop("id")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        name = d.pop("name")

        type = ResourceType(d.pop("type"))

        version_tags = cast(List[str], d.pop("version_tags"))

        tags = cast(List[str], d.pop("tags"))

        meta = ResourceMeta.from_dict(d.pop("meta"))

        def _parse_related(
            data: object,
        ) -> Union["GovernedObject", "Namespace", "Project", "Relationship", "Task"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                related_type_0 = Namespace.from_dict(data)

                return related_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                related_type_1 = Project.from_dict(data)

                return related_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                related_type_2 = Task.from_dict(data)

                return related_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                related_type_3 = GovernedObject.from_dict(data)

                return related_type_3
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            related_type_4 = Relationship.from_dict(data)

            return related_type_4

        related = _parse_related(d.pop("related"))

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

        def _parse_value(
            data: object,
        ) -> Union[
            List[float], List[str], None, bool, datetime.datetime, float, int, str
        ]:
            if data is None:
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
                    bool,
                    datetime.datetime,
                    float,
                    int,
                    str,
                ],
                data,
            )

        value = _parse_value(d.pop("value"))

        def _parse_resource_blob_links(
            data: object,
        ) -> Union["ListRelationship", "ListResourceBlobLink"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                resource_blob_links_type_0 = ListResourceBlobLink.from_dict(data)

                return resource_blob_links_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            resource_blob_links_type_1 = ListRelationship.from_dict(data)

            return resource_blob_links_type_1

        resource_blob_links = _parse_resource_blob_links(d.pop("resource_blob_links"))

        def _parse_dataset_schema(
            data: object,
        ) -> Union["DatasetSchema", "Relationship", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                dataset_schema_type_0 = DatasetSchema.from_dict(data)

                return dataset_schema_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                dataset_schema_type_1 = Relationship.from_dict(data)

                return dataset_schema_type_1
            except:  # noqa: E722
                pass
            return cast(Union["DatasetSchema", "Relationship", None], data)

        dataset_schema = _parse_dataset_schema(d.pop("dataset_schema"))

        resource = cls(
            object_=object_,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            name=name,
            type=type,
            version_tags=version_tags,
            tags=tags,
            meta=meta,
            related=related,
            created_by=created_by,
            value=value,
            resource_blob_links=resource_blob_links,
            dataset_schema=dataset_schema,
        )

        resource.additional_properties = d
        return resource

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
