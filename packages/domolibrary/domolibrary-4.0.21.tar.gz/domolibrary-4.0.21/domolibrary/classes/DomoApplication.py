# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/classes/50_DomoApplication.ipynb.

# %% auto 0
__all__ = ["DomoApplication"]

# %% ../../nbs/classes/50_DomoApplication.ipynb 2
import pandas as pd
from dataclasses import dataclass, field
from typing import Optional, List
import httpx

from nbdev.showdoc import patch_to

import domolibrary.routes.application as application_routes
import domolibrary.classes.DomoApplication_Job as dmdj
import domolibrary.utils.DictDot as util_dd
import domolibrary.client.DomoAuth as dmda


# %% ../../nbs/classes/50_DomoApplication.ipynb 8
@dataclass
class DomoApplication:
    auth: dmda.DomoAuth = field(repr=False)
    id: str
    version: str = None
    name: str = None
    customer_id: str = None
    description: str = None
    execution_class: str = None
    grants: List[str] = None
    jobs: List[dmdj.DomoJob] = field(default=None)
    jobs_schedule: List[dmdj.DomoTrigger_Schedule] = field(default=None, repr=False)

    @classmethod
    def _from_json(cls, obj, auth: dmda.DomoFullAuth = None):
        dd = util_dd.DictDot(obj)

        return cls(
            id=dd.applicationId,
            customer_id=dd.customerId,
            name=dd.name,
            description=dd.description,
            version=dd.version,
            execution_class=dd.executionClass,
            grants=dd.authorities,
            auth=auth,
        )

    def _get_job_class(self):
        return DomoJob_Types.get_from_api_name(self.name)


# %% ../../nbs/classes/50_DomoApplication.ipynb 9
@patch_to(DomoApplication, cls_method=True)
async def get_from_id(
    cls,
    auth: dmda.DomoAuth,
    application_id,
    return_raw: bool = False,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop=2,
):
    res = await application_routes.get_application_by_id(
        application_id=application_id,
        auth=auth,
        session=session,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    return cls._from_json(obj=res.response, auth=auth)


# %% ../../nbs/classes/50_DomoApplication.ipynb 15
@patch_to(DomoApplication)
async def find_next_job_schedule(
    self, return_raw: bool = False
) -> dmdj.DomoTrigger_Schedule:

    await self.get_jobs()
    await self.get_schedules()

    df_all_hours = pd.DataFrame(range(0, 23), columns=["hour"])
    df_all_minutes = pd.DataFrame(range(0, 60), columns=["minute"])

    df_all_hours["tmp"] = 1
    df_all_minutes["tmp"] = 1
    df_all = pd.merge(df_all_hours, df_all_minutes, on="tmp").drop(columns=["tmp"])

    # get the number of occurencies of each hour and minutes
    schedules_grouped = (
        self.jobs_schedule.groupby(["hour", "minute"])
        .size()
        .reset_index(name="cnt_schedule")
    )

    # print(schedules_grouped)
    # print(df_all)

    schedules_interpolated = pd.merge(
        df_all, schedules_grouped, how="left", on=["hour", "minute"]
    )

    schedules_interpolated["cnt_schedule"] = schedules_interpolated[
        "cnt_schedule"
    ].fillna(value=0)
    schedules_interpolated.sort_values(
        ["cnt_schedule", "hour", "minute"], ascending=True, inplace=True
    )

    schedules_interpolated.reset_index(drop=True, inplace=True)

    if return_raw:
        return schedules_interpolated

    return dmdj.DomoTrigger_Schedule(
        hour=int(schedules_interpolated.loc[0].get("hour")),
        minute=int(schedules_interpolated.loc[0].get("minute")),
    )
