# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/routes/application.ipynb.

# %% auto 0
__all__ = [
    "ApplicationError_NoneRetrieved",
    "get_applications",
    "get_application_by_id",
    "ApplicationError_NoJobRetrieved",
    "get_application_jobs",
    "get_application_job_by_id",
    "generate_remote_domostats",
    "generate_body_watchdog_generic",
    "CRUD_ApplicationJob_Error",
    "create_application_job",
    "update_application_job",
    "update_application_job_trigger",
    "execute_application_job",
]

# %% ../../nbs/routes/application.ipynb 2
from typing import Union
import httpx

import domolibrary.client.get_data as gd
import domolibrary.client.ResponseGetData as rgd
import domolibrary.client.DomoAuth as dmda
import domolibrary.client.DomoError as de

from pprint import pprint


# %% ../../nbs/routes/application.ipynb 4
class ApplicationError_NoneRetrieved(de.DomoError):
    def __init__(
        self,
        domo_instance,
        application_id=None,
        application_name=None,
        parent_class=None,
        function_name=None,
        job_id=None,
    ):
        message = "No applications retrieve"

        if application_id:
            message = f"unable to retrieve application - {application_id}"

        if application_name:
            message = f"unable to retrieve application - {application_name}"

        if application_id and job_id:
            message = (
                f"unable to retrieve {job_id} job from application - {application_name}"
            )

        super().__init__(
            message=message,
            parent_class=parent_class,
            function_name=function_name,
            domo_instance=domo_instance,
        )


@gd.route_function
async def get_applications(
    auth: dmda.DomoAuth,
    session: Union[httpx.AsyncClient, httpx.AsyncClient, None] = None,
    debug_api: bool = False,
    parent_class: str = None,
    debug_num_stacks_to_drop=1,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/executor/v1/applications/"

    if debug_api:
        print(url)

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if not res.is_success:
        raise ApplicationError_NoneRetrieved(
            domo_instance=auth.domo_instance,
            parent_class=parent_class,
            function_name=res.traceback_details.function_name,
        )
    return res


# %% ../../nbs/routes/application.ipynb 7
@gd.route_function
async def get_application_by_id(
    auth: dmda.DomoAuth,
    application_id: str,
    session: Union[httpx.AsyncClient, httpx.AsyncClient, None] = None,
    debug_api: bool = False,
    parent_class: str = None,
    debug_num_stacks_to_drop: int = 1,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/executor/v1/applications/{application_id}"

    if debug_api:
        print(url)

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if not res.is_success:
        raise ApplicationError_NoneRetrieved(
            domo_instance=auth.domo_instance,
            application_id=application_id,
            parent_class=parent_class,
            function_name=res.traceback_details.function_name,
        )

    return res


# %% ../../nbs/routes/application.ipynb 10
class ApplicationError_NoJobRetrieved(de.DomoError):
    def __init__(
        self,
        domo_instance,
        application_id=None,
        parent_class=None,
        function_name=None,
    ):
        message = f"no jobs retrieved from application - {application_id}"

        super().__init__(
            message=message,
            parent_class=parent_class,
            function_name=function_name,
            domo_instance=domo_instance,
        )


gd.route_function


async def get_application_jobs(
    auth: dmda.DomoFullAuth,
    application_id: str,
    parent_class: str = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop=2,
    session: Union[httpx.AsyncClient, httpx.AsyncClient, None] = None,
) -> rgd.ResponseGetData:

    offset_params = {"offset": "offset", "limit": "limit"}

    url = f"https://{auth.domo_instance}.domo.com/api/executor/v2/applications/{application_id}/jobs"

    def arr_fn(res) -> list[dict]:
        return res.response.get("jobs")

    res = await gd.looper(
        auth=auth,
        method="GET",
        url=url,
        arr_fn=arr_fn,
        loop_until_end=True,
        offset_params=offset_params,
        session=session,
        debug_api=debug_api,
    )

    if not res.is_success:
        raise ApplicationError_NoJobRetrieved(
            domo_instance=auth.domo_instance,
            application_id=application_id,
            parent_class=parent_class,
            function_name=res.traceback_details.function_name,
        )

    return res


# %% ../../nbs/routes/application.ipynb 12
@gd.route_function
async def get_application_job_by_id(
    auth: dmda.DomoFullAuth,
    application_id: str,
    job_id: str,
    parent_class: str = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop=2,
    session: Union[httpx.AsyncClient, httpx.AsyncClient, None] = None,
) -> rgd.ResponseGetData:

    url = f"https://{auth.domo_instance}.domo.com/api/executor/v1/applications/{application_id}/jobs/{job_id}"

    res = await gd.get_data(
        auth=auth,
        method="GET",
        url=url,
        session=session,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if not res.is_success:
        raise ApplicationError_NoneRetrieved(
            domo_instance=auth.domo_instance,
            application_id=application_id,
            parent_class=parent_class,
            function_name=res.traceback_details.function_name,
            job_id=job_id,
        )

    return res


# %% ../../nbs/routes/application.ipynb 15
def generate_remote_domostats(
    target_instance: str,
    report_dict: dict,
    output_dataset_id: str,
    account_id: str,
    schedule_ls: list,
    execution_timeout: int = 1440,
    debug_api: bool = False,
):

    instance_url = f"{target_instance}.domo.com"

    body = {
        "jobName": instance_url,
        "jobDescription": f"Get Remote stat from {instance_url}",
        "executionTimeout": execution_timeout,
        "executionPayload": {
            "remoteInstance": instance_url,
            "policies": report_dict,
            "metricsDatasetId": output_dataset_id,
        },
        "accounts": [account_id],
        "executionClass": "com.domo.executor.subscriberstats.SubscriberStatsExecutor",
        "resources": {"requests": {"memory": "256M"}, "limits": {"memory": "256M"}},
        "triggers": schedule_ls,
    }

    if debug_api:
        pprint(body)

    return body


def generate_body_watchdog_generic(
    job_name: str,
    notify_user_ids_ls: list,
    notify_group_ids_ls: list,
    notify_emails_ls: list,
    log_dataset_id: str,
    schedule_ls: list,
    watchdog_parameter_body: dict,
    execution_timeout=1440,
    debug_api: bool = False,
):

    body = {
        "jobName": job_name,
        "jobDescription": f"Watchdog for {job_name}",
        "executionTimeout": execution_timeout,
        "accounts": [],
        "executionPayload": {
            "notifyUserIds": notify_user_ids_ls or [],
            "notifyGroupIds": notify_group_ids_ls or [],
            "notifyEmailAddresses": notify_emails_ls or [],
            "watcherParameters": watchdog_parameter_body,
            "metricsDatasetId": log_dataset_id,
        },
        "resources": {"requests": {"memory": "256Mi"}, "limits": {"memory": "256Mi"}},
        "triggers": schedule_ls,
    }

    if debug_api:
        pprint(body)

    return body


# %% ../../nbs/routes/application.ipynb 16
class CRUD_ApplicationJob_Error(de.DomoError):
    def __init__(
        self, domo_instance, application_id, message, parent_class, function_name
    ):
        super().__init__(
            self,
            domo_instance=domo_instance,
            entity_id=application_id,
            parent_class=parent_class,
            function_name=function_name,
            message=message,
        )


# create the new RemoteDomostats job


@gd.route_function
async def create_application_job(
    auth: dmda.DomoFullAuth,
    body: dict,
    application_id: str,
    debug_api: bool = False,
    debug_num_stacks_to_drop=2,
    parent_class: str = None,
    session: Union[httpx.AsyncClient, httpx.AsyncClient, None] = None,
) -> rgd.ResponseGetData:

    url = f"https://{auth.domo_instance}.domo.com/api/executor/v1/applications/{application_id}/jobs"

    if debug_api:
        print(url)

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="POST",
        body=body,
        session=session,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if not res.is_success:
        raise CRUD_ApplicationJob_Error(
            domo_instance=auth.domo_instance,
            application_id=application_id,
            message=res.response,
            parent_class=parent_class,
            function_name=res.traceback_details.function_name,
        )

    return res


# update the job
@gd.route_function
async def update_application_job(
    auth: dmda.DomoFullAuth,
    body: dict,
    job_id: str,
    application_id: str,
    debug_num_stacks_to_drop=1,
    parent_class: str = None,
    session: Union[httpx.AsyncClient, httpx.AsyncClient, None] = None,
    debug_api: bool = False,
) -> rgd.ResponseGetData:

    url = f"https://{auth.domo_instance}.domo.com/api/executor/v1/applications/{application_id}/jobs/{job_id}"

    if debug_api:
        print(url)

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="PUT",
        body=body,
        debug_api=debug_api,
        session=session,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if not res.is_success:
        raise CRUD_ApplicationJob_Error(
            domo_instance=auth.domo_instance,
            application_id=application_id,
            message=res.response,
            parent_class=parent_class,
            function_name=res.traceback_details.function_name,
        )

    return res


@gd.route_function
async def update_application_job_trigger(
    auth: dmda.DomoFullAuth,
    body: dict,
    job_id: str,
    trigger_id: str,
    application_id: str,
    debug_num_stacks_to_drop=1,
    parent_class: str = None,
    session: Union[httpx.AsyncClient, httpx.AsyncClient, None] = None,
    debug_api: bool = False,
) -> rgd.ResponseGetData:

    url = f"https://{auth.domo_instance}.domo.com/api/executor/v1/applications/{application_id}/jobs/{job_id}/triggers/{trigger_id}"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="PUT",
        body=body,
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if not res.is_success:
        raise CRUD_ApplicationJob_Error(
            domo_instance=auth.domo_instance,
            application_id=application_id,
            message=res.response,
            parent_class=parent_class,
            function_name=res.traceback_details.function_name,
        )

    return res


# %% ../../nbs/routes/application.ipynb 17
@gd.route_function
async def execute_application_job(
    auth: dmda.DomoAuth,
    application_id,
    job_id,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class: str = None,
    session: httpx.AsyncClient = None,
):
    url = f"https://{auth.domo_instance}.domo.com/api/executor/v1/applications/{application_id}/jobs/{job_id}/executions"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="POST",
        body={},
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    return res
