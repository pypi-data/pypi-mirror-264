from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.namespace import Namespace
    from ..models.relationship import Relationship
    from ..models.structured_document_data import StructuredDocumentData
    from ..models.task import Task
    from ..models.user import User


T = TypeVar("T", bound="Document")


@_attrs_define
class Document:
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
        name (str):
        data (StructuredDocumentData):
        is_template (bool):
        is_template_section (bool):
        is_system_managed (bool):
        from_template (Union['Document', 'Relationship', None]):
        task (Union['Relationship', 'Task', None]):
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
    name: str
    data: "StructuredDocumentData"
    is_template: bool
    is_template_section: bool
    is_system_managed: bool
    from_template: Union["Document", "Relationship", None]
    task: Union["Relationship", "Task", None]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.namespace import Namespace
        from ..models.relationship import Relationship
        from ..models.task import Task
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

        name = self.name

        data = self.data.to_dict()

        is_template = self.is_template

        is_template_section = self.is_template_section

        is_system_managed = self.is_system_managed

        from_template: Union[Dict[str, Any], None]
        if isinstance(self.from_template, Document):
            from_template = self.from_template.to_dict()
        elif isinstance(self.from_template, Relationship):
            from_template = self.from_template.to_dict()
        else:
            from_template = self.from_template

        task: Union[Dict[str, Any], None]
        if isinstance(self.task, Task):
            task = self.task.to_dict()
        elif isinstance(self.task, Relationship):
            task = self.task.to_dict()
        else:
            task = self.task

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
                "name": name,
                "data": data,
                "is_template": is_template,
                "is_template_section": is_template_section,
                "is_system_managed": is_system_managed,
                "from_template": from_template,
                "task": task,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.namespace import Namespace
        from ..models.relationship import Relationship
        from ..models.structured_document_data import StructuredDocumentData
        from ..models.task import Task
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

        name = d.pop("name")

        data = StructuredDocumentData.from_dict(d.pop("data"))

        is_template = d.pop("is_template")

        is_template_section = d.pop("is_template_section")

        is_system_managed = d.pop("is_system_managed")

        def _parse_from_template(
            data: object,
        ) -> Union["Document", "Relationship", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                from_template_type_0 = Document.from_dict(data)

                return from_template_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                from_template_type_1 = Relationship.from_dict(data)

                return from_template_type_1
            except:  # noqa: E722
                pass
            return cast(Union["Document", "Relationship", None], data)

        from_template = _parse_from_template(d.pop("from_template"))

        def _parse_task(data: object) -> Union["Relationship", "Task", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                task_type_0 = Task.from_dict(data)

                return task_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                task_type_1 = Relationship.from_dict(data)

                return task_type_1
            except:  # noqa: E722
                pass
            return cast(Union["Relationship", "Task", None], data)

        task = _parse_task(d.pop("task"))

        document = cls(
            object_=object_,
            id=id,
            base_id=base_id,
            version_number=version_number,
            version_tags=version_tags,
            version_tag=version_tag,
            version_updated_fields=version_updated_fields,
            version_updated_by=version_updated_by,
            namespace=namespace,
            name=name,
            data=data,
            is_template=is_template,
            is_template_section=is_template_section,
            is_system_managed=is_system_managed,
            from_template=from_template,
            task=task,
        )

        document.additional_properties = d
        return document

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
