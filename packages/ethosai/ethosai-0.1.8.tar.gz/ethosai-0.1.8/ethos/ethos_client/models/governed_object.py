from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.governed_object_object_classification import (
    GovernedObjectObjectClassification,
)

if TYPE_CHECKING:
    from ..models.folder import Folder
    from ..models.governed_object_data import GovernedObjectData
    from ..models.governed_object_metadata import GovernedObjectMetadata
    from ..models.governed_type import GovernedType
    from ..models.list_label_link import ListLabelLink
    from ..models.list_relationship import ListRelationship
    from ..models.namespace import Namespace
    from ..models.relationship import Relationship
    from ..models.user import User


T = TypeVar("T", bound="GovernedObject")


@_attrs_define
class GovernedObject:
    """
    Attributes:
        object_ (str):
        id (str):
        base_id (str): The base ID of this object without the version tag suffix.
        version_number (int):
        version_tags (List[str]):
        version_tag (str): The primary version tag for this version, such as v0, v1, etc.
        version_updated_fields (List[str]): A list of which fields were updated in this version from the previous
            version.
        version_updated_by (Union['Relationship', 'User', None]): The user who updated the versioned object to this
            version.
        namespace (Union['Namespace', 'Relationship']):
        label_links (Union['ListLabelLink', 'ListRelationship']):
        governed_type (Union['GovernedType', 'Relationship']):
        folder (Union['Folder', 'Relationship']):
        object_classification (GovernedObjectObjectClassification):
        data (GovernedObjectData):
        version_updated_data_fields (List[str]): A list of which data fields were updated in this Governed Object
            version from the previous version.
        version_metadata (Union['GovernedObjectMetadata', 'Relationship']): The latest metadata specific to this
            governed object version. Each governed object version will have its own individual version_metadata.
        base_metadata (Union['GovernedObjectMetadata', 'Relationship']): The latest base metadata, shared across all
            versions of this governed object.
    """

    object_: str
    id: str
    base_id: str
    version_number: int
    version_tags: List[str]
    version_tag: str
    version_updated_fields: List[str]
    version_updated_by: Union["Relationship", "User", None]
    namespace: Union["Namespace", "Relationship"]
    label_links: Union["ListLabelLink", "ListRelationship"]
    governed_type: Union["GovernedType", "Relationship"]
    folder: Union["Folder", "Relationship"]
    object_classification: GovernedObjectObjectClassification
    data: "GovernedObjectData"
    version_updated_data_fields: List[str]
    version_metadata: Union["GovernedObjectMetadata", "Relationship"]
    base_metadata: Union["GovernedObjectMetadata", "Relationship"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.folder import Folder
        from ..models.governed_object_metadata import GovernedObjectMetadata
        from ..models.governed_type import GovernedType
        from ..models.list_label_link import ListLabelLink
        from ..models.namespace import Namespace
        from ..models.relationship import Relationship
        from ..models.user import User

        object_ = self.object_

        id = self.id

        base_id = self.base_id

        version_number = self.version_number

        version_tags = self.version_tags

        version_tag = self.version_tag

        version_updated_fields = self.version_updated_fields

        version_updated_by: Union[Dict[str, Any], None]
        if isinstance(self.version_updated_by, User):
            version_updated_by = self.version_updated_by.to_dict()
        elif isinstance(self.version_updated_by, Relationship):
            version_updated_by = self.version_updated_by.to_dict()
        else:
            version_updated_by = self.version_updated_by

        namespace: Dict[str, Any]
        if isinstance(self.namespace, Namespace):
            namespace = self.namespace.to_dict()
        else:
            namespace = self.namespace.to_dict()

        label_links: Dict[str, Any]
        if isinstance(self.label_links, ListLabelLink):
            label_links = self.label_links.to_dict()
        else:
            label_links = self.label_links.to_dict()

        governed_type: Dict[str, Any]
        if isinstance(self.governed_type, GovernedType):
            governed_type = self.governed_type.to_dict()
        else:
            governed_type = self.governed_type.to_dict()

        folder: Dict[str, Any]
        if isinstance(self.folder, Folder):
            folder = self.folder.to_dict()
        else:
            folder = self.folder.to_dict()

        object_classification = self.object_classification.value

        data = self.data.to_dict()

        version_updated_data_fields = self.version_updated_data_fields

        version_metadata: Dict[str, Any]
        if isinstance(self.version_metadata, GovernedObjectMetadata):
            version_metadata = self.version_metadata.to_dict()
        else:
            version_metadata = self.version_metadata.to_dict()

        base_metadata: Dict[str, Any]
        if isinstance(self.base_metadata, GovernedObjectMetadata):
            base_metadata = self.base_metadata.to_dict()
        else:
            base_metadata = self.base_metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "id": id,
                "base_id": base_id,
                "version_number": version_number,
                "version_tags": version_tags,
                "version_tag": version_tag,
                "version_updated_fields": version_updated_fields,
                "version_updated_by": version_updated_by,
                "namespace": namespace,
                "label_links": label_links,
                "governed_type": governed_type,
                "folder": folder,
                "object_classification": object_classification,
                "data": data,
                "version_updated_data_fields": version_updated_data_fields,
                "version_metadata": version_metadata,
                "base_metadata": base_metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.folder import Folder
        from ..models.governed_object_data import GovernedObjectData
        from ..models.governed_object_metadata import GovernedObjectMetadata
        from ..models.governed_type import GovernedType
        from ..models.list_label_link import ListLabelLink
        from ..models.list_relationship import ListRelationship
        from ..models.namespace import Namespace
        from ..models.relationship import Relationship
        from ..models.user import User

        d = src_dict.copy()
        object_ = d.pop("object")

        id = d.pop("id")

        base_id = d.pop("base_id")

        version_number = d.pop("version_number")

        version_tags = cast(List[str], d.pop("version_tags"))

        version_tag = d.pop("version_tag")

        version_updated_fields = cast(List[str], d.pop("version_updated_fields"))

        def _parse_version_updated_by(
            data: object,
        ) -> Union["Relationship", "User", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                version_updated_by_type_0 = User.from_dict(data)

                return version_updated_by_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                version_updated_by_type_1 = Relationship.from_dict(data)

                return version_updated_by_type_1
            except:  # noqa: E722
                pass
            return cast(Union["Relationship", "User", None], data)

        version_updated_by = _parse_version_updated_by(d.pop("version_updated_by"))

        def _parse_namespace(data: object) -> Union["Namespace", "Relationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                namespace_type_0 = Namespace.from_dict(data)

                return namespace_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            namespace_type_1 = Relationship.from_dict(data)

            return namespace_type_1

        namespace = _parse_namespace(d.pop("namespace"))

        def _parse_label_links(
            data: object,
        ) -> Union["ListLabelLink", "ListRelationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                label_links_type_0 = ListLabelLink.from_dict(data)

                return label_links_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            label_links_type_1 = ListRelationship.from_dict(data)

            return label_links_type_1

        label_links = _parse_label_links(d.pop("label_links"))

        def _parse_governed_type(data: object) -> Union["GovernedType", "Relationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                governed_type_type_0 = GovernedType.from_dict(data)

                return governed_type_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            governed_type_type_1 = Relationship.from_dict(data)

            return governed_type_type_1

        governed_type = _parse_governed_type(d.pop("governed_type"))

        def _parse_folder(data: object) -> Union["Folder", "Relationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                folder_type_0 = Folder.from_dict(data)

                return folder_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            folder_type_1 = Relationship.from_dict(data)

            return folder_type_1

        folder = _parse_folder(d.pop("folder"))

        object_classification = GovernedObjectObjectClassification(
            d.pop("object_classification")
        )

        data = GovernedObjectData.from_dict(d.pop("data"))

        version_updated_data_fields = cast(
            List[str], d.pop("version_updated_data_fields")
        )

        def _parse_version_metadata(
            data: object,
        ) -> Union["GovernedObjectMetadata", "Relationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                version_metadata_type_0 = GovernedObjectMetadata.from_dict(data)

                return version_metadata_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            version_metadata_type_1 = Relationship.from_dict(data)

            return version_metadata_type_1

        version_metadata = _parse_version_metadata(d.pop("version_metadata"))

        def _parse_base_metadata(
            data: object,
        ) -> Union["GovernedObjectMetadata", "Relationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                base_metadata_type_0 = GovernedObjectMetadata.from_dict(data)

                return base_metadata_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            base_metadata_type_1 = Relationship.from_dict(data)

            return base_metadata_type_1

        base_metadata = _parse_base_metadata(d.pop("base_metadata"))

        governed_object = cls(
            object_=object_,
            id=id,
            base_id=base_id,
            version_number=version_number,
            version_tags=version_tags,
            version_tag=version_tag,
            version_updated_fields=version_updated_fields,
            version_updated_by=version_updated_by,
            namespace=namespace,
            label_links=label_links,
            governed_type=governed_type,
            folder=folder,
            object_classification=object_classification,
            data=data,
            version_updated_data_fields=version_updated_data_fields,
            version_metadata=version_metadata,
            base_metadata=base_metadata,
        )

        governed_object.additional_properties = d
        return governed_object

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
