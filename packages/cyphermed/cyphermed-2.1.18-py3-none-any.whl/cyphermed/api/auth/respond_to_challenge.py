from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.challenge import Challenge
from ...models.respond_to_challenge_form_params import RespondToChallengeFormParams
from ...models.token_info import TokenInfo
from ...types import Response


def _get_kwargs(
    form_data: RespondToChallengeFormParams,
) -> Dict[str, Any]:

    pass

    return {
        "method": "post",
        "url": "/v2/auth/challenge",
        "data": form_data.to_dict(),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Challenge, TokenInfo]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = TokenInfo.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.OK:
        response_200 = Challenge.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Challenge, TokenInfo]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    form_data: RespondToChallengeFormParams,
) -> Response[Union[Challenge, TokenInfo]]:
    """Respond To Challenge

     Answer a challenge to verify MFA device or token

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Challenge, TokenInfo]]
    """

    kwargs = _get_kwargs(
        form_data=form_data,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    form_data: RespondToChallengeFormParams,
) -> Optional[Union[Challenge, TokenInfo]]:
    """Respond To Challenge

     Answer a challenge to verify MFA device or token

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Challenge, TokenInfo]
    """

    return sync_detailed(
        client=client,
        form_data=form_data,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    form_data: RespondToChallengeFormParams,
) -> Response[Union[Challenge, TokenInfo]]:
    """Respond To Challenge

     Answer a challenge to verify MFA device or token

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Challenge, TokenInfo]]
    """

    kwargs = _get_kwargs(
        form_data=form_data,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    form_data: RespondToChallengeFormParams,
) -> Optional[Union[Challenge, TokenInfo]]:
    """Respond To Challenge

     Answer a challenge to verify MFA device or token

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Challenge, TokenInfo]
    """

    return (
        await asyncio_detailed(
            client=client,
            form_data=form_data,
        )
    ).parsed
