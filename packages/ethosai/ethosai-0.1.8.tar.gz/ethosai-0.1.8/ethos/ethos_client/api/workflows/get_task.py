from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.task import Task
from ...types import UNSET, Response, Unset


def _get_kwargs(
    task_id: str,
    *,
    expand: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_expand: Union[None, Unset, str]
    if isinstance(expand, Unset):
        json_expand = UNSET
    else:
        json_expand = expand
    params["expand"] = json_expand

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/v1/tasks/{task_id}".format(
            task_id=task_id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, Task]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Task.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, Task]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    task_id: str,
    *,
    client: AuthenticatedClient,
    expand: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, Task]]:
    """Get Task

    Args:
        task_id (str):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Task]]
    """

    kwargs = _get_kwargs(
        task_id=task_id,
        expand=expand,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    task_id: str,
    *,
    client: AuthenticatedClient,
    expand: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, Task]]:
    """Get Task

    Args:
        task_id (str):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Task]
    """

    return sync_detailed(
        task_id=task_id,
        client=client,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    task_id: str,
    *,
    client: AuthenticatedClient,
    expand: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, Task]]:
    """Get Task

    Args:
        task_id (str):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Task]]
    """

    kwargs = _get_kwargs(
        task_id=task_id,
        expand=expand,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    task_id: str,
    *,
    client: AuthenticatedClient,
    expand: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, Task]]:
    """Get Task

    Args:
        task_id (str):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Task]
    """

    return (
        await asyncio_detailed(
            task_id=task_id,
            client=client,
            expand=expand,
        )
    ).parsed
