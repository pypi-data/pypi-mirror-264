from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.list_document import ListDocument
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    namespace_id: str,
    is_template: Union[None, Unset, bool] = UNSET,
    is_template_section: Union[None, Unset, bool] = UNSET,
    is_system_managed: Union[None, Unset, bool] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["namespace_id"] = namespace_id

    json_is_template: Union[None, Unset, bool]
    if isinstance(is_template, Unset):
        json_is_template = UNSET
    else:
        json_is_template = is_template
    params["is_template"] = json_is_template

    json_is_template_section: Union[None, Unset, bool]
    if isinstance(is_template_section, Unset):
        json_is_template_section = UNSET
    else:
        json_is_template_section = is_template_section
    params["is_template_section"] = json_is_template_section

    json_is_system_managed: Union[None, Unset, bool]
    if isinstance(is_system_managed, Unset):
        json_is_system_managed = UNSET
    else:
        json_is_system_managed = is_system_managed
    params["is_system_managed"] = json_is_system_managed

    json_expand: Union[None, Unset, str]
    if isinstance(expand, Unset):
        json_expand = UNSET
    else:
        json_expand = expand
    params["expand"] = json_expand

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/v1/documents",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ListDocument]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListDocument.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ListDocument]]:
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
    is_template: Union[None, Unset, bool] = UNSET,
    is_template_section: Union[None, Unset, bool] = UNSET,
    is_system_managed: Union[None, Unset, bool] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, ListDocument]]:
    """Get Documents

    Args:
        namespace_id (str):
        is_template (Union[None, Unset, bool]):
        is_template_section (Union[None, Unset, bool]):
        is_system_managed (Union[None, Unset, bool]):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ListDocument]]
    """

    kwargs = _get_kwargs(
        namespace_id=namespace_id,
        is_template=is_template,
        is_template_section=is_template_section,
        is_system_managed=is_system_managed,
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
    is_template: Union[None, Unset, bool] = UNSET,
    is_template_section: Union[None, Unset, bool] = UNSET,
    is_system_managed: Union[None, Unset, bool] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, ListDocument]]:
    """Get Documents

    Args:
        namespace_id (str):
        is_template (Union[None, Unset, bool]):
        is_template_section (Union[None, Unset, bool]):
        is_system_managed (Union[None, Unset, bool]):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ListDocument]
    """

    return sync_detailed(
        client=client,
        namespace_id=namespace_id,
        is_template=is_template,
        is_template_section=is_template_section,
        is_system_managed=is_system_managed,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    namespace_id: str,
    is_template: Union[None, Unset, bool] = UNSET,
    is_template_section: Union[None, Unset, bool] = UNSET,
    is_system_managed: Union[None, Unset, bool] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, ListDocument]]:
    """Get Documents

    Args:
        namespace_id (str):
        is_template (Union[None, Unset, bool]):
        is_template_section (Union[None, Unset, bool]):
        is_system_managed (Union[None, Unset, bool]):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ListDocument]]
    """

    kwargs = _get_kwargs(
        namespace_id=namespace_id,
        is_template=is_template,
        is_template_section=is_template_section,
        is_system_managed=is_system_managed,
        expand=expand,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    namespace_id: str,
    is_template: Union[None, Unset, bool] = UNSET,
    is_template_section: Union[None, Unset, bool] = UNSET,
    is_system_managed: Union[None, Unset, bool] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, ListDocument]]:
    """Get Documents

    Args:
        namespace_id (str):
        is_template (Union[None, Unset, bool]):
        is_template_section (Union[None, Unset, bool]):
        is_system_managed (Union[None, Unset, bool]):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ListDocument]
    """

    return (
        await asyncio_detailed(
            client=client,
            namespace_id=namespace_id,
            is_template=is_template,
            is_template_section=is_template_section,
            is_system_managed=is_system_managed,
            expand=expand,
        )
    ).parsed
