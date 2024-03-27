from typing import (
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

from ..models.proxy_inference_prediction_method_type_0 import (
    ProxyInferencePredictionMethodType0,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProxyInference")


@_attrs_define
class ProxyInference:
    """
    Attributes:
        id (str):
        white (Union[None, float]):
        black (Union[None, float]):
        api (Union[None, float]):
        native (Union[None, float]):
        multiple (Union[None, float]):
        hispanic (Union[None, float]):
        predicted_race (Union[None, str]):
        prediction_method (Union[None, ProxyInferencePredictionMethodType0]):
        object_ (Union[Unset, str]):  Default: 'proxy_inference'.
    """

    id: str
    white: Union[None, float]
    black: Union[None, float]
    api: Union[None, float]
    native: Union[None, float]
    multiple: Union[None, float]
    hispanic: Union[None, float]
    predicted_race: Union[None, str]
    prediction_method: Union[None, ProxyInferencePredictionMethodType0]
    object_: Union[Unset, str] = "proxy_inference"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        white: Union[None, float]
        white = self.white

        black: Union[None, float]
        black = self.black

        api: Union[None, float]
        api = self.api

        native: Union[None, float]
        native = self.native

        multiple: Union[None, float]
        multiple = self.multiple

        hispanic: Union[None, float]
        hispanic = self.hispanic

        predicted_race: Union[None, str]
        predicted_race = self.predicted_race

        prediction_method: Union[None, str]
        if isinstance(self.prediction_method, ProxyInferencePredictionMethodType0):
            prediction_method = self.prediction_method.value
        else:
            prediction_method = self.prediction_method

        object_ = self.object_

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "white": white,
                "black": black,
                "api": api,
                "native": native,
                "multiple": multiple,
                "hispanic": hispanic,
                "predicted_race": predicted_race,
                "prediction_method": prediction_method,
            }
        )
        if object_ is not UNSET:
            field_dict["object"] = object_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        def _parse_white(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        white = _parse_white(d.pop("white"))

        def _parse_black(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        black = _parse_black(d.pop("black"))

        def _parse_api(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        api = _parse_api(d.pop("api"))

        def _parse_native(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        native = _parse_native(d.pop("native"))

        def _parse_multiple(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        multiple = _parse_multiple(d.pop("multiple"))

        def _parse_hispanic(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        hispanic = _parse_hispanic(d.pop("hispanic"))

        def _parse_predicted_race(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        predicted_race = _parse_predicted_race(d.pop("predicted_race"))

        def _parse_prediction_method(
            data: object,
        ) -> Union[None, ProxyInferencePredictionMethodType0]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                prediction_method_type_0 = ProxyInferencePredictionMethodType0(data)

                return prediction_method_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, ProxyInferencePredictionMethodType0], data)

        prediction_method = _parse_prediction_method(d.pop("prediction_method"))

        object_ = d.pop("object", UNSET)

        proxy_inference = cls(
            id=id,
            white=white,
            black=black,
            api=api,
            native=native,
            multiple=multiple,
            hispanic=hispanic,
            predicted_race=predicted_race,
            prediction_method=prediction_method,
            object_=object_,
        )

        proxy_inference.additional_properties = d
        return proxy_inference

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
