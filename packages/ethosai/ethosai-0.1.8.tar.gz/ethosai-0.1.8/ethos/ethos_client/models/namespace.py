from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.list_datasource import ListDatasource
    from ..models.list_document import ListDocument
    from ..models.list_governed_object import ListGovernedObject
    from ..models.list_governed_type import ListGovernedType
    from ..models.list_label import ListLabel
    from ..models.list_project import ListProject
    from ..models.list_relationship import ListRelationship
    from ..models.list_workflow_template import ListWorkflowTemplate
    from ..models.org import Org
    from ..models.relationship import Relationship


T = TypeVar("T", bound="Namespace")


@_attrs_define
class Namespace:
    """
    Attributes:
        object_ (str):
        id (str):
        created_at (str):
        updated_at (str):
        org (Union['Org', 'Relationship']):
        name (str):
        governed_types (Union['ListGovernedType', 'ListRelationship']):
        governed_objects (Union['ListGovernedObject', 'ListRelationship']):
        projects (Union['ListProject', 'ListRelationship']):
        workflow_templates (Union['ListRelationship', 'ListWorkflowTemplate']):
        documents (Union['ListDocument', 'ListRelationship']):
        datasources (Union['ListDatasource', 'ListRelationship']):
        labels (Union['ListLabel', 'ListRelationship']):
    """

    object_: str
    id: str
    created_at: str
    updated_at: str
    org: Union["Org", "Relationship"]
    name: str
    governed_types: Union["ListGovernedType", "ListRelationship"]
    governed_objects: Union["ListGovernedObject", "ListRelationship"]
    projects: Union["ListProject", "ListRelationship"]
    workflow_templates: Union["ListRelationship", "ListWorkflowTemplate"]
    documents: Union["ListDocument", "ListRelationship"]
    datasources: Union["ListDatasource", "ListRelationship"]
    labels: Union["ListLabel", "ListRelationship"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.list_datasource import ListDatasource
        from ..models.list_document import ListDocument
        from ..models.list_governed_object import ListGovernedObject
        from ..models.list_governed_type import ListGovernedType
        from ..models.list_label import ListLabel
        from ..models.list_project import ListProject
        from ..models.list_workflow_template import ListWorkflowTemplate
        from ..models.org import Org

        object_ = self.object_

        id = self.id

        created_at = self.created_at

        updated_at = self.updated_at

        org: Dict[str, Any]
        if isinstance(self.org, Org):
            org = self.org.to_dict()
        else:
            org = self.org.to_dict()

        name = self.name

        governed_types: Dict[str, Any]
        if isinstance(self.governed_types, ListGovernedType):
            governed_types = self.governed_types.to_dict()
        else:
            governed_types = self.governed_types.to_dict()

        governed_objects: Dict[str, Any]
        if isinstance(self.governed_objects, ListGovernedObject):
            governed_objects = self.governed_objects.to_dict()
        else:
            governed_objects = self.governed_objects.to_dict()

        projects: Dict[str, Any]
        if isinstance(self.projects, ListProject):
            projects = self.projects.to_dict()
        else:
            projects = self.projects.to_dict()

        workflow_templates: Dict[str, Any]
        if isinstance(self.workflow_templates, ListWorkflowTemplate):
            workflow_templates = self.workflow_templates.to_dict()
        else:
            workflow_templates = self.workflow_templates.to_dict()

        documents: Dict[str, Any]
        if isinstance(self.documents, ListDocument):
            documents = self.documents.to_dict()
        else:
            documents = self.documents.to_dict()

        datasources: Dict[str, Any]
        if isinstance(self.datasources, ListDatasource):
            datasources = self.datasources.to_dict()
        else:
            datasources = self.datasources.to_dict()

        labels: Dict[str, Any]
        if isinstance(self.labels, ListLabel):
            labels = self.labels.to_dict()
        else:
            labels = self.labels.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "org": org,
                "name": name,
                "governed_types": governed_types,
                "governed_objects": governed_objects,
                "projects": projects,
                "workflow_templates": workflow_templates,
                "documents": documents,
                "datasources": datasources,
                "labels": labels,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_datasource import ListDatasource
        from ..models.list_document import ListDocument
        from ..models.list_governed_object import ListGovernedObject
        from ..models.list_governed_type import ListGovernedType
        from ..models.list_label import ListLabel
        from ..models.list_project import ListProject
        from ..models.list_relationship import ListRelationship
        from ..models.list_workflow_template import ListWorkflowTemplate
        from ..models.org import Org
        from ..models.relationship import Relationship

        d = src_dict.copy()
        object_ = d.pop("object")

        id = d.pop("id")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        def _parse_org(data: object) -> Union["Org", "Relationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                org_type_0 = Org.from_dict(data)

                return org_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            org_type_1 = Relationship.from_dict(data)

            return org_type_1

        org = _parse_org(d.pop("org"))

        name = d.pop("name")

        def _parse_governed_types(
            data: object,
        ) -> Union["ListGovernedType", "ListRelationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                governed_types_type_0 = ListGovernedType.from_dict(data)

                return governed_types_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            governed_types_type_1 = ListRelationship.from_dict(data)

            return governed_types_type_1

        governed_types = _parse_governed_types(d.pop("governed_types"))

        def _parse_governed_objects(
            data: object,
        ) -> Union["ListGovernedObject", "ListRelationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                governed_objects_type_0 = ListGovernedObject.from_dict(data)

                return governed_objects_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            governed_objects_type_1 = ListRelationship.from_dict(data)

            return governed_objects_type_1

        governed_objects = _parse_governed_objects(d.pop("governed_objects"))

        def _parse_projects(data: object) -> Union["ListProject", "ListRelationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                projects_type_0 = ListProject.from_dict(data)

                return projects_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            projects_type_1 = ListRelationship.from_dict(data)

            return projects_type_1

        projects = _parse_projects(d.pop("projects"))

        def _parse_workflow_templates(
            data: object,
        ) -> Union["ListRelationship", "ListWorkflowTemplate"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                workflow_templates_type_0 = ListWorkflowTemplate.from_dict(data)

                return workflow_templates_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            workflow_templates_type_1 = ListRelationship.from_dict(data)

            return workflow_templates_type_1

        workflow_templates = _parse_workflow_templates(d.pop("workflow_templates"))

        def _parse_documents(data: object) -> Union["ListDocument", "ListRelationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                documents_type_0 = ListDocument.from_dict(data)

                return documents_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            documents_type_1 = ListRelationship.from_dict(data)

            return documents_type_1

        documents = _parse_documents(d.pop("documents"))

        def _parse_datasources(
            data: object,
        ) -> Union["ListDatasource", "ListRelationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                datasources_type_0 = ListDatasource.from_dict(data)

                return datasources_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            datasources_type_1 = ListRelationship.from_dict(data)

            return datasources_type_1

        datasources = _parse_datasources(d.pop("datasources"))

        def _parse_labels(data: object) -> Union["ListLabel", "ListRelationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                labels_type_0 = ListLabel.from_dict(data)

                return labels_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            labels_type_1 = ListRelationship.from_dict(data)

            return labels_type_1

        labels = _parse_labels(d.pop("labels"))

        namespace = cls(
            object_=object_,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            org=org,
            name=name,
            governed_types=governed_types,
            governed_objects=governed_objects,
            projects=projects,
            workflow_templates=workflow_templates,
            documents=documents,
            datasources=datasources,
            labels=labels,
        )

        namespace.additional_properties = d
        return namespace

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
