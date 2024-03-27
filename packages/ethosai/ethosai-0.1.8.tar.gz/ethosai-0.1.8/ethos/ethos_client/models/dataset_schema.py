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

from ..models.dataset_schema_state import DatasetSchemaState
from ..models.dataset_schema_state_reason_type_0 import DatasetSchemaStateReasonType0

if TYPE_CHECKING:
    from ..models.list_dataset_schema_column import ListDatasetSchemaColumn
    from ..models.list_relationship import ListRelationship
    from ..models.relationship import Relationship
    from ..models.resource import Resource
    from ..models.user import User


T = TypeVar("T", bound="DatasetSchema")


@_attrs_define
class DatasetSchema:
    """
    Attributes:
        object_ (str):
        id (str):
        created_at (str):
        updated_at (str):
        resource (Union['Relationship', 'Resource']):
        state (DatasetSchemaState):
        state_reason (Union[DatasetSchemaStateReasonType0, None]):
        created_by (Union['Relationship', 'User', None]):
        columns (Union['ListDatasetSchemaColumn', 'ListRelationship']):
    """

    object_: str
    id: str
    created_at: str
    updated_at: str
    resource: Union["Relationship", "Resource"]
    state: DatasetSchemaState
    state_reason: Union[DatasetSchemaStateReasonType0, None]
    created_by: Union["Relationship", "User", None]
    columns: Union["ListDatasetSchemaColumn", "ListRelationship"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.list_dataset_schema_column import ListDatasetSchemaColumn
        from ..models.relationship import Relationship
        from ..models.resource import Resource
        from ..models.user import User

        object_ = self.object_

        id = self.id

        created_at = self.created_at

        updated_at = self.updated_at

        resource: Dict[str, Any]
        if isinstance(self.resource, Resource):
            resource = self.resource.to_dict()
        else:
            resource = self.resource.to_dict()

        state = self.state.value

        state_reason: Union[None, str]
        if isinstance(self.state_reason, DatasetSchemaStateReasonType0):
            state_reason = self.state_reason.value
        else:
            state_reason = self.state_reason

        created_by: Union[Dict[str, Any], None]
        if isinstance(self.created_by, User):
            created_by = self.created_by.to_dict()
        elif isinstance(self.created_by, Relationship):
            created_by = self.created_by.to_dict()
        else:
            created_by = self.created_by

        columns: Dict[str, Any]
        if isinstance(self.columns, ListDatasetSchemaColumn):
            columns = self.columns.to_dict()
        else:
            columns = self.columns.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "resource": resource,
                "state": state,
                "state_reason": state_reason,
                "created_by": created_by,
                "columns": columns,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_dataset_schema_column import ListDatasetSchemaColumn
        from ..models.list_relationship import ListRelationship
        from ..models.relationship import Relationship
        from ..models.resource import Resource
        from ..models.user import User

        d = src_dict.copy()
        object_ = d.pop("object")

        id = d.pop("id")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        def _parse_resource(data: object) -> Union["Relationship", "Resource"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                resource_type_0 = Resource.from_dict(data)

                return resource_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            resource_type_1 = Relationship.from_dict(data)

            return resource_type_1

        resource = _parse_resource(d.pop("resource"))

        state = DatasetSchemaState(d.pop("state"))

        def _parse_state_reason(
            data: object,
        ) -> Union[DatasetSchemaStateReasonType0, None]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                state_reason_type_0 = DatasetSchemaStateReasonType0(data)

                return state_reason_type_0
            except:  # noqa: E722
                pass
            return cast(Union[DatasetSchemaStateReasonType0, None], data)

        state_reason = _parse_state_reason(d.pop("state_reason"))

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

        def _parse_columns(
            data: object,
        ) -> Union["ListDatasetSchemaColumn", "ListRelationship"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                columns_type_0 = ListDatasetSchemaColumn.from_dict(data)

                return columns_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            columns_type_1 = ListRelationship.from_dict(data)

            return columns_type_1

        columns = _parse_columns(d.pop("columns"))

        dataset_schema = cls(
            object_=object_,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            resource=resource,
            state=state,
            state_reason=state_reason,
            created_by=created_by,
            columns=columns,
        )

        dataset_schema.additional_properties = d
        return dataset_schema

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
