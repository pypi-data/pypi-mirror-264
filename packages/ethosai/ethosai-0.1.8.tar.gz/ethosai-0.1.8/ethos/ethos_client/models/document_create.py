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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.structured_document_data import StructuredDocumentData


T = TypeVar("T", bound="DocumentCreate")


@_attrs_define
class DocumentCreate:
    """
    Attributes:
        namespace_id (str):
        name (str):
        data (Union['StructuredDocumentData', None, Unset]):
        is_template (Union[Unset, bool]):  Default: False.
        is_template_section (Union[Unset, bool]):  Default: False.
    """

    namespace_id: str
    name: str
    data: Union["StructuredDocumentData", None, Unset] = UNSET
    is_template: Union[Unset, bool] = False
    is_template_section: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.structured_document_data import StructuredDocumentData

        namespace_id = self.namespace_id

        name = self.name

        data: Union[Dict[str, Any], None, Unset]
        if isinstance(self.data, Unset):
            data = UNSET
        elif isinstance(self.data, StructuredDocumentData):
            data = self.data.to_dict()
        else:
            data = self.data

        is_template = self.is_template

        is_template_section = self.is_template_section

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "namespace_id": namespace_id,
                "name": name,
            }
        )
        if data is not UNSET:
            field_dict["data"] = data
        if is_template is not UNSET:
            field_dict["is_template"] = is_template
        if is_template_section is not UNSET:
            field_dict["is_template_section"] = is_template_section

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.structured_document_data import StructuredDocumentData

        d = src_dict.copy()
        namespace_id = d.pop("namespace_id")

        name = d.pop("name")

        def _parse_data(data: object) -> Union["StructuredDocumentData", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_type_0 = StructuredDocumentData.from_dict(data)

                return data_type_0
            except:  # noqa: E722
                pass
            return cast(Union["StructuredDocumentData", None, Unset], data)

        data = _parse_data(d.pop("data", UNSET))

        is_template = d.pop("is_template", UNSET)

        is_template_section = d.pop("is_template_section", UNSET)

        document_create = cls(
            namespace_id=namespace_id,
            name=name,
            data=data,
            is_template=is_template,
            is_template_section=is_template_section,
        )

        document_create.additional_properties = d
        return document_create

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
