from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.governed_type_field import GovernedTypeField
from ...models.governed_type_field_update import GovernedTypeFieldUpdate
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    governed_type_field_id: str,
    *,
    body: GovernedTypeFieldUpdate,
    expand: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    params: Dict[str, Any] = {}

    json_expand: Union[None, Unset, str]
    if isinstance(expand, Unset):
        json_expand = UNSET
    else:
        json_expand = expand
    params["expand"] = json_expand

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": "/v1/governed_type_fields/{governed_type_field_id}".format(
            governed_type_field_id=governed_type_field_id,
        ),
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GovernedTypeField, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GovernedTypeField.from_dict(response.json())

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
) -> Response[Union[GovernedTypeField, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    governed_type_field_id: str,
    *,
    client: AuthenticatedClient,
    body: GovernedTypeFieldUpdate,
    expand: Union[None, Unset, str] = UNSET,
) -> Response[Union[GovernedTypeField, HTTPValidationError]]:
    """Update Governed Type Field

    Args:
        governed_type_field_id (str):
        expand (Union[None, Unset, str]):
        body (GovernedTypeFieldUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GovernedTypeField, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        governed_type_field_id=governed_type_field_id,
        body=body,
        expand=expand,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    governed_type_field_id: str,
    *,
    client: AuthenticatedClient,
    body: GovernedTypeFieldUpdate,
    expand: Union[None, Unset, str] = UNSET,
) -> Optional[Union[GovernedTypeField, HTTPValidationError]]:
    """Update Governed Type Field

    Args:
        governed_type_field_id (str):
        expand (Union[None, Unset, str]):
        body (GovernedTypeFieldUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GovernedTypeField, HTTPValidationError]
    """

    return sync_detailed(
        governed_type_field_id=governed_type_field_id,
        client=client,
        body=body,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    governed_type_field_id: str,
    *,
    client: AuthenticatedClient,
    body: GovernedTypeFieldUpdate,
    expand: Union[None, Unset, str] = UNSET,
) -> Response[Union[GovernedTypeField, HTTPValidationError]]:
    """Update Governed Type Field

    Args:
        governed_type_field_id (str):
        expand (Union[None, Unset, str]):
        body (GovernedTypeFieldUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GovernedTypeField, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        governed_type_field_id=governed_type_field_id,
        body=body,
        expand=expand,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    governed_type_field_id: str,
    *,
    client: AuthenticatedClient,
    body: GovernedTypeFieldUpdate,
    expand: Union[None, Unset, str] = UNSET,
) -> Optional[Union[GovernedTypeField, HTTPValidationError]]:
    """Update Governed Type Field

    Args:
        governed_type_field_id (str):
        expand (Union[None, Unset, str]):
        body (GovernedTypeFieldUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GovernedTypeField, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            governed_type_field_id=governed_type_field_id,
            client=client,
            body=body,
            expand=expand,
        )
    ).parsed
