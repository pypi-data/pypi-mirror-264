from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.phase import Phase
from ...models.phase_update import PhaseUpdate
from ...types import UNSET, Response, Unset


def _get_kwargs(
    phase_id: str,
    *,
    body: PhaseUpdate,
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
        "url": "/v1/phases/{phase_id}".format(
            phase_id=phase_id,
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
) -> Optional[Union[HTTPValidationError, Phase]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Phase.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, Phase]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    phase_id: str,
    *,
    client: AuthenticatedClient,
    body: PhaseUpdate,
    expand: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, Phase]]:
    """Update Phase

    Args:
        phase_id (str):
        expand (Union[None, Unset, str]):
        body (PhaseUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Phase]]
    """

    kwargs = _get_kwargs(
        phase_id=phase_id,
        body=body,
        expand=expand,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    phase_id: str,
    *,
    client: AuthenticatedClient,
    body: PhaseUpdate,
    expand: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, Phase]]:
    """Update Phase

    Args:
        phase_id (str):
        expand (Union[None, Unset, str]):
        body (PhaseUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Phase]
    """

    return sync_detailed(
        phase_id=phase_id,
        client=client,
        body=body,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    phase_id: str,
    *,
    client: AuthenticatedClient,
    body: PhaseUpdate,
    expand: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, Phase]]:
    """Update Phase

    Args:
        phase_id (str):
        expand (Union[None, Unset, str]):
        body (PhaseUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Phase]]
    """

    kwargs = _get_kwargs(
        phase_id=phase_id,
        body=body,
        expand=expand,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    phase_id: str,
    *,
    client: AuthenticatedClient,
    body: PhaseUpdate,
    expand: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, Phase]]:
    """Update Phase

    Args:
        phase_id (str):
        expand (Union[None, Unset, str]):
        body (PhaseUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Phase]
    """

    return (
        await asyncio_detailed(
            phase_id=phase_id,
            client=client,
            body=body,
            expand=expand,
        )
    ).parsed
