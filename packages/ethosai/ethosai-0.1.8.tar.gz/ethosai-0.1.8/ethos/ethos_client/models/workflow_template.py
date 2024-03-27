from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.namespace import Namespace
    from ..models.relationship import Relationship
    from ..models.user import User
    from ..models.workflow_template_data import WorkflowTemplateData


T = TypeVar("T", bound="WorkflowTemplate")


@_attrs_define
class WorkflowTemplate:
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
        name (str):
        namespace (Union['Namespace', 'Relationship']):
        yaml (str):
        data (WorkflowTemplateData):
    """

    object_: str
    id: str
    base_id: str
    version_number: int
    version_tags: List[str]
    version_tag: str
    version_updated_fields: List[str]
    version_updated_by: Union["Relationship", "User", None]
    name: str
    namespace: Union["Namespace", "Relationship"]
    yaml: str
    data: "WorkflowTemplateData"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
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

        name = self.name

        namespace: Dict[str, Any]
        if isinstance(self.namespace, Namespace):
            namespace = self.namespace.to_dict()
        else:
            namespace = self.namespace.to_dict()

        yaml = self.yaml

        data = self.data.to_dict()

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
                "name": name,
                "namespace": namespace,
                "yaml": yaml,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.namespace import Namespace
        from ..models.relationship import Relationship
        from ..models.user import User
        from ..models.workflow_template_data import WorkflowTemplateData

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

        name = d.pop("name")

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

        yaml = d.pop("yaml")

        data = WorkflowTemplateData.from_dict(d.pop("data"))

        workflow_template = cls(
            object_=object_,
            id=id,
            base_id=base_id,
            version_number=version_number,
            version_tags=version_tags,
            version_tag=version_tag,
            version_updated_fields=version_updated_fields,
            version_updated_by=version_updated_by,
            name=name,
            namespace=namespace,
            yaml=yaml,
            data=data,
        )

        workflow_template.additional_properties = d
        return workflow_template

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
