from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_resources_type_type_0 import GetResourcesTypeType0
from ...models.http_validation_error import HTTPValidationError
from ...models.list_resource import ListResource
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    related_id: str,
    type: Union[GetResourcesTypeType0, None, Unset] = UNSET,
    name: Union[None, Unset, str] = UNSET,
    version_tag: Union[None, Unset, str] = UNSET,
    tag: Union[None, Unset, str] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["related_id"] = related_id

    json_type: Union[None, Unset, str]
    if isinstance(type, Unset):
        json_type = UNSET
    elif isinstance(type, GetResourcesTypeType0):
        json_type = type.value
    else:
        json_type = type
    params["type"] = json_type

    json_name: Union[None, Unset, str]
    if isinstance(name, Unset):
        json_name = UNSET
    else:
        json_name = name
    params["name"] = json_name

    json_version_tag: Union[None, Unset, str]
    if isinstance(version_tag, Unset):
        json_version_tag = UNSET
    else:
        json_version_tag = version_tag
    params["version_tag"] = json_version_tag

    json_tag: Union[None, Unset, str]
    if isinstance(tag, Unset):
        json_tag = UNSET
    else:
        json_tag = tag
    params["tag"] = json_tag

    json_expand: Union[None, Unset, str]
    if isinstance(expand, Unset):
        json_expand = UNSET
    else:
        json_expand = expand
    params["expand"] = json_expand

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/v1/resources",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ListResource]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListResource.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ListResource]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    related_id: str,
    type: Union[GetResourcesTypeType0, None, Unset] = UNSET,
    name: Union[None, Unset, str] = UNSET,
    version_tag: Union[None, Unset, str] = UNSET,
    tag: Union[None, Unset, str] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, ListResource]]:
    """Get Resources

    Args:
        related_id (str):
        type (Union[GetResourcesTypeType0, None, Unset]):
        name (Union[None, Unset, str]):
        version_tag (Union[None, Unset, str]):
        tag (Union[None, Unset, str]):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ListResource]]
    """

    kwargs = _get_kwargs(
        related_id=related_id,
        type=type,
        name=name,
        version_tag=version_tag,
        tag=tag,
        expand=expand,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    related_id: str,
    type: Union[GetResourcesTypeType0, None, Unset] = UNSET,
    name: Union[None, Unset, str] = UNSET,
    version_tag: Union[None, Unset, str] = UNSET,
    tag: Union[None, Unset, str] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, ListResource]]:
    """Get Resources

    Args:
        related_id (str):
        type (Union[GetResourcesTypeType0, None, Unset]):
        name (Union[None, Unset, str]):
        version_tag (Union[None, Unset, str]):
        tag (Union[None, Unset, str]):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ListResource]
    """

    return sync_detailed(
        client=client,
        related_id=related_id,
        type=type,
        name=name,
        version_tag=version_tag,
        tag=tag,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    related_id: str,
    type: Union[GetResourcesTypeType0, None, Unset] = UNSET,
    name: Union[None, Unset, str] = UNSET,
    version_tag: Union[None, Unset, str] = UNSET,
    tag: Union[None, Unset, str] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, ListResource]]:
    """Get Resources

    Args:
        related_id (str):
        type (Union[GetResourcesTypeType0, None, Unset]):
        name (Union[None, Unset, str]):
        version_tag (Union[None, Unset, str]):
        tag (Union[None, Unset, str]):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ListResource]]
    """

    kwargs = _get_kwargs(
        related_id=related_id,
        type=type,
        name=name,
        version_tag=version_tag,
        tag=tag,
        expand=expand,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    related_id: str,
    type: Union[GetResourcesTypeType0, None, Unset] = UNSET,
    name: Union[None, Unset, str] = UNSET,
    version_tag: Union[None, Unset, str] = UNSET,
    tag: Union[None, Unset, str] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, ListResource]]:
    """Get Resources

    Args:
        related_id (str):
        type (Union[GetResourcesTypeType0, None, Unset]):
        name (Union[None, Unset, str]):
        version_tag (Union[None, Unset, str]):
        tag (Union[None, Unset, str]):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ListResource]
    """

    return (
        await asyncio_detailed(
            client=client,
            related_id=related_id,
            type=type,
            name=name,
            version_tag=version_tag,
            tag=tag,
            expand=expand,
        )
    ).parsed
