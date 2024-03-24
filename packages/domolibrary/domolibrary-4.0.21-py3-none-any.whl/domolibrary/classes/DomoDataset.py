# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/classes/50_DomoDataset.ipynb.

# %% auto 0
__all__ = [
    "DatasetSchema_Types",
    "DomoDataset_Schema_Column",
    "DomoDataset_Schema",
    "DatasetTags_SetTagsError",
    "DomoDataset_Tags",
    "DomoDataset",
    "QueryExecutionError",
    "DomoDataset_DeleteDataset_Error",
    "DomoDataset_CreateDataset_Error",
]

# %% ../../nbs/classes/50_DomoDataset.ipynb 3
import json
import io

import httpx
import asyncio

import pandas as pd
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum

from nbdev.showdoc import patch_to

import domolibrary.utils.DictDot as util_dd
import domolibrary.utils.chunk_execution as ce

import domolibrary.client.DomoAuth as dmda
import domolibrary.client.DomoError as de

import domolibrary.routes.dataset as dataset_routes

import domolibrary.classes.DomoPDP as dmpdp
import domolibrary.classes.DomoCertification as dmdc

# %% ../../nbs/classes/50_DomoDataset.ipynb 5
from domolibrary.routes.dataset import (
    ShareDataset_AccessLevelEnum,
    DatasetNotFoundError,
    QueryRequestError,
    ShareDataset_Error,
    UploadDataError,
)


# %% ../../nbs/classes/50_DomoDataset.ipynb 7
async def _have_prereqs(self, auth, dataset_id, function_name):
    """tests if have a parent dataset or prerequsite dataset_id and auth object"""

    auth_from_self_dataset = (
        getattr(self.dataset, "auth", None) if getattr(self, "dataset", None) else None
    )
    auth_from_self = getattr(self, "auth", None)

    auth = auth or auth_from_self or auth_from_self_dataset

    await auth.get_auth_token()

    if not auth or not auth.token:
        raise de.AuthNotProvidedError(
            function_name=function_name, entity_id=self.dataset.id
        )

    id_from_self = getattr(self, "id", None)
    id_from_self_parent = (
        getattr(self.dataset, "id", None) if getattr(self, "dataset", None) else None
    )

    dataset_id = dataset_id or id_from_self or id_from_self_parent

    if not dataset_id:
        raise de.DatasetNotProvidedError(
            function_name=function_name, domo_instance=auth.domo_instance
        )

    return auth, dataset_id


# %% ../../nbs/classes/50_DomoDataset.ipynb 8
class DatasetSchema_Types(Enum):
    STRING = "STRING"
    DOUBLE = "DOUBLE"
    LONG = "LONG"
    DATE = "DATE"
    DATETIME = "DATETIME"


@dataclass
class DomoDataset_Schema_Column:
    name: str
    id: str
    type: DatasetSchema_Types
    order: int = 0
    visible: bool = True
    upsert_key: bool = False

    def __eq__(self, other):
        return self.id == other.id

    @classmethod
    def _from_json(cls, json_obj):
        dd = util_dd.DictDot(json_obj)
        return cls(
            name=dd.name,
            id=dd.id,
            type=dd.type,
            visible=dd.visible or dd.isVisible or True,
            upsert_key=dd.upsertKey or False,
            order=dd.order or 0,
        )

    def to_dict(self):
        s = self.__dict__
        s["upsertKey"] = s.pop("upsert_key") if "upsert_key" in s else False
        return s


@dataclass
class DomoDataset_Schema:
    """class for interacting with dataset schemas"""

    dataset: any = None
    columns: List[DomoDataset_Schema_Column] = field(default_factory=list)

    async def get(
        self,
        auth: Optional[dmda.DomoAuth] = None,
        dataset_id: str = None,
        debug_api: bool = False,
        return_raw: bool = False,  # return the raw response
    ) -> List[DomoDataset_Schema_Column]:
        """method that retrieves schema for a dataset"""

        auth, dataset_id = await _have_prereqs(
            self=self,
            auth=auth,
            dataset_id=dataset_id,
            function_name="DomoDataset_Schema.get",
        )

        res = await dataset_routes.get_schema(
            auth=auth, dataset_id=dataset_id, debug_api=debug_api
        )

        if return_raw:
            return res.response

        if res.status == 200:
            json_list = res.response.get("tables")[0].get("columns")

            self.columns = [
                DomoDataset_Schema_Column._from_json(json_obj=json_obj)
                for json_obj in json_list
            ]

            return self.columns


# %% ../../nbs/classes/50_DomoDataset.ipynb 12
class DatasetSchema_InvalidSchema(de.DomoError):
    def __init__(self, domo_instance, dataset_id, missing_columns, dataset_name=None):

        if dataset_id:
            message = f"{dataset_id}{f' - {dataset_name}' if dataset_name else ''} is missing columns {', '.join(missing_columns)}"

        super().__init__(domo_instance=domo_instance, message=message)


@patch_to(DomoDataset_Schema)
async def _test_missing_columns(
    self: DomoDataset_Schema,
    df: pd.DataFrame,
    dataset_id=None,
    auth: dmda.DomoAuth = None,
):

    dataset_id = dataset_id or self.dataset.id
    auth = auth or self.dataset.auth

    await self.get(dataset_id=dataset_id, auth=auth)

    missing_columns = [
        col for col in df.columns if col not in [scol.name for scol in self.columns]
    ]

    if len(missing_columns) > 0:
        raise DatasetSchema_InvalidSchema(
            domo_instance=auth.domo_instance,
            dataset_id=dataset_id,
            missing_columns=missing_columns,
        )
        return missing_columns

    return False


# %% ../../nbs/classes/50_DomoDataset.ipynb 14
@patch_to(DomoDataset_Schema)
async def reset_col_order(self: DomoDataset_Schema, df: pd.DataFrame, dataset_id):

    await self.get()

    if len(self.columns) != len(df.columns):
        raise Exception("")

    for index, col in enumerate(self.schema.columns):
        col.order = col.order if col.order > 0 else index

    # for index, schema in enumerate(consol_ds.schema.columns):
    #     schema.order = index

    # schema = {'columns': [col.__dict__ for col in consol_ds.schema.columns]}
    # schema

    # import domolibrary.routes.dataset as dataset_routes
    # await dataset_routes.alter_schema(auth = consol_auth, dataset_id = consol_ds.id, schema_obj = schema)

    df[[]]


# %% ../../nbs/classes/50_DomoDataset.ipynb 15
@patch_to(DomoDataset_Schema)
def to_dict(self: DomoDataset_Schema):
    return {"columns": [col.to_dict() for col in self.columns]}


# %% ../../nbs/classes/50_DomoDataset.ipynb 17
@patch_to(DomoDataset_Schema)
def add_col(
    self: DomoDataset_Schema, col: DomoDataset_Schema_Column, debug_prn: bool = False
):

    if col in self.columns and debug_prn:
        print(
            f"column - {col.name} already in dataset {self.dataset.name if self.dataset else '' }"
        )

    if col not in self.columns:
        self.columns.append(col)

    return self.columns


@patch_to(DomoDataset_Schema)
def remove_col(
    self: DomoDataset_Schema,
    remove_col: DomoDataset_Schema_Column,
    debug_prn: bool = False,
):

    [
        self.columns.pop(index)
        for index, col in enumerate(self.columns)
        if col == remove_col
    ]

    return self.columns


# %% ../../nbs/classes/50_DomoDataset.ipynb 19
@patch_to(DomoDataset_Schema)
async def alter_schema(
    self: DomoDataset_Schema,
    dataset_id: str = None,
    auth: dmda.DomoAuth = None,
    return_raw: bool = False,
    debug_api: bool = False,
):

    dataset_id = dataset_id or self.dataset.id
    auth = auth or self.dataset.auth

    schema_obj = self.to_dict()

    if return_raw:
        return schema_obj

    res = await dataset_routes.alter_schema(
        dataset_id=dataset_id, auth=auth, schema_obj=schema_obj, debug_api=debug_api
    )


# %% ../../nbs/classes/50_DomoDataset.ipynb 22
class DatasetTags_SetTagsError(Exception):
    """return if DatasetTags request is not successfull"""

    def __init__(self, dataset_id, domo_instance):
        message = f"failed to set tags on dataset - {dataset_id} in {domo_instance}"
        super().__init__(message)


@dataclass
class DomoDataset_Tags:
    """class for interacting with dataset tags"""

    dataset: any = None
    tag_ls: List[str] = field(default_factory=list)

    async def get(
        self,
        dataset_id: str = None,
        auth: Optional[dmda.DomoAuth] = None,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
    ) -> List[str]:  # returns a list of tags
        """gets the existing list of dataset_tags"""

        auth, dataset_id = await _have_prereqs(
            self=self,
            auth=auth,
            dataset_id=dataset_id,
            function_name="DomoDataset_Tages.get",
        )

        res = await dataset_routes.get_dataset_by_id(
            dataset_id=dataset_id, auth=auth, debug_api=debug_api, session=session
        )

        if res.is_success == False:
            print(res)
            return None

        tag_ls = []

        if res.response.get("tags"):
            tag_ls = json.loads(res.response.get("tags"))

        self.tag_ls = tag_ls

        return tag_ls

    async def set(
        self,
        tag_ls: List[str],
        dataset_id: str = None,
        auth: Optional[dmda.DomoAuth] = None,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
    ) -> List[str]:  # returns a list of tags
        """replaces all tags with a new list of dataset_tags"""

        auth, dataset_id = await _have_prereqs(
            self=self,
            auth=auth,
            dataset_id=dataset_id,
            function_name="DomoDatasetTags.set",
        )

        res = await dataset_routes.set_dataset_tags(
            auth=auth,
            tag_ls=list(set(tag_ls)),
            dataset_id=dataset_id,
            debug_api=debug_api,
            session=session,
        )

        if res.status != 200:
            raise DatasetTags_SetTagsError(
                dataset_id=dataset_id, domo_instance=auth.domo_instance
            )

        await self.get(dataset_id=dataset_id, auth=auth)

        return self.tag_ls


# %% ../../nbs/classes/50_DomoDataset.ipynb 25
@patch_to(DomoDataset_Tags)
async def add(
    self: DomoDataset_Tags,
    add_tag_ls: List[str],
    dataset_id: str = None,
    auth: Optional[dmda.DomoAuth] = None,
    debug_api: bool = False,
    session: Optional[httpx.AsyncClient] = None,
) -> List[str]:  # returns a list of tags
    """appends tags to the list of existing dataset_tags"""

    auth, dataset_id = await _have_prereqs(
        self=self,
        auth=auth,
        dataset_id=dataset_id,
        function_name="DomoDataset_Tags.add",
    )

    existing_tag_ls = await self.get(dataset_id=dataset_id, auth=auth) or []

    add_tag_ls += existing_tag_ls

    return await self.set(
        auth=auth,
        dataset_id=dataset_id,
        tag_ls=list(set(add_tag_ls)),
        debug_api=debug_api,
        session=session,
    )


# %% ../../nbs/classes/50_DomoDataset.ipynb 27
@patch_to(DomoDataset_Tags)
async def remove(
    self: DomoDataset_Tags,
    remove_tag_ls: List[str],
    dataset_id: str = None,
    auth: dmda.DomoFullAuth = None,
    debug_api: bool = False,
    session: Optional[httpx.AsyncClient] = None,
) -> List[str]:  # returns a list of tags
    """removes tags from the existing list of dataset_tags"""

    auth, dataset_id = await _have_prereqs(
        self=self,
        auth=auth,
        dataset_id=dataset_id,
        function_name="DomoDataset_Tags.remove",
    )

    existing_tag_ls = await self.get(dataset_id=dataset_id, auth=auth)

    existing_tag_ls = [ex for ex in existing_tag_ls if ex not in remove_tag_ls]

    return await self.set(
        auth=auth,
        dataset_id=dataset_id,
        tag_ls=list(set(existing_tag_ls)),
        debug_api=debug_api,
        session=session,
    )


# %% ../../nbs/classes/50_DomoDataset.ipynb 31
@dataclass
class DomoDataset:
    "interacts with domo datasets"

    auth: dmda.DomoAuth = field(repr=False, default=None)

    id: str = ""
    display_type: str = ""
    data_provider_type: str = ""
    name: str = ""
    description: str = ""
    row_count: int = None
    column_count: int = None

    stream_id: int = None

    owner: dict = field(default_factory=dict)
    formula: dict = field(default_factory=dict)

    schema: DomoDataset_Schema = field(default=None)
    tags: DomoDataset_Tags = field(default=None)

    certification: dmdc.DomoCertification = None
    PDP: dmpdp.Dataset_PDP_Policies = None

    def __post_init__(self):
        self.schema = DomoDataset_Schema(dataset=self)
        self.tags = DomoDataset_Tags(dataset=self)

        self.PDP = dmpdp.Dataset_PDP_Policies(dataset=self)

    def display_url(self):
        return f"https://{self.auth.domo_instance }.domo.com/datasources/{self.id}/details/overview"


# %% ../../nbs/classes/50_DomoDataset.ipynb 35
@patch_to(DomoDataset, cls_method=True)
async def get_from_id(
    cls: DomoDataset,
    dataset_id: str,
    auth: dmda.DomoAuth,
    debug_api: bool = False,
    return_raw: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop=2,
    parent_class: str = None,
):
    """retrieves dataset metadata"""

    parent_class = parent_class or cls.__name__

    res = await dataset_routes.get_dataset_by_id(
        auth=auth,
        dataset_id=dataset_id,
        debug_api=debug_api,
        session=session,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if return_raw:
        return res.response

    dd = util_dd.DictDot(res.response)
    ds = cls(
        auth=auth,
        id=dd.id,
        display_type=dd.displayType,
        data_provider_type=dd.dataProviderType,
        name=dd.name,
        description=dd.description,
        owner=res.response.get("owner"),
        stream_id=dd.streamId,
        row_count=int(dd.rowCount),
        column_count=int(dd.columnCount),
    )

    if dd.properties.formulas.formulas.__dict__:
        # print(dd.properties.formulas.formulas.__dict__)
        ds.formula = res.response.get("properties").get("formulas").get("formulas")

    if dd.tags:
        ds.tags.tag_ls = json.loads(dd.tags)

    if dd.certification:
        # print('class def certification', dd.certification)
        ds.certification = dmdc.DomoCertification._from_json(dd.certification)

    return ds


# %% ../../nbs/classes/50_DomoDataset.ipynb 40
class QueryExecutionError(de.DomoError):
    def __init__(
        self, sql, dataset_id, domo_instance, status, message, function_name=None
    ):

        message = f"error executing {sql}: {message}"

        super().__init__(
            entity_id=dataset_id,
            function_name=function_name,
            status=status,
            message=message,
            domo_instance=domo_instance,
        )


@patch_to(DomoDataset, cls_method=True)
async def query_dataset_private(
    cls: DomoDataset,
    auth: dmda.DomoAuth,  # DomoFullAuth or DomoTokenAuth
    dataset_id: str,
    sql: str,
    session: Optional[httpx.AsyncClient] = None,
    filter_pdp_policy_id_ls: List[int] = None,  # filter by pdp policy
    loop_until_end: bool = False,  # retrieve all available rows
    limit=100,  # maximum rows to return per request.  refers to PAGINATION
    skip=0,
    maximum=100,  # equivalent to the LIMIT or TOP clause in SQL, the number of rows to return total
    debug_api: bool = False,
    debug_loop: bool = False,
    debug_num_stacks_to_drop: int = 2,
    timeout=10,  # larger API requests may require a longer response time
    maximum_retry: int = 5,
    parent_class: str = None,
    is_return_dataframe: bool = True,
) -> pd.DataFrame:

    parent_class = parent_class or cls.__name__
    res = None
    retry = 1

    if filter_pdp_policy_id_ls and not isinstance(filter_pdp_policy_id_ls, list):
        filter_pdp_policy_id_ls = [int(filter_pdp_policy_id_ls)]

    while (not res or not res.is_success) and retry <= maximum_retry:
        try:
            res = await dataset_routes.query_dataset_private(
                auth=auth,
                dataset_id=dataset_id,
                sql=sql,
                maximum=maximum,
                filter_pdp_policy_id_ls=filter_pdp_policy_id_ls,
                skip=skip,
                limit=limit,
                loop_until_end=loop_until_end,
                session=session,
                debug_loop=debug_loop,
                debug_api=debug_api,
                timeout=timeout,
                debug_num_stacks_to_drop=debug_num_stacks_to_drop,
                parent_class=parent_class,
            )
        except dataset_routes.DatasetNotFoundError as e:
            print(e)
            return res

        except dataset_routes.QueryRequestError as e:
            print(e)
            return res

        except Exception as e:
            if retry <= maximum_retry:
                print(
                    f"⚠️ Error.  Attempt {retry} / {maximum_retry} - {e} - while query dataset {dataset_id} in {auth.domo_instance} with {sql}"
                )
            retry += 1

    if res and not res.is_success:
        raise QueryExecutionError(
            status=res.status,
            message=res.response,
            function_name="query_dataset_private",
            sql=sql,
            dataset_id=dataset_id,
            domo_instance=auth.domo_instance,
        )

    if is_return_dataframe:
        return pd.DataFrame(res.response)

    return res.response


# %% ../../nbs/classes/50_DomoDataset.ipynb 42
class DomoDataset_DeleteDataset_Error(de.DomoError):
    def __init__(self, dataset_id, status, reason, domo_instance, function_name):

        super().__init__(
            entity_id=dataset_id,
            function_name=function_name,
            status=status,
            message=reason,
            domo_instance=domo_instance,
        )


@patch_to(DomoDataset)
async def delete(
    self: DomoDataset,
    dataset_id=None,
    auth: dmda.DomoAuth = None,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):

    dataset_id = dataset_id or self.id
    auth = auth or self.auth

    res = await dataset_routes.delete(
        auth=auth, dataset_id=dataset_id, debug_api=debug_api, session=session
    )

    if not res.is_success:
        raise DomoDataset_DeleteDataset_Error(
            dataset_id=dataset_id,
            function_name="DomoDataset.delete",
            domo_instance=auth.domo_instance,
            status=res.status,
            reason=res.response,
        )

    return res


# %% ../../nbs/classes/50_DomoDataset.ipynb 43
@patch_to(DomoDataset)
async def share(
    self: DomoDataset,
    member,  # DomoUser or DomoGroup
    auth: dmda.DomoAuth = None,
    share_type: ShareDataset_AccessLevelEnum = ShareDataset_AccessLevelEnum.CAN_SHARE,
    is_send_email=False,
    debug_api: bool = False,
    debug_prn: bool = False,
    session: httpx.AsyncClient = None,
):

    body = dataset_routes.generate_share_dataset_payload(
        entity_type="GROUP" if type(member).__name__ == "DomoGroup" else "USER",
        entity_id=int(member.id),
        access_level=share_type,
        is_send_email=is_send_email,
    )

    res = await dataset_routes.share_dataset(
        auth=auth or self.auth,
        dataset_id=self.id,
        body=body,
        session=session,
        debug_api=debug_api,
    )

    return res


# %% ../../nbs/classes/50_DomoDataset.ipynb 47
@patch_to(DomoDataset)
async def index_dataset(
    self: DomoDataset,
    auth: dmda.DomoAuth = None,
    dataset_id: str = None,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):

    auth = auth or self.auth
    dataset_id = dataset_id or self.id
    return await dataset_routes.index_dataset(
        auth=auth, dataset_id=dataset_id, debug_api=debug_api, session=session
    )


# %% ../../nbs/classes/50_DomoDataset.ipynb 48
@patch_to(DomoDataset)
async def upload_data(
    self: DomoDataset,
    upload_df: pd.DataFrame = None,
    upload_df_ls: list[pd.DataFrame] = None,
    upload_file: io.TextIOWrapper = None,
    upload_method: str = "REPLACE",  # APPEND or REPLACE
    partition_key: str = None,
    is_index: bool = True,
    dataset_id: str = None,
    dataset_upload_id=None,
    auth: dmda.DomoAuth = None,
    session: httpx.AsyncClient = None,
    debug_api: bool = False,
    debug_prn: bool = False,
):

    auth, dataset_id = await _have_prereqs(
        self=self, auth=auth, dataset_id=dataset_id, function_name="upload_data"
    )

    upload_df_ls = upload_df_ls or [upload_df]

    status_message = f"{dataset_id} {partition_key} | {auth.domo_instance}"

    # stage 1 get uploadId
    retry = 1
    while dataset_upload_id is None and retry < 5:
        try:
            if debug_prn:
                print(f"\n\n🎭 starting Stage 1 - {status_message}")

            res = await dataset_routes.upload_dataset_stage_1(
                auth=auth,
                dataset_id=dataset_id,
                session=session,
                partition_tag=partition_key,
                debug_api=debug_api,
            )
            if debug_prn:
                print(f"\n\n🎭 Stage 1 response -- {res.status} for {status_message}")

            dataset_upload_id = res.response

        except dataset_routes.UploadDataError as e:
            print(f"{e} - attempt{retry}")
            retry += 1

            if retry == 5:
                print(f"failed to upload data for {dataset_id} in {auth.domo_instance}")
                raise e
                return

            await asyncio.sleep(5)

    # stage 2 upload_dataset
    if upload_file:
        if debug_prn:
            print(f"\n\n🎭 starting Stage 2 - upload file for {status_message}")

        res = await ce.gather_with_concurrency(
            n=60,
            *[
                dataset_routes.upload_dataset_stage_2_file(
                    auth=auth,
                    dataset_id=dataset_id,
                    upload_id=dataset_upload_id,
                    part_id=1,
                    data_file=upload_file,
                    session=session,
                    debug_api=debug_api,
                )
            ],
        )

    else:
        if debug_prn:
            print(
                f"\n\n🎭 starting Stage 2 - {len(upload_df_ls)} - number of parts for {status_message}"
            )

        res = await ce.gather_with_concurrency(
            n=60,
            *[
                dataset_routes.upload_dataset_stage_2_df(
                    auth=auth,
                    dataset_id=dataset_id,
                    upload_id=dataset_upload_id,
                    part_id=index + 1,
                    upload_df=df,
                    session=session,
                    debug_api=debug_api,
                )
                for index, df in enumerate(upload_df_ls)
            ],
        )

    if debug_prn:
        print(f"🎭 Stage 2 - upload data: complete for {status_message}")

    # stage 3 commit_data
    if debug_prn:
        print(
            f"\n\n🎭 starting Stage 3 - commit dataset_upload_id for {status_message}"
        )

    await asyncio.sleep(5)  # wait for uploads to finish

    res = await dataset_routes.upload_dataset_stage_3(
        auth=auth,
        dataset_id=dataset_id,
        upload_id=dataset_upload_id,
        update_method=upload_method,
        partition_tag=partition_key,
        is_index=False,
        session=session,
        debug_api=debug_api,
    )

    if debug_prn:
        print(f"\n🎭 stage 3 - commit dataset: complete for {status_message} ")

    if is_index:
        await asyncio.sleep(3)
        return await self.index_dataset(
            auth=auth, dataset_id=dataset_id, debug_api=debug_api, session=session
        )

    return res


# %% ../../nbs/classes/50_DomoDataset.ipynb 50
@patch_to(DomoDataset)
async def list_partitions(
    self: DomoDataset,
    auth: dmda.DomoAuth = None,
    dataset_id: str = None,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):

    auth = auth or self.auth
    dataset_id = dataset_id or self.id

    res = await dataset_routes.list_partitions(
        auth=auth, dataset_id=dataset_id, debug_api=debug_api, session=session
    )
    if res.status != 200:
        return None

    return res.response


# %% ../../nbs/classes/50_DomoDataset.ipynb 53
class DomoDataset_CreateDataset_Error(Exception):
    def __init__(self, domo_instance: str, dataset_name: str, status: int, reason: str):
        message = f"Failure to create dataset {dataset_name} in {domo_instance} :: {status} - {reason}"
        super().__init__(message)


@patch_to(DomoDataset, cls_method=True)
async def create(
    cls: DomoDataset,
    dataset_name: str,
    dataset_type="api",
    schema=None,
    auth: dmda.DomoAuth = None,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):
    schema = schema or {
        "columns": [
            {"name": "col1", "type": "LONG", "upsertKey": False},
            {"name": "col2", "type": "STRING", "upsertKey": False},
        ]
    }

    res = await dataset_routes.create(
        dataset_name=dataset_name,
        dataset_type=dataset_type,
        schema=schema,
        auth=auth,
        debug_api=debug_api,
        session=session,
    )

    if not res.is_success:
        raise DomoDataset_CreateDataset_Error(
            domo_instance=auth.domo_instance,
            dataset_name=dataset_name,
            status=res.status,
            reason=res.response,
        )

    dataset_id = res.response.get("dataSource").get("dataSourceId")

    return await cls.get_from_id(dataset_id=dataset_id, auth=auth)


# %% ../../nbs/classes/50_DomoDataset.ipynb 56
@patch_to(DomoDataset)
async def delete_partition(
    self: DomoDataset,
    dataset_partition_id: str,
    dataset_id: str = None,
    empty_df: pd.DataFrame = None,
    auth: dmda.DomoAuth = None,
    is_index: bool = True,
    debug_api: bool = False,
    debug_prn: bool = False,
    return_raw: bool = False,
):

    auth = auth or self.auth
    dataset_id = dataset_id or self.id

    if empty_df is None:
        empty_df = await self.query_dataset_private(
            auth=auth,
            dataset_id=dataset_id,
            sql="SELECT * from table limit 1",
            debug_api=debug_api,
        )

    await self.upload_data(
        upload_df=empty_df.head(0),
        upload_method="REPLACE",
        is_index=is_index,
        partition_key=dataset_partition_id,
        debug_api=debug_api,
    )
    if debug_prn:
        print(f"\n\n🎭 starting Stage 1")

    res = await dataset_routes.delete_partition_stage_1(
        auth=auth,
        dataset_id=dataset_id,
        dataset_partition_id=dataset_partition_id,
        debug_api=debug_api,
    )
    if debug_prn:
        print(f"\n\n🎭 Stage 1 response -- {res.status}")
        print(res)

    if debug_prn:
        print("starting Stage 2")

    res = await dataset_routes.delete_partition_stage_2(
        auth=auth,
        dataset_id=dataset_id,
        dataset_partition_id=dataset_partition_id,
        debug_api=debug_api,
    )

    if debug_prn:
        print(f"\n\n🎭 Stage 2 response -- {res.status}")

    if debug_prn:
        print("starting Stage 3")

    res = await dataset_routes.index_dataset(
        auth=auth, dataset_id=dataset_id, debug_api=debug_api
    )
    if debug_prn:
        print(f"\n\n🎭 Stage 3 response -- {res.status}")

    if return_raw:
        return res

    return res.response


# %% ../../nbs/classes/50_DomoDataset.ipynb 59
@patch_to(DomoDataset)
async def reset_dataset(
    self: DomoDataset,
    auth: dmda.DomoAuth = None,
    is_index: bool = True,
    debug_api: bool = False,
):

    execute_reset = input(
        "This function will delete all rows.  Type BLOW_ME_AWAY to execute:"
    )

    if execute_reset != "BLOW_ME_AWAY":
        print("You didn't type BLOW_ME_AWAY, moving on.")
        return None

    auth = auth or self.auth

    if not auth:
        raise Exception("auth required")

    # create empty dataset to retain schema
    empty_df = await self.query_dataset_private(
        auth=auth,
        dataset_id=self.id,
        sql="SELECT * from table limit 1",
        debug_api=debug_api,
    )
    empty_df = empty_df.head(0)

    # get partition list
    partition_list = await self.list_partitions()
    if len(partition_list) > 0:
        partition_list = ce.chunk_list(partition_list, 100)

    for index, pl in enumerate(partition_list):
        print(f"🥫 starting chunk {index + 1} of {len(partition_list)}")

        await asyncio.gather(
            *[
                self.delete_partition(
                    auth=auth,
                    dataset_partition_id=partition.get("partitionId"),
                    empty_df=empty_df,
                    debug_api=debug_api,
                )
                for partition in pl
            ]
        )
        if is_index:
            await self.index_dataset()

    res = await self.upload_data(
        upload_df=empty_df,
        upload_method="REPLACE",
        is_index=is_index,
        debug_api=debug_api,
    )

    return res
