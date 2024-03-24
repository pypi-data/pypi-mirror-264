# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/integrations/DomoJupyter.ipynb.

# %% auto 0
__all__ = [
    "GetJupyter_ErrorRetrievingAccount",
    "GetJupyter_ErrorRetrievingAccountProperty",
    "get_jupyter_account",
    "NoConfigCompanyError",
    "GetInstanceConfig",
    "InvalidAccountTypeError",
    "DomoJupyterAccount_InstanceAuth",
    "is_v2",
    "process_row",
    "GetDomains_Query_AuthMatch_Error",
    "InvalidAccountNameError",
    "GenerateAuth_InvalidDomoInstanceList",
    "GenerateAuth_CredentialsNotProvided",
]

# %% ../../nbs/integrations/DomoJupyter.ipynb 2
import pandas as pd
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


import re
import time
import json


from nbdev.showdoc import patch_to

import domolibrary.client.DomoAuth as dmda
import domolibrary.client.Logger as lc
import domolibrary.classes.DomoDataset as dmds
import domolibrary.utils.chunk_execution as ce


# %% ../../nbs/integrations/DomoJupyter.ipynb 5
class GetJupyter_ErrorRetrievingAccount(Exception):
    def __init__(self, account_name):
        self.message = f"failure to retrieve DomoDomoJupyter Account {account_name}"
        super().__init__(self.message)


class GetJupyter_ErrorRetrievingAccountProperty(Exception):
    def __init__(self, account_name, property_name):
        self.message = f"failure to retrieve {property_name} DomoDomoJupyter Account {account_name}"
        super().__init__(self.message)


def get_jupyter_account(
    account_name: str,  # name of account as it appears in the
    domojupyter_fn: callable,
    maximum_retry: int = 10,
) -> (
    list,
    dict,
):  # returns account properties list and a dictionary of the properties.
    """import a domojupyter account, will loop until success"""
    account_properties = None

    retry_attempt = 0
    while not account_properties and retry_attempt <= maximum_retry:
        try:
            account_properties = domojupyter_fn.get_account_property_keys(account_name)
            retry_attempt += 1

        except Exception as e:
            print(f"Error:  retry attempt {retry_attempt} - {account_name}: {e}")
            time.sleep(2)

    if not account_properties:
        raise GetJupyter_ErrorRetrievingAccount(account_name=account_name)

    obj = {}

    retry_attempt = 0
    for index, prop in enumerate(account_properties):
        value = None

        while not value and retry_attempt <= maximum_retry:
            try:
                value = domojupyter_fn.get_account_property_value(
                    account_name, account_properties[index]
                )

            except Exception as e:
                print(f"trying again - {prop} - {e}")
                time.sleep(2)

        if not value:
            raise GetJupyter_ErrorRetrievingAccountProperty(
                account_name=account_name, property_name=prop
            )

        obj.update({prop: value})

    return account_properties, obj


# %% ../../nbs/integrations/DomoJupyter.ipynb 6
class NoConfigCompanyError(Exception):
    def __init__(self, sql, domo_instance):
        message = f'SQL "{sql}" returned no results in {domo_instance}'
        self.message = message
        super().__init__(self.message)


class GetInstanceConfig:
    config: pd.DataFrame = None
    logger: lc.Logger = None

    def __init__(self, logger: Optional[lc.Logger] = None):
        self.logger = logger or lc.Logger(app_name="GetInstanceConfig")

    async def _retrieve_company_ds(
        self,
        config_auth: dmda.DomoAuth,
        dataset_id: str,
        sql: str,
        debug_prn: bool = False,
        debug_api: bool = False,
        debug_log: bool = False,
        debug_num_stacks_to_drop: int = 2,
    ) -> [dict]:  # list of config query
        """wrapper for `DomoDataset.query_dataset_private` retrieves company configuration dataset and stores it as config"""

        ds = await dmds.DomoDataset.get_from_id(
            auth=config_auth,
            dataset_id=dataset_id,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=self.__class__.__name__,
        )

        message = (
            f"⚙️ START - Retrieving company list \n{ds.display_url()} using \n{sql}"
        )

        if debug_prn:
            print(message)

        self.logger.log_info(message, debug_log=debug_log)

        config_df = await ds.query_dataset_private(
            auth=config_auth,
            dataset_id=dataset_id,
            sql=sql,
            debug_api=debug_api,
            loop_until_end=True,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=self.__class__.__name__,
            is_return_dataframe=False,
        )
        if len(config_df) == 0:
            raise NoConfigCompanyError(sql, domo_instance=config_auth.domo_instance)

        self.config = config_df

        message = f"\n⚙️ SUCCESS 🎉 Retrieved company list \nThere are {len(config_df)} companies to update"

        if debug_prn:
            print(message)
        self.logger.log_info(message, debug_log=debug_log)

        return config_df


# %% ../../nbs/integrations/DomoJupyter.ipynb 9
class InvalidAccountTypeError(Exception):
    """raised when account type is not expected type"""

    def __init__(self, account_name, account_type):

        self.message = f"account: {account_name} is not {account_type}"
        super().__init__(self.message)


@dataclass
class DomoJupyterAccount_InstanceAuth:
    """class for interacting with DomoJupyterAccount objects and generating a DomoAuth object"""

    account_name: str

    domo_username: str = None

    display_name: str = field(repr=False, default=None)

    domo_instance: str = field(repr=False, default=None)
    domo_instance_ls: list = field(repr=False, default=None)

    raw_cred: dict = field(repr=False, default=None)
    domo_password: str = field(repr=False, default=None)
    domo_access_token: str = field(repr=False, default=None)

    auth_ls: list = field(repr=False, default=None)

    account_name_mask = "^dj_.*_acc"

    def __post_init__(self):
        if not self.display_name and self.domo_username:
            self._set_display_name()

    def _set_display_name(self):
        clean_text = re.sub("@.*$", "", self.domo_username)
        self.display_name = clean_text

    @staticmethod
    def _test_regex_mask(
        test_string: str,  # the string to test
        regex_mask: str,  # the regex expression to test
    ) -> bool:  # boolean of the re match
        """tests if a string matches the regex pattern"""

        return bool(re.match(regex_mask, test_string))

    @staticmethod
    def _clean_account_admin_accounts(account_name):

        clean_str = re.sub("^dj_", "", account_name)
        clean_str = re.sub("_acc$", "", clean_str)

        return clean_str


# %% ../../nbs/integrations/DomoJupyter.ipynb 11
async def is_v2(instance_auth: dmda.DomoFullAuth):
    """wrapper for the domo boostrap.is_group_ownership_beta function to return a binary for if the instance has the group ownership beta enabled"""

    import domolibrary.classes.DomoBootstrap as dmbs

    domo_bootstrap = dmbs.DomoBootstrap(auth=instance_auth)
    is_v2 = await domo_bootstrap.is_feature_accountsv2_enabled()
    return 1 if is_v2 else 0


async def process_row(
    instance: dict,
    domo_instance,
    instance_creds: DomoJupyterAccount_InstanceAuth,
    config_enum=None,
    debug_api: bool = False,
    debug_prn: bool = False,
    logger=None,
):
    # convert DomoJupyterAccount_InstanceAuth obj to
    if isinstance(instance_creds, DomoJupyterAccount_InstanceAuth):
        instance_creds = instance_creds.generate_auth(domo_instance=domo_instance)

    instance.update({"instance_auth": instance_creds})

    try:
        await instance_creds.get_auth_token(debug_api=debug_api)
        instance.update({"is_valid": 1})

        if isinstance(instance_creds, dmda.DomoFullAuth):
            instance.update({"is_v2": await is_v2(instance_auth=instance_creds)})

    except (
        dmda.InvalidCredentialsError,
        dmda.AccountLockedError,
        dmda.InvalidInstanceError,
        dmda.NoAccessTokenReturned,
    ) as e:
        if debug_prn:
            print(e)
        logger.log_error(str(e))
        instance.update({"is_valid": 0})

    config_creds = None
    if config_enum and instance.get("config_exception_pw") == 0:
        config_creds = config_enum["config_1"].value

    elif config_enum and instance.get("config_exception_pw") == 1:
        config_creds = config_enum["config_0"].value

    if isinstance(config_creds, DomoJupyterAccount_InstanceAuth):
        config_creds = config_creds.generate_auth(domo_instance=domo_instance)

    instance.update({"config_auth": config_creds})

    return instance


# %% ../../nbs/integrations/DomoJupyter.ipynb 14
class GetDomains_Query_AuthMatch_Error(Exception):
    """raise if SQL query fails to return column named 'auth_match_col'"""

    def __init__(self, sql: str = None, domo_instance: str = None, message: str = None):
        self.message = (
            message
            or f"Query failed to return a column 'auth_match_col' sql = {sql} in {domo_instance}"
        )
        super().__init__(self.message)


@patch_to(GetInstanceConfig, cls_method=True)
async def get_domains_with_instance_auth(
    cls: GetInstanceConfig,
    default_auth: dmda.DomoAuth,  # default auth to use with each row
    auth_enum: Enum,  # Enum where enum_name should match to `auth_match_col` from config_sql query and enum_value is the appropriate DomoAuth or DomoJupyterAccount object
    config_auth: dmda.DomoAuth = None,  # which instance to retrieve configuration data from
    config_dataset_id: str = None,  # dataset_id to run config_sql query against
    config_sql: str = "select domain as domo_instance,concat(config_useprod, '-', project) as auth_match_col from table",
    debug_api: bool = False,
    debug_log: bool = False,
    debug_prn: bool = False,
    logger: lc.Logger = None,  # pass in Logger class
) -> (
    pd.DataFrame
):  # returns a dataframe with domo_instance, instance_auth, and binary column is_valid
    """uses a sql query to retrieve a list of domo_instances and map authentication object to each instance"""

    if not logger:
        logger = lc.Logger(app_name="get_domains_with_instance_auth")

    gic = cls(logger=logger)

    config_ls = await gic._retrieve_company_ds(
        config_auth=config_auth,
        dataset_id=config_dataset_id,
        sql=config_sql,
        debug_prn=debug_prn,
        debug_log=debug_log,
        debug_api=debug_api,
    )

    if "auth_match_col" not in config_ls[0]:
        message = f"Query failed to return a column 'auth_match_col' sql = {config_sql} in {config_auth.domo_instance}"
        raise GetDomains_Query_AuthMatch_Error(message)

    config_ls = await ce.gather_with_concurrency(
        *[
            process_row(
                instance=instance,
                domo_instance=instance["domo_instance"],
                instance_creds=(
                    auth_enum[instance["auth_match_col"]].value
                    if instance["auth_match_col"] in auth_enum._member_names_
                    else default_auth
                ),
                config_enum=(
                    auth_enum if "config_1" in auth_enum._member_names_ else None
                ),
                debug_api=debug_api,
                debug_prn=debug_prn,
                logger=logger,
            )
            for instance in config_ls
        ],
        n=10,
    )

    return pd.DataFrame(config_ls)


# %% ../../nbs/integrations/DomoJupyter.ipynb 17
class InvalidAccountNameError(Exception):
    """raised when account name does not follow format string"""

    def __init__(self, account_name=None, regex_pattern=None):
        account_str = f'"{account_name}" '
        regex_str = f'"{regex_pattern}"'

        message = f"string {account_str if account_name else ''}does not match regex pattern {regex_str or ''}"
        self.message = message

        super().__init__(self.message)


@patch_to(DomoJupyterAccount_InstanceAuth, cls_method=True)
def get_domo_instance_auth_account(
    cls: DomoJupyterAccount_InstanceAuth,
    account_name: str,  # domojupyter account to retrieve
    # Domo's domojupyter module, pass in b/c can only be retrieved inside Domo jupyter notebook environment
    domojupyter_fn: callable,
    # set the domo_instance or retrieve from the domojupyter_account credential store
    domo_instance=None,
):
    """
    retrieves Abstract Credential Store from DomoJupyter environment.
    expects credentials property to contain DOMO_USERNAME, DOMO_PASSWORD, or DOMO_ACCESS_TOKEN, and (optional) DOMO_INSTANCE
    """

    if not cls._test_regex_mask(account_name, cls.account_name_mask):
        raise InvalidAccountNameError(
            account_name=account_name, regex_pattern=cls.account_name_mask
        )

    account_properties, dj_account = get_jupyter_account(
        account_name, domojupyter_fn=domojupyter_fn
    )

    if account_properties != ["credentials"]:
        raise InvalidAccountTypeError(
            account_name=account_name, account_type="abstract_credential_store"
        )

    creds = json.loads(dj_account.get("credentials"))

    return cls(
        account_name=account_name,
        raw_cred=creds,
        domo_username=creds.get("DOMO_USERNAME"),
        domo_password=creds.get("DOMO_PASSWORD"),
        domo_access_token=creds.get("DOMO_ACCESS_TOKEN"),
        domo_instance=domo_instance or creds.get("DOMO_INSTANCE"),
    )


# %% ../../nbs/integrations/DomoJupyter.ipynb 19
class GenerateAuth_InvalidDomoInstanceList(Exception):
    def __init__(self):
        message = "provide a list of domo_instances"
        super().__init__(message)


class GenerateAuth_CredentialsNotProvided(Exception):
    def __init__(self):
        message = "object does not have a valid combination of credentials (access_token or username and password)"
        super().__init__(message)


@patch_to(DomoJupyterAccount_InstanceAuth)
def generate_auth(self, domo_instance):
    if self.domo_access_token:
        auth = dmda.DomoTokenAuth(
            domo_instance=domo_instance, domo_access_token=self.domo_access_token
        )

    elif self.domo_username and self.domo_password:

        auth = dmda.DomoFullAuth(
            domo_instance=domo_instance,
            domo_username=self.domo_username,
            domo_password=self.domo_password,
        )

    else:
        raise GenerateAuth_CredentialsNotProvided()

    return auth


@patch_to(DomoJupyterAccount_InstanceAuth)
def generate_auth_ls(
    self: DomoJupyterAccount_InstanceAuth,
    domo_instance_ls: list[str] = None,  # list of domo_instances
) -> list[dmda.DomoAuth]:  # list of domo auth objects
    """for every domo_instance in domo_instance_ls generates an DomoAuth object"""

    # reset internal lists
    self.domo_instance = None

    self.domo_instance_ls = list(set(domo_instance_ls or self.domo_instance_ls))

    if not self.domo_instance_ls:
        raise GenerateAuth_InvalidDomoInstanceList()

    self.auth_ls = []
    for domo_instance in self.domo_instance_ls:
        auth = self.generate_auth(domo_instance)

        self.auth_ls.append(auth)

    return self.auth_ls
