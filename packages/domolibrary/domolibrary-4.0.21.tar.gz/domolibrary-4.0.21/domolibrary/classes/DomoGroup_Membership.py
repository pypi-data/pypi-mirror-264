# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/classes/50_DomoGroup_Membership.ipynb.

# %% ../../nbs/classes/50_DomoGroup_Membership.ipynb 2
from __future__ import annotations
from typing import List

import httpx

from nbdev.showdoc import patch_to

import domolibrary.utils.chunk_execution as ce

import domolibrary.client.DomoAuth as dmda
import domolibrary.client.DomoError as de

import domolibrary.routes.group as group_routes

import domolibrary.classes.DomoUser as dmu

# %% auto 0
__all__ = ["UpdateGroupMembership", "GroupMembership"]


# %% ../../nbs/classes/50_DomoGroup_Membership.ipynb 4
class UpdateGroupMembership(de.DomoError):
    def __init__(self, member_name, group_name, domo_instance):
        super().__init__(
            domo_instance=domo_instance,
            message=f"unable to add {member_name} to {group_name}",
        )


class GroupMembership:
    _add_member_ls: list[str]
    _remove_group_ls: list[str]

    _add_owners_ls: list[str]
    _remove_owner_ls: list[str]

    _current_member_ls: list[str]
    _current_owner_ls: list[str]

    group = None

    def __init__(self, group):
        self.group = group

        self._add_member_ls: List[dict] = []
        self._remove_member_ls: List[dict] = []

        self._add_owner_ls: List[dict] = []
        self._remove_owner_ls: List[dict] = []

        self._current_member_ls = []
        self._current_owner_ls = []

    def _add_to_list(self, member, list_to_update, debug_prn: bool = False):
        import domolibrary.classes.DomoUser as dmu
        import domolibrary.classes.DomoGroup as dmg

        match_obj = next(
            (
                user_obj
                for user_obj in list_to_update
                if user_obj.get("id") == member.id
            ),
            None,
        )
        if match_obj:
            print(f"➡️ {member}  of type {type(member).__name__} already in ls")
            return list_to_update

        if debug_prn:
            print(
                f"➡️ adding {member.id}  of type {type(member).__name__} to {self.group.name}"
            )

        if isinstance(member, dmu.DomoUser):
            list_to_update.append({"id": str(member.id), "type": "USER"})

            return list_to_update

        if isinstance(member, dmg.DomoGroup):
            list_to_update.append({"id": str(member.id), "type": "GROUP"})

            return list_to_update

        member_name = (
            getattr(member, "name", None)
            or getattr(member, "display_name", None)
            or "name not provided"
        )

        raise UpdateGroupMembership(
            domo_instance=self.group.auth.domo_instance,
            group_name=self.group.name,
            member_name=member_name,
        )

    def _add_member(self, member, debug_prn: bool = False):
        return self._add_to_list(member, self._add_member_ls, debug_prn)

    def _remove_member(self, member, debug_prn: bool = False):
        if type(member).__name__ == "DomoGroup" and member.type == "system":
            if debug_prn:
                print(f"remove_owner - skipping {member.name} type is {member.type}")
            return
        return self._add_to_list(member, self._remove_member_ls, debug_prn)

    def _add_owner(self, member, debug_prn: bool = False):
        return self._add_to_list(member, self._add_owner_ls, debug_prn)

    def _remove_owner(self, member, debug_prn: bool = False):
        if type(member).__name__ == "DomoGroup" and member.type == "system":
            if debug_prn:
                print(f"remove_owner - skipping {member.name} type is {member.type}")
            return

        return self._add_to_list(member, self._remove_owner_ls, debug_prn)

    def _reset_obj(self):
        self._add_member_ls = []
        self._remove_member_ls = []

        self._add_owner_ls = []
        self._remove_owner_ls = []

    async def _update_group_access(
        self,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
    ):
        res = await group_routes.update_group_membership(
            auth=self.group.auth,
            group_id=self.group.id,
            add_member_arr=self._add_member_ls,
            remove_member_arr=self._remove_member_ls,
            add_owner_arr=self._add_owner_ls,
            remove_owner_arr=self._remove_owner_ls,
            debug_api=debug_api,
            session=session,
        )
        self._reset_obj()

        # add
        # remove
        # set


# %% ../../nbs/classes/50_DomoGroup_Membership.ipynb 6
@patch_to(GroupMembership)
async def get_owners(
    self: GroupMembership,
    auth: dmda.DomoAuth = None,
    return_raw: bool = False,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):
    import domolibrary.classes.DomoUser as dmu
    import domolibrary.classes.DomoGroup as dmg

    auth = auth or self.group.auth

    self._current_owner_ls = []

    res = await group_routes.get_group_owners(
        group_id=self.group.id, auth=self.group.auth
    )
    if return_raw:
        return res

    group_ids = [obj.get("id") for obj in res.response if obj.get("type") == "GROUP"]
    if group_ids:
        domo_groups = await ce.gather_with_concurrency(
            n=60,
            *[
                dmg.DomoGroup.get_by_id(group_id=group_id, auth=auth)
                for group_id in group_ids
            ],
        )
        self._current_owner_ls += domo_groups

    user_ids = [obj.get("id") for obj in res.response if obj.get("type") == "USER"]
    if user_ids:
        domo_users = await dmu.DomoUsers.by_id(
            user_ids=user_ids, auth=auth, only_allow_one=False
        )
        self._current_owner_ls += domo_users

    self.group.owner_id_ls = group_ids + user_ids
    self.group.owner_ls = self._current_owner_ls

    return self._current_owner_ls
    # return domo_users


# %% ../../nbs/classes/50_DomoGroup_Membership.ipynb 7
@patch_to(GroupMembership)
async def get_members(
    self: GroupMembership,
    auth: dmda.DomoAuth = None,
    return_raw: bool = False,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):
    import domolibrary.classes.DomoUser as dmu

    auth = auth or self.group.auth

    self._current_member_ls = []

    res = await group_routes.get_group_membership(
        group_id=self.group.id, auth=self.group.auth
    )
    if return_raw:
        return res

    user_ids = [obj.get("userId") for obj in res.response]
    if user_ids:
        domo_users = await dmu.DomoUsers.by_id(
            user_ids=user_ids, auth=auth, only_allow_one=False
        )
        self._current_member_ls += domo_users

    self.group.members_id_ls = user_ids
    self.group.members_ls = self._current_member_ls

    return self.group.members_ls


# %% ../../nbs/classes/50_DomoGroup_Membership.ipynb 9
@patch_to(GroupMembership)
async def add_members(
    self: GroupMembership,
    add_user_ls: list[dmu.DomoUser],
    return_raw: bool = False,
    debug_api: bool = False,
    debug_prn: bool = False,
    session: httpx.AsyncClient = None,
):
    self._reset_obj()

    [self._add_member(domo_user, debug_prn) for domo_user in add_user_ls]

    res = await self._update_group_access(debug_api=debug_api, session=session)

    if return_raw:
        return res

    return await self.get_members()


@patch_to(GroupMembership)
async def remove_members(
    self: GroupMembership,
    remove_user_ls: list[dmu.DomoUser],
    return_raw: bool = False,
    debug_api: bool = False,
    debug_prn: bool = False,
    session: httpx.AsyncClient = None,
):
    self._reset_obj()

    [self._remove_member(domo_user, debug_prn) for domo_user in remove_user_ls]

    res = await self._update_group_access(debug_api=debug_api, session=session)

    if return_raw:
        return res

    return await self.get_members()


@patch_to(GroupMembership)
async def set_members(
    self: GroupMembership,
    user_ls: list[dmu.DomoUser],
    return_raw: bool = False,
    debug_api: bool = False,
    debug_prn: bool = False,
    session: httpx.AsyncClient = None,
):
    self._reset_obj()

    domo_users = await self.get_members()

    if debug_prn:
        print({"domo_users": domo_users, "user_ls": user_ls})

    [self._add_member(domo_user, debug_prn) for domo_user in user_ls]
    [
        self._remove_member(domo_user, debug_prn)
        for domo_user in domo_users
        if domo_user not in user_ls
    ]

    res = await self._update_group_access(debug_api=debug_api, session=session)

    if return_raw:
        return res

    return await self.get_members()


# %% ../../nbs/classes/50_DomoGroup_Membership.ipynb 10
@patch_to(GroupMembership)
async def add_owners(
    self: GroupMembership,
    add_owner_ls,
    return_raw: bool = False,
    debug_api: bool = False,
    debug_prn: bool = False,
    session: httpx.AsyncClient = None,
):
    self._reset_obj()

    [self._add_owner(domo_user, debug_prn) for domo_user in add_owner_ls]

    res = await self._update_group_access(debug_api=debug_api, session=session)

    if return_raw:
        return res

    return await self.get_owners()


@patch_to(GroupMembership)
async def remove_owners(
    self: GroupMembership,
    remove_owner_ls,
    return_raw: bool = False,
    debug_api: bool = False,
    debug_prn: bool = False,
    session: httpx.AsyncClient = None,
):
    self._reset_obj()

    [self._remove_owner(domo_user, debug_prn) for domo_user in remove_owner_ls]

    res = await self._update_group_access(debug_api=debug_api, session=session)

    if return_raw:
        return res

    return await self.get_owners()


@patch_to(GroupMembership)
async def set_owners(
    self: GroupMembership,
    owner_ls,
    return_raw: bool = False,
    debug_api: bool = False,
    debug_prn: bool = False,
    session: httpx.AsyncClient = None,
):
    self._reset_obj()

    domo_users = await self.get_owners()

    if debug_prn:
        print({"domo_users": domo_users, "user_ls": owner_ls})

    [self._add_owner(domo_user, debug_prn) for domo_user in owner_ls]
    [
        self._remove_owner(domo_user, debug_prn)
        for domo_user in domo_users
        if domo_user not in owner_ls
    ]

    res = await self._update_group_access(debug_api=debug_api, session=session)

    if return_raw:
        return res

    return await self.get_owners()


# %% ../../nbs/classes/50_DomoGroup_Membership.ipynb 11
@patch_to(GroupMembership)
async def add_owner_manage_groups_role(self: GroupMembership):
    import domolibrary.classes.DomoGroup as dmg

    await dmg.DomoGroups.toggle_system_group_visibility(
        auth=self.group.auth, is_hide_system_groups=False
    )

    grant_group = await dmg.DomoGroup.search_by_name(
        auth=self.group.auth, group_name="Grant: Manage all groups"
    )

    await self.add_owners(add_owner_ls=[grant_group])

    await dmg.DomoGroups.toggle_system_group_visibility(
        auth=self.group.auth, is_hide_system_groups=True
    )
