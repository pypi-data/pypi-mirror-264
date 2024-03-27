from http import HTTPStatus
from typing import Any, Dict, Literal, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.list_label import ListLabel
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    namespace_id: str,
    related_type: Union[Literal["governed_object"], None, Unset] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["namespace_id"] = namespace_id

    json_related_type: Union[Literal["governed_object"], None, Unset]
    if isinstance(related_type, Unset):
        json_related_type = UNSET
    else:
        json_related_type = related_type
    params["related_type"] = json_related_type

    json_expand: Union[None, Unset, str]
    if isinstance(expand, Unset):
        json_expand = UNSET
    else:
        json_expand = expand
    params["expand"] = json_expand

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/v1/labels",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ListLabel]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListLabel.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ListLabel]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    namespace_id: str,
    related_type: Union[Literal["governed_object"], None, Unset] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, ListLabel]]:
    """Get Labels

    Args:
        namespace_id (str):
        related_type (Union[Literal['governed_object'], None, Unset]):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ListLabel]]
    """

    kwargs = _get_kwargs(
        namespace_id=namespace_id,
        related_type=related_type,
        expand=expand,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    namespace_id: str,
    related_type: Union[Literal["governed_object"], None, Unset] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, ListLabel]]:
    """Get Labels

    Args:
        namespace_id (str):
        related_type (Union[Literal['governed_object'], None, Unset]):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ListLabel]
    """

    return sync_detailed(
        client=client,
        namespace_id=namespace_id,
        related_type=related_type,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    namespace_id: str,
    related_type: Union[Literal["governed_object"], None, Unset] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, ListLabel]]:
    """Get Labels

    Args:
        namespace_id (str):
        related_type (Union[Literal['governed_object'], None, Unset]):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ListLabel]]
    """

    kwargs = _get_kwargs(
        namespace_id=namespace_id,
        related_type=related_type,
        expand=expand,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    namespace_id: str,
    related_type: Union[Literal["governed_object"], None, Unset] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, ListLabel]]:
    """Get Labels

    Args:
        namespace_id (str):
        related_type (Union[Literal['governed_object'], None, Unset]):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ListLabel]
    """

    return (
        await asyncio_detailed(
            client=client,
            namespace_id=namespace_id,
            related_type=related_type,
            expand=expand,
        )
    ).parsed
