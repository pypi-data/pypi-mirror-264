from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_email_template_body import CreateEmailTemplateBody
from ...models.new_email_template_info import NewEmailTemplateInfo
from ...types import Response


def _get_kwargs(
    *,
    json_body: CreateEmailTemplateBody,
) -> Dict[str, Any]:

    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/v2/email/templates",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[NewEmailTemplateInfo]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = NewEmailTemplateInfo.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[NewEmailTemplateInfo]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: CreateEmailTemplateBody,
) -> Response[NewEmailTemplateInfo]:
    """Create Email Template

     Create a new email template

    Args:
        json_body (CreateEmailTemplateBody): Which Template fields to include in request bodies

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[NewEmailTemplateInfo]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: CreateEmailTemplateBody,
) -> Optional[NewEmailTemplateInfo]:
    """Create Email Template

     Create a new email template

    Args:
        json_body (CreateEmailTemplateBody): Which Template fields to include in request bodies

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        NewEmailTemplateInfo
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: CreateEmailTemplateBody,
) -> Response[NewEmailTemplateInfo]:
    """Create Email Template

     Create a new email template

    Args:
        json_body (CreateEmailTemplateBody): Which Template fields to include in request bodies

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[NewEmailTemplateInfo]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: CreateEmailTemplateBody,
) -> Optional[NewEmailTemplateInfo]:
    """Create Email Template

     Create a new email template

    Args:
        json_body (CreateEmailTemplateBody): Which Template fields to include in request bodies

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        NewEmailTemplateInfo
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
