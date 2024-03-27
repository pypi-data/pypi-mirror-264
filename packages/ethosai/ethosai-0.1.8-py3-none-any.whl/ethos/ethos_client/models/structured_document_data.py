from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.structured_document_data_root import StructuredDocumentDataRoot


T = TypeVar("T", bound="StructuredDocumentData")


@_attrs_define
class StructuredDocumentData:
    """
    Attributes:
        root (StructuredDocumentDataRoot):
    """

    root: "StructuredDocumentDataRoot"

    def to_dict(self) -> Dict[str, Any]:
        root = self.root.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "root": root,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.structured_document_data_root import StructuredDocumentDataRoot

        d = src_dict.copy()
        root = StructuredDocumentDataRoot.from_dict(d.pop("root"))

        structured_document_data = cls(
            root=root,
        )

        return structured_document_data
