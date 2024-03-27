from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.list_relationship import ListRelationship
    from ..models.list_workflow import ListWorkflow
    from ..models.namespace import Namespace
    from ..models.relationship import Relationship


T = TypeVar("T", bound="Project")


@_attrs_define
class Project:
    """
    Attributes:
        object_ (str):
        id (str):
        created_at (str):
        updated_at (str):
        namespace (Union['Namespace', 'Relationship']):
        name (str):
        workflows (Union['ListRelationship', 'ListWorkflow']):
    """

    object_: str
    id: str
    created_at: str
    updated_at: str
    namespace: Union["Namespace", "Relationship"]
    name: str
    workflows: Union["ListRelationship", "ListWorkflow"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.list_workflow import ListWorkflow
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

        workflows: Dict[str, Any]
        if isinstance(self.workflows, ListWorkflow):
            workflows = self.workflows.to_dict()
        else:
            workflows = self.workflows.to_dict()

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
                "workflows": workflows,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_relationship import ListRelationship
        from ..models.list_workflow import ListWorkflow
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

        def _parse_workflows(data: object) -> Union["ListRelationship", "ListWorkflow"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                workflows_type_0 = ListWorkflow.from_dict(data)

                return workflows_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            workflows_type_1 = ListRelationship.from_dict(data)

            return workflows_type_1

        workflows = _parse_workflows(d.pop("workflows"))

        project = cls(
            object_=object_,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            namespace=namespace,
            name=name,
            workflows=workflows,
        )

        project.additional_properties = d
        return project

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
