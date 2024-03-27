from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.list_workflow import ListWorkflow
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    project_id: str,
    name: Union[None, Unset, str] = UNSET,
    workflow_template_id: Union[None, Unset, str] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["project_id"] = project_id

    json_name: Union[None, Unset, str]
    if isinstance(name, Unset):
        json_name = UNSET
    else:
        json_name = name
    params["name"] = json_name

    json_workflow_template_id: Union[None, Unset, str]
    if isinstance(workflow_template_id, Unset):
        json_workflow_template_id = UNSET
    else:
        json_workflow_template_id = workflow_template_id
    params["workflow_template_id"] = json_workflow_template_id

    json_expand: Union[None, Unset, str]
    if isinstance(expand, Unset):
        json_expand = UNSET
    else:
        json_expand = expand
    params["expand"] = json_expand

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/v1/workflows",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ListWorkflow]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListWorkflow.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ListWorkflow]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    project_id: str,
    name: Union[None, Unset, str] = UNSET,
    workflow_template_id: Union[None, Unset, str] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, ListWorkflow]]:
    """Get Workflows

    Args:
        project_id (str):
        name (Union[None, Unset, str]):
        workflow_template_id (Union[None, Unset, str]):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ListWorkflow]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        name=name,
        workflow_template_id=workflow_template_id,
        expand=expand,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    project_id: str,
    name: Union[None, Unset, str] = UNSET,
    workflow_template_id: Union[None, Unset, str] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, ListWorkflow]]:
    """Get Workflows

    Args:
        project_id (str):
        name (Union[None, Unset, str]):
        workflow_template_id (Union[None, Unset, str]):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ListWorkflow]
    """

    return sync_detailed(
        client=client,
        project_id=project_id,
        name=name,
        workflow_template_id=workflow_template_id,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id: str,
    name: Union[None, Unset, str] = UNSET,
    workflow_template_id: Union[None, Unset, str] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, ListWorkflow]]:
    """Get Workflows

    Args:
        project_id (str):
        name (Union[None, Unset, str]):
        workflow_template_id (Union[None, Unset, str]):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ListWorkflow]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        name=name,
        workflow_template_id=workflow_template_id,
        expand=expand,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    project_id: str,
    name: Union[None, Unset, str] = UNSET,
    workflow_template_id: Union[None, Unset, str] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, ListWorkflow]]:
    """Get Workflows

    Args:
        project_id (str):
        name (Union[None, Unset, str]):
        workflow_template_id (Union[None, Unset, str]):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ListWorkflow]
    """

    return (
        await asyncio_detailed(
            client=client,
            project_id=project_id,
            name=name,
            workflow_template_id=workflow_template_id,
            expand=expand,
        )
    ).parsed
