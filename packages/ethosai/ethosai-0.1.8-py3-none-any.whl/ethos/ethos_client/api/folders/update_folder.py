from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.folder import Folder
from ...models.folder_update import FolderUpdate
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    folder_id: str,
    *,
    body: FolderUpdate,
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
        "url": "/v1/folders/{folder_id}".format(
            folder_id=folder_id,
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
) -> Optional[Union[Folder, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Folder.from_dict(response.json())

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
) -> Response[Union[Folder, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    folder_id: str,
    *,
    client: AuthenticatedClient,
    body: FolderUpdate,
    expand: Union[None, Unset, str] = UNSET,
) -> Response[Union[Folder, HTTPValidationError]]:
    """Update Folder

    Args:
        folder_id (str):
        expand (Union[None, Unset, str]):
        body (FolderUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Folder, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        folder_id=folder_id,
        body=body,
        expand=expand,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    folder_id: str,
    *,
    client: AuthenticatedClient,
    body: FolderUpdate,
    expand: Union[None, Unset, str] = UNSET,
) -> Optional[Union[Folder, HTTPValidationError]]:
    """Update Folder

    Args:
        folder_id (str):
        expand (Union[None, Unset, str]):
        body (FolderUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Folder, HTTPValidationError]
    """

    return sync_detailed(
        folder_id=folder_id,
        client=client,
        body=body,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    folder_id: str,
    *,
    client: AuthenticatedClient,
    body: FolderUpdate,
    expand: Union[None, Unset, str] = UNSET,
) -> Response[Union[Folder, HTTPValidationError]]:
    """Update Folder

    Args:
        folder_id (str):
        expand (Union[None, Unset, str]):
        body (FolderUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Folder, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        folder_id=folder_id,
        body=body,
        expand=expand,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    folder_id: str,
    *,
    client: AuthenticatedClient,
    body: FolderUpdate,
    expand: Union[None, Unset, str] = UNSET,
) -> Optional[Union[Folder, HTTPValidationError]]:
    """Update Folder

    Args:
        folder_id (str):
        expand (Union[None, Unset, str]):
        body (FolderUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Folder, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            folder_id=folder_id,
            client=client,
            body=body,
            expand=expand,
        )
    ).parsed
