from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.document import Document
from ...models.http_validation_error import HTTPValidationError
from ...models.task_document_update import TaskDocumentUpdate
from ...types import UNSET, Response, Unset


def _get_kwargs(
    task_id: str,
    document_id: str,
    *,
    body: TaskDocumentUpdate,
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
        "url": "/v1/tasks/{task_id}/documents/{document_id}".format(
            task_id=task_id,
            document_id=document_id,
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
) -> Optional[Union[Document, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Document.from_dict(response.json())

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
) -> Response[Union[Document, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    task_id: str,
    document_id: str,
    *,
    client: AuthenticatedClient,
    body: TaskDocumentUpdate,
    expand: Union[None, Unset, str] = UNSET,
) -> Response[Union[Document, HTTPValidationError]]:
    """Update Task Document

    Args:
        task_id (str):
        document_id (str):
        expand (Union[None, Unset, str]):
        body (TaskDocumentUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Document, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        task_id=task_id,
        document_id=document_id,
        body=body,
        expand=expand,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    task_id: str,
    document_id: str,
    *,
    client: AuthenticatedClient,
    body: TaskDocumentUpdate,
    expand: Union[None, Unset, str] = UNSET,
) -> Optional[Union[Document, HTTPValidationError]]:
    """Update Task Document

    Args:
        task_id (str):
        document_id (str):
        expand (Union[None, Unset, str]):
        body (TaskDocumentUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Document, HTTPValidationError]
    """

    return sync_detailed(
        task_id=task_id,
        document_id=document_id,
        client=client,
        body=body,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    task_id: str,
    document_id: str,
    *,
    client: AuthenticatedClient,
    body: TaskDocumentUpdate,
    expand: Union[None, Unset, str] = UNSET,
) -> Response[Union[Document, HTTPValidationError]]:
    """Update Task Document

    Args:
        task_id (str):
        document_id (str):
        expand (Union[None, Unset, str]):
        body (TaskDocumentUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Document, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        task_id=task_id,
        document_id=document_id,
        body=body,
        expand=expand,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    task_id: str,
    document_id: str,
    *,
    client: AuthenticatedClient,
    body: TaskDocumentUpdate,
    expand: Union[None, Unset, str] = UNSET,
) -> Optional[Union[Document, HTTPValidationError]]:
    """Update Task Document

    Args:
        task_id (str):
        document_id (str):
        expand (Union[None, Unset, str]):
        body (TaskDocumentUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Document, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            task_id=task_id,
            document_id=document_id,
            client=client,
            body=body,
            expand=expand,
        )
    ).parsed
