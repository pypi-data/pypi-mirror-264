from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_tunnel_body import CreateTunnelBody
from ...models.new_tunnel_info import NewTunnelInfo
from ...types import Response


def _get_kwargs(
    device_id: str,
    *,
    json_body: CreateTunnelBody,
) -> Dict[str, Any]:

    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/v2/devices/{device_id}/tunnels".format(
            device_id=device_id,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[NewTunnelInfo]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = NewTunnelInfo.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[NewTunnelInfo]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    device_id: str,
    *,
    client: AuthenticatedClient,
    json_body: CreateTunnelBody,
) -> Response[NewTunnelInfo]:
    """Open Device Tunnel

     Create a new tunnel for a device

    Args:
        device_id (str):
        json_body (CreateTunnelBody): Create a new tunnel

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[NewTunnelInfo]
    """

    kwargs = _get_kwargs(
        device_id=device_id,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    device_id: str,
    *,
    client: AuthenticatedClient,
    json_body: CreateTunnelBody,
) -> Optional[NewTunnelInfo]:
    """Open Device Tunnel

     Create a new tunnel for a device

    Args:
        device_id (str):
        json_body (CreateTunnelBody): Create a new tunnel

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        NewTunnelInfo
    """

    return sync_detailed(
        device_id=device_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    device_id: str,
    *,
    client: AuthenticatedClient,
    json_body: CreateTunnelBody,
) -> Response[NewTunnelInfo]:
    """Open Device Tunnel

     Create a new tunnel for a device

    Args:
        device_id (str):
        json_body (CreateTunnelBody): Create a new tunnel

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[NewTunnelInfo]
    """

    kwargs = _get_kwargs(
        device_id=device_id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    device_id: str,
    *,
    client: AuthenticatedClient,
    json_body: CreateTunnelBody,
) -> Optional[NewTunnelInfo]:
    """Open Device Tunnel

     Create a new tunnel for a device

    Args:
        device_id (str):
        json_body (CreateTunnelBody): Create a new tunnel

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        NewTunnelInfo
    """

    return (
        await asyncio_detailed(
            device_id=device_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
