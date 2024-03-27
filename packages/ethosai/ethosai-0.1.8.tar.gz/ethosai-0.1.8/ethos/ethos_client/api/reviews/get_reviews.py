from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.list_review import ListReview
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    workflow_id: str,
    user_id: Union[None, Unset, str] = UNSET,
    state: Union[None, Unset, str] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["workflow_id"] = workflow_id

    json_user_id: Union[None, Unset, str]
    if isinstance(user_id, Unset):
        json_user_id = UNSET
    else:
        json_user_id = user_id
    params["user_id"] = json_user_id

    json_state: Union[None, Unset, str]
    if isinstance(state, Unset):
        json_state = UNSET
    else:
        json_state = state
    params["state"] = json_state

    json_expand: Union[None, Unset, str]
    if isinstance(expand, Unset):
        json_expand = UNSET
    else:
        json_expand = expand
    params["expand"] = json_expand

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/v1/reviews",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ListReview]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListReview.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ListReview]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    workflow_id: str,
    user_id: Union[None, Unset, str] = UNSET,
    state: Union[None, Unset, str] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, ListReview]]:
    """Get Reviews

    Args:
        workflow_id (str):
        user_id (Union[None, Unset, str]):
        state (Union[None, Unset, str]):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ListReview]]
    """

    kwargs = _get_kwargs(
        workflow_id=workflow_id,
        user_id=user_id,
        state=state,
        expand=expand,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    workflow_id: str,
    user_id: Union[None, Unset, str] = UNSET,
    state: Union[None, Unset, str] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, ListReview]]:
    """Get Reviews

    Args:
        workflow_id (str):
        user_id (Union[None, Unset, str]):
        state (Union[None, Unset, str]):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ListReview]
    """

    return sync_detailed(
        client=client,
        workflow_id=workflow_id,
        user_id=user_id,
        state=state,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    workflow_id: str,
    user_id: Union[None, Unset, str] = UNSET,
    state: Union[None, Unset, str] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, ListReview]]:
    """Get Reviews

    Args:
        workflow_id (str):
        user_id (Union[None, Unset, str]):
        state (Union[None, Unset, str]):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ListReview]]
    """

    kwargs = _get_kwargs(
        workflow_id=workflow_id,
        user_id=user_id,
        state=state,
        expand=expand,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    workflow_id: str,
    user_id: Union[None, Unset, str] = UNSET,
    state: Union[None, Unset, str] = UNSET,
    expand: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, ListReview]]:
    """Get Reviews

    Args:
        workflow_id (str):
        user_id (Union[None, Unset, str]):
        state (Union[None, Unset, str]):
        expand (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ListReview]
    """

    return (
        await asyncio_detailed(
            client=client,
            workflow_id=workflow_id,
            user_id=user_id,
            state=state,
            expand=expand,
        )
    ).parsed
