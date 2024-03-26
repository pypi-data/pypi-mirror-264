import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_user_list import AdminUserList
from ...models.anon_user_list import AnonUserList
from ...models.user_list import UserList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    is_active: Union[Unset, None, bool] = UNSET,
    is_delete_protected: Union[Unset, None, bool] = UNSET,
    created_by: Union[Unset, None, str] = UNSET,
    last_updated_by: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    search_fields: Union[Unset, None, str] = UNSET,
    page_count: Union[None, Unset, bool, str] = False,
    object_count: Union[None, Unset, bool, str] = False,
    limit: Union[Unset, None, int] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    order_by: Union[Unset, None, str] = UNSET,
    desc: Union[None, Unset, bool, str] = False,
    bust_cache: Union[None, Unset, bool, str] = False,
    created_date: Union[Unset, None, datetime.datetime] = UNSET,
    created_date_gte: Union[Unset, None, datetime.datetime] = UNSET,
    created_date_lte: Union[Unset, None, datetime.datetime] = UNSET,
    last_updated_date: Union[Unset, None, datetime.datetime] = UNSET,
    last_updated_date_gte: Union[Unset, None, datetime.datetime] = UNSET,
    last_updated_date_lte: Union[Unset, None, datetime.datetime] = UNSET,
    tags: Union[Unset, None, str] = UNSET,
    tags_contains: Union[Unset, None, str] = UNSET,
    tags_contains_any: Union[Unset, None, str] = UNSET,
    is_org_admin: Union[Unset, None, bool] = UNSET,
    is_project_admin: Union[Unset, None, bool] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    group_id: Union[Unset, None, str] = UNSET,
    role_id: Union[Unset, None, str] = UNSET,
    locale: Union[Unset, None, str] = UNSET,
    locale_regex: Union[Unset, None, str] = UNSET,
    zoneinfo: Union[Unset, None, str] = UNSET,
    zoneinfo_regex: Union[Unset, None, str] = UNSET,
    last_seen: Union[Unset, None, datetime.datetime] = UNSET,
    last_seen_gte: Union[Unset, None, datetime.datetime] = UNSET,
    last_seen_lte: Union[Unset, None, datetime.datetime] = UNSET,
    mfa_enabled: Union[Unset, None, bool] = UNSET,
    sms_mfa_enabled: Union[Unset, None, bool] = UNSET,
    software_mfa_enabled: Union[Unset, None, bool] = UNSET,
    email: Union[Unset, None, str] = UNSET,
    email_regex: Union[Unset, None, str] = UNSET,
    phone_number: Union[Unset, None, str] = UNSET,
    phone_number_regex: Union[Unset, None, str] = UNSET,
    nickname: Union[Unset, None, str] = UNSET,
    nickname_regex: Union[Unset, None, str] = UNSET,
    username: Union[Unset, None, str] = UNSET,
    username_regex: Union[Unset, None, str] = UNSET,
    first_name: Union[Unset, None, str] = UNSET,
    first_name_regex: Union[Unset, None, str] = UNSET,
    middle_name: Union[Unset, None, str] = UNSET,
    middle_name_regex: Union[Unset, None, str] = UNSET,
    last_name: Union[Unset, None, str] = UNSET,
    last_name_regex: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:

    pass

    params: Dict[str, Any] = {}
    params["is_active"] = is_active

    params["is_delete_protected"] = is_delete_protected

    params["created_by"] = created_by

    params["last_updated_by"] = last_updated_by

    params["search"] = search

    params["search_fields"] = search_fields

    json_page_count: Union[None, Unset, bool, str]
    if isinstance(page_count, Unset):
        json_page_count = UNSET
    elif page_count is None:
        json_page_count = None

    else:
        json_page_count = page_count

    params["page_count"] = json_page_count

    json_object_count: Union[None, Unset, bool, str]
    if isinstance(object_count, Unset):
        json_object_count = UNSET
    elif object_count is None:
        json_object_count = None

    else:
        json_object_count = object_count

    params["object_count"] = json_object_count

    params["limit"] = limit

    params["page"] = page

    params["order_by"] = order_by

    json_desc: Union[None, Unset, bool, str]
    if isinstance(desc, Unset):
        json_desc = UNSET
    elif desc is None:
        json_desc = None

    else:
        json_desc = desc

    params["desc"] = json_desc

    json_bust_cache: Union[None, Unset, bool, str]
    if isinstance(bust_cache, Unset):
        json_bust_cache = UNSET
    elif bust_cache is None:
        json_bust_cache = None

    else:
        json_bust_cache = bust_cache

    params["bust_cache"] = json_bust_cache

    json_created_date: Union[Unset, None, str] = UNSET
    if not isinstance(created_date, Unset):
        json_created_date = created_date.isoformat() if created_date else None

    params["created_date"] = json_created_date

    json_created_date_gte: Union[Unset, None, str] = UNSET
    if not isinstance(created_date_gte, Unset):
        json_created_date_gte = created_date_gte.isoformat() if created_date_gte else None

    params["created_date.gte"] = json_created_date_gte

    json_created_date_lte: Union[Unset, None, str] = UNSET
    if not isinstance(created_date_lte, Unset):
        json_created_date_lte = created_date_lte.isoformat() if created_date_lte else None

    params["created_date.lte"] = json_created_date_lte

    json_last_updated_date: Union[Unset, None, str] = UNSET
    if not isinstance(last_updated_date, Unset):
        json_last_updated_date = last_updated_date.isoformat() if last_updated_date else None

    params["last_updated_date"] = json_last_updated_date

    json_last_updated_date_gte: Union[Unset, None, str] = UNSET
    if not isinstance(last_updated_date_gte, Unset):
        json_last_updated_date_gte = (
            last_updated_date_gte.isoformat() if last_updated_date_gte else None
        )

    params["last_updated_date.gte"] = json_last_updated_date_gte

    json_last_updated_date_lte: Union[Unset, None, str] = UNSET
    if not isinstance(last_updated_date_lte, Unset):
        json_last_updated_date_lte = (
            last_updated_date_lte.isoformat() if last_updated_date_lte else None
        )

    params["last_updated_date.lte"] = json_last_updated_date_lte

    params["tags"] = tags

    params["tags.contains"] = tags_contains

    params["tags.contains_any"] = tags_contains_any

    params["is_org_admin"] = is_org_admin

    params["is_project_admin"] = is_project_admin

    params["project_id"] = project_id

    params["group_id"] = group_id

    params["role_id"] = role_id

    params["locale"] = locale

    params["locale.regex"] = locale_regex

    params["zoneinfo"] = zoneinfo

    params["zoneinfo.regex"] = zoneinfo_regex

    json_last_seen: Union[Unset, None, str] = UNSET
    if not isinstance(last_seen, Unset):
        json_last_seen = last_seen.isoformat() if last_seen else None

    params["last_seen"] = json_last_seen

    json_last_seen_gte: Union[Unset, None, str] = UNSET
    if not isinstance(last_seen_gte, Unset):
        json_last_seen_gte = last_seen_gte.isoformat() if last_seen_gte else None

    params["last_seen.gte"] = json_last_seen_gte

    json_last_seen_lte: Union[Unset, None, str] = UNSET
    if not isinstance(last_seen_lte, Unset):
        json_last_seen_lte = last_seen_lte.isoformat() if last_seen_lte else None

    params["last_seen.lte"] = json_last_seen_lte

    params["mfa_enabled"] = mfa_enabled

    params["sms_mfa_enabled"] = sms_mfa_enabled

    params["software_mfa_enabled"] = software_mfa_enabled

    params["email"] = email

    params["email.regex"] = email_regex

    params["phone_number"] = phone_number

    params["phone_number.regex"] = phone_number_regex

    params["nickname"] = nickname

    params["nickname.regex"] = nickname_regex

    params["username"] = username

    params["username.regex"] = username_regex

    params["first_name"] = first_name

    params["first_name.regex"] = first_name_regex

    params["middle_name"] = middle_name

    params["middle_name.regex"] = middle_name_regex

    params["last_name"] = last_name

    params["last_name.regex"] = last_name_regex

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/v2/users",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union["AdminUserList", "AnonUserList", "UserList"]]:
    if response.status_code == HTTPStatus.OK:

        def _parse_response_200(data: object) -> Union["AdminUserList", "AnonUserList", "UserList"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = AdminUserList.from_dict(data)

                return response_200_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_1 = UserList.from_dict(data)

                return response_200_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_2 = AnonUserList.from_dict(data)

            return response_200_type_2

        response_200 = _parse_response_200(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union["AdminUserList", "AnonUserList", "UserList"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    is_active: Union[Unset, None, bool] = UNSET,
    is_delete_protected: Union[Unset, None, bool] = UNSET,
    created_by: Union[Unset, None, str] = UNSET,
    last_updated_by: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    search_fields: Union[Unset, None, str] = UNSET,
    page_count: Union[None, Unset, bool, str] = False,
    object_count: Union[None, Unset, bool, str] = False,
    limit: Union[Unset, None, int] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    order_by: Union[Unset, None, str] = UNSET,
    desc: Union[None, Unset, bool, str] = False,
    bust_cache: Union[None, Unset, bool, str] = False,
    created_date: Union[Unset, None, datetime.datetime] = UNSET,
    created_date_gte: Union[Unset, None, datetime.datetime] = UNSET,
    created_date_lte: Union[Unset, None, datetime.datetime] = UNSET,
    last_updated_date: Union[Unset, None, datetime.datetime] = UNSET,
    last_updated_date_gte: Union[Unset, None, datetime.datetime] = UNSET,
    last_updated_date_lte: Union[Unset, None, datetime.datetime] = UNSET,
    tags: Union[Unset, None, str] = UNSET,
    tags_contains: Union[Unset, None, str] = UNSET,
    tags_contains_any: Union[Unset, None, str] = UNSET,
    is_org_admin: Union[Unset, None, bool] = UNSET,
    is_project_admin: Union[Unset, None, bool] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    group_id: Union[Unset, None, str] = UNSET,
    role_id: Union[Unset, None, str] = UNSET,
    locale: Union[Unset, None, str] = UNSET,
    locale_regex: Union[Unset, None, str] = UNSET,
    zoneinfo: Union[Unset, None, str] = UNSET,
    zoneinfo_regex: Union[Unset, None, str] = UNSET,
    last_seen: Union[Unset, None, datetime.datetime] = UNSET,
    last_seen_gte: Union[Unset, None, datetime.datetime] = UNSET,
    last_seen_lte: Union[Unset, None, datetime.datetime] = UNSET,
    mfa_enabled: Union[Unset, None, bool] = UNSET,
    sms_mfa_enabled: Union[Unset, None, bool] = UNSET,
    software_mfa_enabled: Union[Unset, None, bool] = UNSET,
    email: Union[Unset, None, str] = UNSET,
    email_regex: Union[Unset, None, str] = UNSET,
    phone_number: Union[Unset, None, str] = UNSET,
    phone_number_regex: Union[Unset, None, str] = UNSET,
    nickname: Union[Unset, None, str] = UNSET,
    nickname_regex: Union[Unset, None, str] = UNSET,
    username: Union[Unset, None, str] = UNSET,
    username_regex: Union[Unset, None, str] = UNSET,
    first_name: Union[Unset, None, str] = UNSET,
    first_name_regex: Union[Unset, None, str] = UNSET,
    middle_name: Union[Unset, None, str] = UNSET,
    middle_name_regex: Union[Unset, None, str] = UNSET,
    last_name: Union[Unset, None, str] = UNSET,
    last_name_regex: Union[Unset, None, str] = UNSET,
) -> Response[Union["AdminUserList", "AnonUserList", "UserList"]]:
    """Get Users

     Get a list of all users

    Args:
        is_active (Union[Unset, None, bool]):  (Admin only) Whether to only return active devices
        is_delete_protected (Union[Unset, None, bool]): Whether to only return delete-protected
            devices
        created_by (Union[Unset, None, str]): ID of the user who created the device
        last_updated_by (Union[Unset, None, str]): ID of the user who last updated the device
        search (Union[Unset, None, str]): Search term to filter devices by
        search_fields (Union[Unset, None, str]): Comma-delimited list of fields to search in
        page_count (Union[None, Unset, bool, str]): Whether to only return the number of pages
        object_count (Union[None, Unset, bool, str]): Whether to only return the number of
            matching entries
        limit (Union[Unset, None, int]): Maximum number of objects to return
        page (Union[Unset, None, int]): Page number to return
        order_by (Union[Unset, None, str]): Field to order results by
        desc (Union[None, Unset, bool, str]): Whether to order results in descending order
        bust_cache (Union[None, Unset, bool, str]): Whether to bypass the cache and get the latest
            data
        created_date (Union[Unset, None, datetime.datetime]): Created date of items to return
        created_date_gte (Union[Unset, None, datetime.datetime]):
        created_date_lte (Union[Unset, None, datetime.datetime]):
        last_updated_date (Union[Unset, None, datetime.datetime]): Last edited date of items to
            return
        last_updated_date_gte (Union[Unset, None, datetime.datetime]):
        last_updated_date_lte (Union[Unset, None, datetime.datetime]):
        tags (Union[Unset, None, str]): Comma delimited list of tags on this device
        tags_contains (Union[Unset, None, str]):
        tags_contains_any (Union[Unset, None, str]):
        is_org_admin (Union[Unset, None, bool]): Whether to only return org admins
        is_project_admin (Union[Unset, None, bool]): Whether to only return project admins
        project_id (Union[Unset, None, str]): ID of the project to filter accounts by
        group_id (Union[Unset, None, str]): ID of the group to filter accounts by
        role_id (Union[Unset, None, str]): ID of the role to filter accounts by
        locale (Union[Unset, None, str]): Locale of the device
        locale_regex (Union[Unset, None, str]):
        zoneinfo (Union[Unset, None, str]): Timezone of the device
        zoneinfo_regex (Union[Unset, None, str]):
        last_seen (Union[Unset, None, datetime.datetime]): Last time the device was seen
        last_seen_gte (Union[Unset, None, datetime.datetime]):
        last_seen_lte (Union[Unset, None, datetime.datetime]):
        mfa_enabled (Union[Unset, None, bool]): Whether to only return users with MFA enabled
        sms_mfa_enabled (Union[Unset, None, bool]): Whether to only return users with SMS MFA
            enabled
        software_mfa_enabled (Union[Unset, None, bool]): Whether to only return users with
            software MFA enabled
        email (Union[Unset, None, str]): Email of the user
        email_regex (Union[Unset, None, str]):
        phone_number (Union[Unset, None, str]): Phone number of the user
        phone_number_regex (Union[Unset, None, str]):
        nickname (Union[Unset, None, str]): Nickname of the user
        nickname_regex (Union[Unset, None, str]):
        username (Union[Unset, None, str]): Username of the user
        username_regex (Union[Unset, None, str]):
        first_name (Union[Unset, None, str]): First (or given) name of the user
        first_name_regex (Union[Unset, None, str]):
        middle_name (Union[Unset, None, str]): Middle name of the user
        middle_name_regex (Union[Unset, None, str]):
        last_name (Union[Unset, None, str]): Last (or family) name of the user
        last_name_regex (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union['AdminUserList', 'AnonUserList', 'UserList']]
    """

    kwargs = _get_kwargs(
        is_active=is_active,
        is_delete_protected=is_delete_protected,
        created_by=created_by,
        last_updated_by=last_updated_by,
        search=search,
        search_fields=search_fields,
        page_count=page_count,
        object_count=object_count,
        limit=limit,
        page=page,
        order_by=order_by,
        desc=desc,
        bust_cache=bust_cache,
        created_date=created_date,
        created_date_gte=created_date_gte,
        created_date_lte=created_date_lte,
        last_updated_date=last_updated_date,
        last_updated_date_gte=last_updated_date_gte,
        last_updated_date_lte=last_updated_date_lte,
        tags=tags,
        tags_contains=tags_contains,
        tags_contains_any=tags_contains_any,
        is_org_admin=is_org_admin,
        is_project_admin=is_project_admin,
        project_id=project_id,
        group_id=group_id,
        role_id=role_id,
        locale=locale,
        locale_regex=locale_regex,
        zoneinfo=zoneinfo,
        zoneinfo_regex=zoneinfo_regex,
        last_seen=last_seen,
        last_seen_gte=last_seen_gte,
        last_seen_lte=last_seen_lte,
        mfa_enabled=mfa_enabled,
        sms_mfa_enabled=sms_mfa_enabled,
        software_mfa_enabled=software_mfa_enabled,
        email=email,
        email_regex=email_regex,
        phone_number=phone_number,
        phone_number_regex=phone_number_regex,
        nickname=nickname,
        nickname_regex=nickname_regex,
        username=username,
        username_regex=username_regex,
        first_name=first_name,
        first_name_regex=first_name_regex,
        middle_name=middle_name,
        middle_name_regex=middle_name_regex,
        last_name=last_name,
        last_name_regex=last_name_regex,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    is_active: Union[Unset, None, bool] = UNSET,
    is_delete_protected: Union[Unset, None, bool] = UNSET,
    created_by: Union[Unset, None, str] = UNSET,
    last_updated_by: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    search_fields: Union[Unset, None, str] = UNSET,
    page_count: Union[None, Unset, bool, str] = False,
    object_count: Union[None, Unset, bool, str] = False,
    limit: Union[Unset, None, int] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    order_by: Union[Unset, None, str] = UNSET,
    desc: Union[None, Unset, bool, str] = False,
    bust_cache: Union[None, Unset, bool, str] = False,
    created_date: Union[Unset, None, datetime.datetime] = UNSET,
    created_date_gte: Union[Unset, None, datetime.datetime] = UNSET,
    created_date_lte: Union[Unset, None, datetime.datetime] = UNSET,
    last_updated_date: Union[Unset, None, datetime.datetime] = UNSET,
    last_updated_date_gte: Union[Unset, None, datetime.datetime] = UNSET,
    last_updated_date_lte: Union[Unset, None, datetime.datetime] = UNSET,
    tags: Union[Unset, None, str] = UNSET,
    tags_contains: Union[Unset, None, str] = UNSET,
    tags_contains_any: Union[Unset, None, str] = UNSET,
    is_org_admin: Union[Unset, None, bool] = UNSET,
    is_project_admin: Union[Unset, None, bool] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    group_id: Union[Unset, None, str] = UNSET,
    role_id: Union[Unset, None, str] = UNSET,
    locale: Union[Unset, None, str] = UNSET,
    locale_regex: Union[Unset, None, str] = UNSET,
    zoneinfo: Union[Unset, None, str] = UNSET,
    zoneinfo_regex: Union[Unset, None, str] = UNSET,
    last_seen: Union[Unset, None, datetime.datetime] = UNSET,
    last_seen_gte: Union[Unset, None, datetime.datetime] = UNSET,
    last_seen_lte: Union[Unset, None, datetime.datetime] = UNSET,
    mfa_enabled: Union[Unset, None, bool] = UNSET,
    sms_mfa_enabled: Union[Unset, None, bool] = UNSET,
    software_mfa_enabled: Union[Unset, None, bool] = UNSET,
    email: Union[Unset, None, str] = UNSET,
    email_regex: Union[Unset, None, str] = UNSET,
    phone_number: Union[Unset, None, str] = UNSET,
    phone_number_regex: Union[Unset, None, str] = UNSET,
    nickname: Union[Unset, None, str] = UNSET,
    nickname_regex: Union[Unset, None, str] = UNSET,
    username: Union[Unset, None, str] = UNSET,
    username_regex: Union[Unset, None, str] = UNSET,
    first_name: Union[Unset, None, str] = UNSET,
    first_name_regex: Union[Unset, None, str] = UNSET,
    middle_name: Union[Unset, None, str] = UNSET,
    middle_name_regex: Union[Unset, None, str] = UNSET,
    last_name: Union[Unset, None, str] = UNSET,
    last_name_regex: Union[Unset, None, str] = UNSET,
) -> Optional[Union["AdminUserList", "AnonUserList", "UserList"]]:
    """Get Users

     Get a list of all users

    Args:
        is_active (Union[Unset, None, bool]):  (Admin only) Whether to only return active devices
        is_delete_protected (Union[Unset, None, bool]): Whether to only return delete-protected
            devices
        created_by (Union[Unset, None, str]): ID of the user who created the device
        last_updated_by (Union[Unset, None, str]): ID of the user who last updated the device
        search (Union[Unset, None, str]): Search term to filter devices by
        search_fields (Union[Unset, None, str]): Comma-delimited list of fields to search in
        page_count (Union[None, Unset, bool, str]): Whether to only return the number of pages
        object_count (Union[None, Unset, bool, str]): Whether to only return the number of
            matching entries
        limit (Union[Unset, None, int]): Maximum number of objects to return
        page (Union[Unset, None, int]): Page number to return
        order_by (Union[Unset, None, str]): Field to order results by
        desc (Union[None, Unset, bool, str]): Whether to order results in descending order
        bust_cache (Union[None, Unset, bool, str]): Whether to bypass the cache and get the latest
            data
        created_date (Union[Unset, None, datetime.datetime]): Created date of items to return
        created_date_gte (Union[Unset, None, datetime.datetime]):
        created_date_lte (Union[Unset, None, datetime.datetime]):
        last_updated_date (Union[Unset, None, datetime.datetime]): Last edited date of items to
            return
        last_updated_date_gte (Union[Unset, None, datetime.datetime]):
        last_updated_date_lte (Union[Unset, None, datetime.datetime]):
        tags (Union[Unset, None, str]): Comma delimited list of tags on this device
        tags_contains (Union[Unset, None, str]):
        tags_contains_any (Union[Unset, None, str]):
        is_org_admin (Union[Unset, None, bool]): Whether to only return org admins
        is_project_admin (Union[Unset, None, bool]): Whether to only return project admins
        project_id (Union[Unset, None, str]): ID of the project to filter accounts by
        group_id (Union[Unset, None, str]): ID of the group to filter accounts by
        role_id (Union[Unset, None, str]): ID of the role to filter accounts by
        locale (Union[Unset, None, str]): Locale of the device
        locale_regex (Union[Unset, None, str]):
        zoneinfo (Union[Unset, None, str]): Timezone of the device
        zoneinfo_regex (Union[Unset, None, str]):
        last_seen (Union[Unset, None, datetime.datetime]): Last time the device was seen
        last_seen_gte (Union[Unset, None, datetime.datetime]):
        last_seen_lte (Union[Unset, None, datetime.datetime]):
        mfa_enabled (Union[Unset, None, bool]): Whether to only return users with MFA enabled
        sms_mfa_enabled (Union[Unset, None, bool]): Whether to only return users with SMS MFA
            enabled
        software_mfa_enabled (Union[Unset, None, bool]): Whether to only return users with
            software MFA enabled
        email (Union[Unset, None, str]): Email of the user
        email_regex (Union[Unset, None, str]):
        phone_number (Union[Unset, None, str]): Phone number of the user
        phone_number_regex (Union[Unset, None, str]):
        nickname (Union[Unset, None, str]): Nickname of the user
        nickname_regex (Union[Unset, None, str]):
        username (Union[Unset, None, str]): Username of the user
        username_regex (Union[Unset, None, str]):
        first_name (Union[Unset, None, str]): First (or given) name of the user
        first_name_regex (Union[Unset, None, str]):
        middle_name (Union[Unset, None, str]): Middle name of the user
        middle_name_regex (Union[Unset, None, str]):
        last_name (Union[Unset, None, str]): Last (or family) name of the user
        last_name_regex (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union['AdminUserList', 'AnonUserList', 'UserList']
    """

    return sync_detailed(
        client=client,
        is_active=is_active,
        is_delete_protected=is_delete_protected,
        created_by=created_by,
        last_updated_by=last_updated_by,
        search=search,
        search_fields=search_fields,
        page_count=page_count,
        object_count=object_count,
        limit=limit,
        page=page,
        order_by=order_by,
        desc=desc,
        bust_cache=bust_cache,
        created_date=created_date,
        created_date_gte=created_date_gte,
        created_date_lte=created_date_lte,
        last_updated_date=last_updated_date,
        last_updated_date_gte=last_updated_date_gte,
        last_updated_date_lte=last_updated_date_lte,
        tags=tags,
        tags_contains=tags_contains,
        tags_contains_any=tags_contains_any,
        is_org_admin=is_org_admin,
        is_project_admin=is_project_admin,
        project_id=project_id,
        group_id=group_id,
        role_id=role_id,
        locale=locale,
        locale_regex=locale_regex,
        zoneinfo=zoneinfo,
        zoneinfo_regex=zoneinfo_regex,
        last_seen=last_seen,
        last_seen_gte=last_seen_gte,
        last_seen_lte=last_seen_lte,
        mfa_enabled=mfa_enabled,
        sms_mfa_enabled=sms_mfa_enabled,
        software_mfa_enabled=software_mfa_enabled,
        email=email,
        email_regex=email_regex,
        phone_number=phone_number,
        phone_number_regex=phone_number_regex,
        nickname=nickname,
        nickname_regex=nickname_regex,
        username=username,
        username_regex=username_regex,
        first_name=first_name,
        first_name_regex=first_name_regex,
        middle_name=middle_name,
        middle_name_regex=middle_name_regex,
        last_name=last_name,
        last_name_regex=last_name_regex,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    is_active: Union[Unset, None, bool] = UNSET,
    is_delete_protected: Union[Unset, None, bool] = UNSET,
    created_by: Union[Unset, None, str] = UNSET,
    last_updated_by: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    search_fields: Union[Unset, None, str] = UNSET,
    page_count: Union[None, Unset, bool, str] = False,
    object_count: Union[None, Unset, bool, str] = False,
    limit: Union[Unset, None, int] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    order_by: Union[Unset, None, str] = UNSET,
    desc: Union[None, Unset, bool, str] = False,
    bust_cache: Union[None, Unset, bool, str] = False,
    created_date: Union[Unset, None, datetime.datetime] = UNSET,
    created_date_gte: Union[Unset, None, datetime.datetime] = UNSET,
    created_date_lte: Union[Unset, None, datetime.datetime] = UNSET,
    last_updated_date: Union[Unset, None, datetime.datetime] = UNSET,
    last_updated_date_gte: Union[Unset, None, datetime.datetime] = UNSET,
    last_updated_date_lte: Union[Unset, None, datetime.datetime] = UNSET,
    tags: Union[Unset, None, str] = UNSET,
    tags_contains: Union[Unset, None, str] = UNSET,
    tags_contains_any: Union[Unset, None, str] = UNSET,
    is_org_admin: Union[Unset, None, bool] = UNSET,
    is_project_admin: Union[Unset, None, bool] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    group_id: Union[Unset, None, str] = UNSET,
    role_id: Union[Unset, None, str] = UNSET,
    locale: Union[Unset, None, str] = UNSET,
    locale_regex: Union[Unset, None, str] = UNSET,
    zoneinfo: Union[Unset, None, str] = UNSET,
    zoneinfo_regex: Union[Unset, None, str] = UNSET,
    last_seen: Union[Unset, None, datetime.datetime] = UNSET,
    last_seen_gte: Union[Unset, None, datetime.datetime] = UNSET,
    last_seen_lte: Union[Unset, None, datetime.datetime] = UNSET,
    mfa_enabled: Union[Unset, None, bool] = UNSET,
    sms_mfa_enabled: Union[Unset, None, bool] = UNSET,
    software_mfa_enabled: Union[Unset, None, bool] = UNSET,
    email: Union[Unset, None, str] = UNSET,
    email_regex: Union[Unset, None, str] = UNSET,
    phone_number: Union[Unset, None, str] = UNSET,
    phone_number_regex: Union[Unset, None, str] = UNSET,
    nickname: Union[Unset, None, str] = UNSET,
    nickname_regex: Union[Unset, None, str] = UNSET,
    username: Union[Unset, None, str] = UNSET,
    username_regex: Union[Unset, None, str] = UNSET,
    first_name: Union[Unset, None, str] = UNSET,
    first_name_regex: Union[Unset, None, str] = UNSET,
    middle_name: Union[Unset, None, str] = UNSET,
    middle_name_regex: Union[Unset, None, str] = UNSET,
    last_name: Union[Unset, None, str] = UNSET,
    last_name_regex: Union[Unset, None, str] = UNSET,
) -> Response[Union["AdminUserList", "AnonUserList", "UserList"]]:
    """Get Users

     Get a list of all users

    Args:
        is_active (Union[Unset, None, bool]):  (Admin only) Whether to only return active devices
        is_delete_protected (Union[Unset, None, bool]): Whether to only return delete-protected
            devices
        created_by (Union[Unset, None, str]): ID of the user who created the device
        last_updated_by (Union[Unset, None, str]): ID of the user who last updated the device
        search (Union[Unset, None, str]): Search term to filter devices by
        search_fields (Union[Unset, None, str]): Comma-delimited list of fields to search in
        page_count (Union[None, Unset, bool, str]): Whether to only return the number of pages
        object_count (Union[None, Unset, bool, str]): Whether to only return the number of
            matching entries
        limit (Union[Unset, None, int]): Maximum number of objects to return
        page (Union[Unset, None, int]): Page number to return
        order_by (Union[Unset, None, str]): Field to order results by
        desc (Union[None, Unset, bool, str]): Whether to order results in descending order
        bust_cache (Union[None, Unset, bool, str]): Whether to bypass the cache and get the latest
            data
        created_date (Union[Unset, None, datetime.datetime]): Created date of items to return
        created_date_gte (Union[Unset, None, datetime.datetime]):
        created_date_lte (Union[Unset, None, datetime.datetime]):
        last_updated_date (Union[Unset, None, datetime.datetime]): Last edited date of items to
            return
        last_updated_date_gte (Union[Unset, None, datetime.datetime]):
        last_updated_date_lte (Union[Unset, None, datetime.datetime]):
        tags (Union[Unset, None, str]): Comma delimited list of tags on this device
        tags_contains (Union[Unset, None, str]):
        tags_contains_any (Union[Unset, None, str]):
        is_org_admin (Union[Unset, None, bool]): Whether to only return org admins
        is_project_admin (Union[Unset, None, bool]): Whether to only return project admins
        project_id (Union[Unset, None, str]): ID of the project to filter accounts by
        group_id (Union[Unset, None, str]): ID of the group to filter accounts by
        role_id (Union[Unset, None, str]): ID of the role to filter accounts by
        locale (Union[Unset, None, str]): Locale of the device
        locale_regex (Union[Unset, None, str]):
        zoneinfo (Union[Unset, None, str]): Timezone of the device
        zoneinfo_regex (Union[Unset, None, str]):
        last_seen (Union[Unset, None, datetime.datetime]): Last time the device was seen
        last_seen_gte (Union[Unset, None, datetime.datetime]):
        last_seen_lte (Union[Unset, None, datetime.datetime]):
        mfa_enabled (Union[Unset, None, bool]): Whether to only return users with MFA enabled
        sms_mfa_enabled (Union[Unset, None, bool]): Whether to only return users with SMS MFA
            enabled
        software_mfa_enabled (Union[Unset, None, bool]): Whether to only return users with
            software MFA enabled
        email (Union[Unset, None, str]): Email of the user
        email_regex (Union[Unset, None, str]):
        phone_number (Union[Unset, None, str]): Phone number of the user
        phone_number_regex (Union[Unset, None, str]):
        nickname (Union[Unset, None, str]): Nickname of the user
        nickname_regex (Union[Unset, None, str]):
        username (Union[Unset, None, str]): Username of the user
        username_regex (Union[Unset, None, str]):
        first_name (Union[Unset, None, str]): First (or given) name of the user
        first_name_regex (Union[Unset, None, str]):
        middle_name (Union[Unset, None, str]): Middle name of the user
        middle_name_regex (Union[Unset, None, str]):
        last_name (Union[Unset, None, str]): Last (or family) name of the user
        last_name_regex (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union['AdminUserList', 'AnonUserList', 'UserList']]
    """

    kwargs = _get_kwargs(
        is_active=is_active,
        is_delete_protected=is_delete_protected,
        created_by=created_by,
        last_updated_by=last_updated_by,
        search=search,
        search_fields=search_fields,
        page_count=page_count,
        object_count=object_count,
        limit=limit,
        page=page,
        order_by=order_by,
        desc=desc,
        bust_cache=bust_cache,
        created_date=created_date,
        created_date_gte=created_date_gte,
        created_date_lte=created_date_lte,
        last_updated_date=last_updated_date,
        last_updated_date_gte=last_updated_date_gte,
        last_updated_date_lte=last_updated_date_lte,
        tags=tags,
        tags_contains=tags_contains,
        tags_contains_any=tags_contains_any,
        is_org_admin=is_org_admin,
        is_project_admin=is_project_admin,
        project_id=project_id,
        group_id=group_id,
        role_id=role_id,
        locale=locale,
        locale_regex=locale_regex,
        zoneinfo=zoneinfo,
        zoneinfo_regex=zoneinfo_regex,
        last_seen=last_seen,
        last_seen_gte=last_seen_gte,
        last_seen_lte=last_seen_lte,
        mfa_enabled=mfa_enabled,
        sms_mfa_enabled=sms_mfa_enabled,
        software_mfa_enabled=software_mfa_enabled,
        email=email,
        email_regex=email_regex,
        phone_number=phone_number,
        phone_number_regex=phone_number_regex,
        nickname=nickname,
        nickname_regex=nickname_regex,
        username=username,
        username_regex=username_regex,
        first_name=first_name,
        first_name_regex=first_name_regex,
        middle_name=middle_name,
        middle_name_regex=middle_name_regex,
        last_name=last_name,
        last_name_regex=last_name_regex,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    is_active: Union[Unset, None, bool] = UNSET,
    is_delete_protected: Union[Unset, None, bool] = UNSET,
    created_by: Union[Unset, None, str] = UNSET,
    last_updated_by: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    search_fields: Union[Unset, None, str] = UNSET,
    page_count: Union[None, Unset, bool, str] = False,
    object_count: Union[None, Unset, bool, str] = False,
    limit: Union[Unset, None, int] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    order_by: Union[Unset, None, str] = UNSET,
    desc: Union[None, Unset, bool, str] = False,
    bust_cache: Union[None, Unset, bool, str] = False,
    created_date: Union[Unset, None, datetime.datetime] = UNSET,
    created_date_gte: Union[Unset, None, datetime.datetime] = UNSET,
    created_date_lte: Union[Unset, None, datetime.datetime] = UNSET,
    last_updated_date: Union[Unset, None, datetime.datetime] = UNSET,
    last_updated_date_gte: Union[Unset, None, datetime.datetime] = UNSET,
    last_updated_date_lte: Union[Unset, None, datetime.datetime] = UNSET,
    tags: Union[Unset, None, str] = UNSET,
    tags_contains: Union[Unset, None, str] = UNSET,
    tags_contains_any: Union[Unset, None, str] = UNSET,
    is_org_admin: Union[Unset, None, bool] = UNSET,
    is_project_admin: Union[Unset, None, bool] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    group_id: Union[Unset, None, str] = UNSET,
    role_id: Union[Unset, None, str] = UNSET,
    locale: Union[Unset, None, str] = UNSET,
    locale_regex: Union[Unset, None, str] = UNSET,
    zoneinfo: Union[Unset, None, str] = UNSET,
    zoneinfo_regex: Union[Unset, None, str] = UNSET,
    last_seen: Union[Unset, None, datetime.datetime] = UNSET,
    last_seen_gte: Union[Unset, None, datetime.datetime] = UNSET,
    last_seen_lte: Union[Unset, None, datetime.datetime] = UNSET,
    mfa_enabled: Union[Unset, None, bool] = UNSET,
    sms_mfa_enabled: Union[Unset, None, bool] = UNSET,
    software_mfa_enabled: Union[Unset, None, bool] = UNSET,
    email: Union[Unset, None, str] = UNSET,
    email_regex: Union[Unset, None, str] = UNSET,
    phone_number: Union[Unset, None, str] = UNSET,
    phone_number_regex: Union[Unset, None, str] = UNSET,
    nickname: Union[Unset, None, str] = UNSET,
    nickname_regex: Union[Unset, None, str] = UNSET,
    username: Union[Unset, None, str] = UNSET,
    username_regex: Union[Unset, None, str] = UNSET,
    first_name: Union[Unset, None, str] = UNSET,
    first_name_regex: Union[Unset, None, str] = UNSET,
    middle_name: Union[Unset, None, str] = UNSET,
    middle_name_regex: Union[Unset, None, str] = UNSET,
    last_name: Union[Unset, None, str] = UNSET,
    last_name_regex: Union[Unset, None, str] = UNSET,
) -> Optional[Union["AdminUserList", "AnonUserList", "UserList"]]:
    """Get Users

     Get a list of all users

    Args:
        is_active (Union[Unset, None, bool]):  (Admin only) Whether to only return active devices
        is_delete_protected (Union[Unset, None, bool]): Whether to only return delete-protected
            devices
        created_by (Union[Unset, None, str]): ID of the user who created the device
        last_updated_by (Union[Unset, None, str]): ID of the user who last updated the device
        search (Union[Unset, None, str]): Search term to filter devices by
        search_fields (Union[Unset, None, str]): Comma-delimited list of fields to search in
        page_count (Union[None, Unset, bool, str]): Whether to only return the number of pages
        object_count (Union[None, Unset, bool, str]): Whether to only return the number of
            matching entries
        limit (Union[Unset, None, int]): Maximum number of objects to return
        page (Union[Unset, None, int]): Page number to return
        order_by (Union[Unset, None, str]): Field to order results by
        desc (Union[None, Unset, bool, str]): Whether to order results in descending order
        bust_cache (Union[None, Unset, bool, str]): Whether to bypass the cache and get the latest
            data
        created_date (Union[Unset, None, datetime.datetime]): Created date of items to return
        created_date_gte (Union[Unset, None, datetime.datetime]):
        created_date_lte (Union[Unset, None, datetime.datetime]):
        last_updated_date (Union[Unset, None, datetime.datetime]): Last edited date of items to
            return
        last_updated_date_gte (Union[Unset, None, datetime.datetime]):
        last_updated_date_lte (Union[Unset, None, datetime.datetime]):
        tags (Union[Unset, None, str]): Comma delimited list of tags on this device
        tags_contains (Union[Unset, None, str]):
        tags_contains_any (Union[Unset, None, str]):
        is_org_admin (Union[Unset, None, bool]): Whether to only return org admins
        is_project_admin (Union[Unset, None, bool]): Whether to only return project admins
        project_id (Union[Unset, None, str]): ID of the project to filter accounts by
        group_id (Union[Unset, None, str]): ID of the group to filter accounts by
        role_id (Union[Unset, None, str]): ID of the role to filter accounts by
        locale (Union[Unset, None, str]): Locale of the device
        locale_regex (Union[Unset, None, str]):
        zoneinfo (Union[Unset, None, str]): Timezone of the device
        zoneinfo_regex (Union[Unset, None, str]):
        last_seen (Union[Unset, None, datetime.datetime]): Last time the device was seen
        last_seen_gte (Union[Unset, None, datetime.datetime]):
        last_seen_lte (Union[Unset, None, datetime.datetime]):
        mfa_enabled (Union[Unset, None, bool]): Whether to only return users with MFA enabled
        sms_mfa_enabled (Union[Unset, None, bool]): Whether to only return users with SMS MFA
            enabled
        software_mfa_enabled (Union[Unset, None, bool]): Whether to only return users with
            software MFA enabled
        email (Union[Unset, None, str]): Email of the user
        email_regex (Union[Unset, None, str]):
        phone_number (Union[Unset, None, str]): Phone number of the user
        phone_number_regex (Union[Unset, None, str]):
        nickname (Union[Unset, None, str]): Nickname of the user
        nickname_regex (Union[Unset, None, str]):
        username (Union[Unset, None, str]): Username of the user
        username_regex (Union[Unset, None, str]):
        first_name (Union[Unset, None, str]): First (or given) name of the user
        first_name_regex (Union[Unset, None, str]):
        middle_name (Union[Unset, None, str]): Middle name of the user
        middle_name_regex (Union[Unset, None, str]):
        last_name (Union[Unset, None, str]): Last (or family) name of the user
        last_name_regex (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union['AdminUserList', 'AnonUserList', 'UserList']
    """

    return (
        await asyncio_detailed(
            client=client,
            is_active=is_active,
            is_delete_protected=is_delete_protected,
            created_by=created_by,
            last_updated_by=last_updated_by,
            search=search,
            search_fields=search_fields,
            page_count=page_count,
            object_count=object_count,
            limit=limit,
            page=page,
            order_by=order_by,
            desc=desc,
            bust_cache=bust_cache,
            created_date=created_date,
            created_date_gte=created_date_gte,
            created_date_lte=created_date_lte,
            last_updated_date=last_updated_date,
            last_updated_date_gte=last_updated_date_gte,
            last_updated_date_lte=last_updated_date_lte,
            tags=tags,
            tags_contains=tags_contains,
            tags_contains_any=tags_contains_any,
            is_org_admin=is_org_admin,
            is_project_admin=is_project_admin,
            project_id=project_id,
            group_id=group_id,
            role_id=role_id,
            locale=locale,
            locale_regex=locale_regex,
            zoneinfo=zoneinfo,
            zoneinfo_regex=zoneinfo_regex,
            last_seen=last_seen,
            last_seen_gte=last_seen_gte,
            last_seen_lte=last_seen_lte,
            mfa_enabled=mfa_enabled,
            sms_mfa_enabled=sms_mfa_enabled,
            software_mfa_enabled=software_mfa_enabled,
            email=email,
            email_regex=email_regex,
            phone_number=phone_number,
            phone_number_regex=phone_number_regex,
            nickname=nickname,
            nickname_regex=nickname_regex,
            username=username,
            username_regex=username_regex,
            first_name=first_name,
            first_name_regex=first_name_regex,
            middle_name=middle_name,
            middle_name_regex=middle_name_regex,
            last_name=last_name,
            last_name_regex=last_name_regex,
        )
    ).parsed
