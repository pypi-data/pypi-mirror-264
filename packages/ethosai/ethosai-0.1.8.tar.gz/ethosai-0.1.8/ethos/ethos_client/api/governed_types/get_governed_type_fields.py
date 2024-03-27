from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_governed_type_fields_type_type_0 import (
    GetGovernedTypeFieldsTypeType0,
)
from ...models.http_validation_error import HTTPValidationError
from ...models.list_governed_type_field import ListGovernedTypeField
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    governed_type_id: str,
    type: Union[GetGovernedTypeFieldsTypeType0, None, Unset] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["governed_type_id"] = governed_type_id

    json_type: Union[None, Unset, str]
    if isinstance(type, Unset):
        json_type = UNSET
    elif isinstance(type, GetGovernedTypeFieldsTypeType0):
        json_type = type.value
    else:
        json_type = type
    params["type"] = json_type

    json_expand: Union[None, Unset, str]
    if isinstance(expand, Unset):
        json_expand = UNSET
    else:
        json_expand = expand
    params["expand"] = json_expand

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/v1/governed_type_fields",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ListGovernedTypeField]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListGovernedTypeField.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, ListGovernedTypeField]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    governed_type_id: str,
    type: Union[GetGovernedTypeFieldsTypeType0, None, Unset] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, ListGovernedTypeField]]:
    """Get Governed Type Fields

    Args:
        governed_type_id (str):
        type (Union[GetGovernedTypeFieldsTypeType0, None, Unset]):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ListGovernedTypeField]]
    """

    kwargs = _get_kwargs(
        governed_type_id=governed_type_id,
        type=type,
        expand=expand,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    governed_type_id: str,
    type: Union[GetGovernedTypeFieldsTypeType0, None, Unset] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, ListGovernedTypeField]]:
    """Get Governed Type Fields

    Args:
        governed_type_id (str):
        type (Union[GetGovernedTypeFieldsTypeType0, None, Unset]):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ListGovernedTypeField]
    """

    return sync_detailed(
        client=client,
        governed_type_id=governed_type_id,
        type=type,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    governed_type_id: str,
    type: Union[GetGovernedTypeFieldsTypeType0, None, Unset] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, ListGovernedTypeField]]:
    """Get Governed Type Fields

    Args:
        governed_type_id (str):
        type (Union[GetGovernedTypeFieldsTypeType0, None, Unset]):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ListGovernedTypeField]]
    """

    kwargs = _get_kwargs(
        governed_type_id=governed_type_id,
        type=type,
        expand=expand,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    governed_type_id: str,
    type: Union[GetGovernedTypeFieldsTypeType0, None, Unset] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, ListGovernedTypeField]]:
    """Get Governed Type Fields

    Args:
        governed_type_id (str):
        type (Union[GetGovernedTypeFieldsTypeType0, None, Unset]):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ListGovernedTypeField]
    """

    return (
        await asyncio_detailed(
            client=client,
            governed_type_id=governed_type_id,
            type=type,
            expand=expand,
        )
    ).parsed
