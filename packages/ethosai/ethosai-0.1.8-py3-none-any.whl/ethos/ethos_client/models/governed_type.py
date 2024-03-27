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

from ..models.governed_type_object_classification import (
    GovernedTypeObjectClassification,
)

if TYPE_CHECKING:
    from ..models.list_governed_type_field import ListGovernedTypeField
    from ..models.list_relationship import ListRelationship
    from ..models.namespace import Namespace
    from ..models.relationship import Relationship


T = TypeVar("T", bound="GovernedType")


@_attrs_define
class GovernedType:
    """
    Attributes:
        object_ (str):
        id (str):
        created_at (str):
        updated_at (str):
        namespace (Union['Namespace', 'Relationship']):
        name (str):
        description (Union[None, str]):
        object_classification (GovernedTypeObjectClassification):
        object_fields (Union['ListGovernedTypeField', 'ListRelationship']):
        version_metadata_fields (Union['ListGovernedTypeField', 'ListRelationship']):
        base_metadata_fields (Union['ListGovernedTypeField', 'ListRelationship']):
    """

    object_: str
    id: str
    created_at: str
    updated_at: str
    namespace: Union["Namespace", "Relationship"]
    name: str
    description: Union[None, str]
    object_classification: GovernedTypeObjectClassification
    object_fields: Union["ListGovernedTypeField", "ListRelationship"]
    version_metadata_fields: Union["ListGovernedTypeField", "ListRelationship"]
    base_metadata_fields: Union["ListGovernedTypeField", "ListRelationship"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.list_governed_type_field import ListGovernedTypeField
        from ..models.namespace import Namespace

        object_ = self.object_

        id = self.id

        created_at = self.created_at

        updated_at = self.updated_at

        namespace: Dict[str, Any]
        if isinstance(self.namespace, Namespace):
            namespace = self.namespace.to_dict()
        else:
            namespace = self.namespace.to_dict()

        name = self.name

        description: Union[None, str]
        description = self.description

        object_classification = self.object_classification.value

        object_fields: Dict[str, Any]
        if isinstance(self.object_fields, ListGovernedTypeField):
            object_fields = self.object_fields.to_dict()
        else:
            object_fields = self.object_fields.to_dict()

        version_metadata_fields: Dict[str, Any]
        if isinstance(self.version_metadata_fields, ListGovernedTypeField):
            version_metadata_fields = self.version_metadata_fields.to_dict()
        else:
            version_metadata_fields = self.version_metadata_fields.to_dict()

        base_metadata_fields: Dict[str, Any]
        if isinstance(self.base_metadata_fields, ListGovernedTypeField):
            base_metadata_fields = self.base_metadata_fields.to_dict()
        else:
            base_metadata_fields = self.base_metadata_fields.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "namespace": namespace,
                "name": name,
                "description": description,
                "object_classification": object_classification,
                "object_fields": object_fields,
                "version_metadata_fields": version_metadata_fields,
                "base_metadata_fields": base_metadata_fields,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_governed_type_field import ListGovernedTypeField
        from ..models.list_relationship import ListRelationship
        from ..models.namespace import Namespace
        from ..models.relationship import Relationship

        d = src_dict.copy()
        object_ = d.pop("object")

        id = d.pop("id")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

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

        name = d.pop("name")

        def _parse_description(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        description = _parse_description(d.pop("description"))

        object_classification = GovernedTypeObjectClassification(
            d.pop("object_classification")
        )

        def _parse_object_fields(
            data: object,
        ) -> Union["ListGovernedTypeField", "ListRelationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                object_fields_type_0 = ListGovernedTypeField.from_dict(data)

                return object_fields_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            object_fields_type_1 = ListRelationship.from_dict(data)

            return object_fields_type_1

        object_fields = _parse_object_fields(d.pop("object_fields"))

        def _parse_version_metadata_fields(
            data: object,
        ) -> Union["ListGovernedTypeField", "ListRelationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                version_metadata_fields_type_0 = ListGovernedTypeField.from_dict(data)

                return version_metadata_fields_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            version_metadata_fields_type_1 = ListRelationship.from_dict(data)

            return version_metadata_fields_type_1

        version_metadata_fields = _parse_version_metadata_fields(
            d.pop("version_metadata_fields")
        )

        def _parse_base_metadata_fields(
            data: object,
        ) -> Union["ListGovernedTypeField", "ListRelationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                base_metadata_fields_type_0 = ListGovernedTypeField.from_dict(data)

                return base_metadata_fields_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            base_metadata_fields_type_1 = ListRelationship.from_dict(data)

            return base_metadata_fields_type_1

        base_metadata_fields = _parse_base_metadata_fields(
            d.pop("base_metadata_fields")
        )

        governed_type = cls(
            object_=object_,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            namespace=namespace,
            name=name,
            description=description,
            object_classification=object_classification,
            object_fields=object_fields,
            version_metadata_fields=version_metadata_fields,
            base_metadata_fields=base_metadata_fields,
        )

        governed_type.additional_properties = d
        return governed_type

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
