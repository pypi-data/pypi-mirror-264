# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/client/95_Logger.ipynb.

# %% auto 0
__all__ = ["TracebackDetails", "get_traceback", "Logger"]

# %% ../../nbs/client/95_Logger.ipynb 2
import datetime as dt

from typing import Optional, List
from dataclasses import dataclass, field

import traceback

from nbdev.showdoc import patch_to


# %% ../../nbs/client/95_Logger.ipynb 5
@dataclass
class TracebackDetails:
    """result of _get_traceback_details function"""

    function_name: str
    file_name: str
    function_trail: str

    traceback_stack: [traceback.FrameSummary] = None
    parent_class: str = None

    def __init__(
        self,
        traceback_stack: [traceback.FrameSummary],
        parent_class=None,  # pass ParentClass.__name__
        debug_traceback: bool = False,
    ):
        self.function_trail = " -> ".join([line[2] for line in traceback_stack])

        self.function_name = traceback_stack[-1][2]
        self.file_name = traceback_stack[-1][0]
        self.parent_class = parent_class
        self.traceback_stack = traceback_stack


def get_traceback(
    root_module: str = "<module>",
    # drop entries from the top of stack to exclude the functions that retrieve the traceback
    num_stacks_to_drop=0,
    parent_class: str = None,
    debug_traceback: bool = False,
) -> TracebackDetails:  # returns a filtered list of FrameSummaries from traceback
    """method that retrieves traceback"""

    import traceback

    traceback_stack = traceback.extract_stack()

    # find the last module index
    module_index = 0

    for index, tb_line in enumerate(traceback_stack):
        function_name = tb_line[2]

        if function_name == root_module:
            module_index = index

    num_stacks_to_drop += 1  # adjust for init

    if module_index + num_stacks_to_drop >= len(traceback_stack) - 1:
        print("adjusting num_stacks_to_drop, consider revising `get_traceback` call")
        print(
            {
                "stack_length": len(traceback_stack),
                "module_index": module_index,
                "num_stacks_to_drop_passed": num_stacks_to_drop,
            }
        )
        num_stacks_to_drop -= 1

    filtered_traceback_stack = traceback_stack[module_index:-num_stacks_to_drop]

    if debug_traceback:
        print(
            {
                "len orig stack": len(traceback_stack),
                "len filtered stack": len(filtered_traceback_stack),
                "root_module_name": root_module,
                "root_module_index": module_index,
                "stacks_to_drop": num_stacks_to_drop,
            }
        )

    return TracebackDetails(
        traceback_stack=filtered_traceback_stack,
        parent_class=parent_class,
        debug_traceback=debug_traceback,
    )


# %% ../../nbs/client/95_Logger.ipynb 8
class Logger:
    """log class with user customizeable output method"""

    root_module: str
    app_name: str

    logs: List[dict]
    breadcrumb: Optional[list]

    entity_id: Optional[str]
    domo_instance: Optional[str]
    # function to call with write_logs method.
    output_fn: Optional[callable] = None

    def __init__(
        self,
        app_name: str,  # name of the app for grouping logs
        root_module: Optional[str] = "<module>",  # root module for stack trace
        output_fn: Optional[
            callable
        ] = None,  # function to call with write_logs method.
        entity_id: Optional[str] = None,
        domo_instance: Optional[str] = None,
    ):
        self.app_name = app_name
        self.output_fn = output_fn
        self.root_module = root_module
        self.logs = []
        self.breadcrumb = []
        self.domo_instance = domo_instance
        self.entity_id = entity_id

    def _add_crumb(self, crumb):
        if crumb not in self.breadcrumb:
            self.breadcrumb.append(crumb)

    def _remove_crumb(self, crumb):
        if crumb in self.breadcrumb:
            self.breadcrumb.remove(crumb)

    def get_traceback(
        self,
        root_module: str = "<module>",
        # drop entries from the top of stack to exclude the functions that retrieve the traceback
        num_stacks_to_drop=0,
        parent_class: str = None,
    ):
        parent_class = parent_class or self.__class__.__name__

        num_stacks_to_drop += 1

        return get_traceback(
            root_module=root_module,
            num_stacks_to_drop=num_stacks_to_drop,
            parent_class=parent_class,
        )


# %% ../../nbs/client/95_Logger.ipynb 13
@patch_to(Logger)
def _add_log(
    self: Logger,
    message: str,
    type_str: str,
    debug_log: bool = False,
    num_stacks_to_drop=3,
    entity_id: Optional[str] = None,
    domo_instance: Optional[str] = None,
) -> dict:
    """internal method to append message to log"""

    traceback_details = self.get_traceback(num_stacks_to_drop=num_stacks_to_drop)

    if debug_log:
        print(traceback_details.__dict__)

    new_row = {
        "date_time": dt.datetime.now(),
        "application": self.app_name,
        "log_type": type_str,
        "log_message": message,
        "breadcrumb": "->".join(self.breadcrumb),
        "domo_instance": domo_instance or self.domo_instance,
        "entity_id": entity_id or self.entity_id,
    }

    new_row.update(
        {
            "function_name": traceback_details.function_name,
            "file_name": traceback_details.file_name,
            "function_trail": traceback_details.function_trail,
        }
    )

    if debug_log:
        print(new_row)

    self.logs.append(new_row)

    return new_row


@patch_to(Logger)
def log_info(
    self: Logger,
    message,
    entity_id: Optional[str] = None,
    domo_instance: Optional[str] = None,
    debug_log=False,
    num_stacks_to_drop=3,
):
    """log an informational message"""
    return self._add_log(
        message=message,
        entity_id=entity_id,
        domo_instance=domo_instance,
        type_str="Info",
        num_stacks_to_drop=num_stacks_to_drop,
        debug_log=debug_log,
    )


@patch_to(Logger)
def log_error(
    self: Logger,
    message,
    entity_id: Optional[str] = None,
    domo_instance: Optional[str] = None,
    debug_log=False,
    num_stacks_to_drop=3,
):
    """log an error message"""

    return self._add_log(
        message=message,
        entity_id=entity_id,
        domo_instance=domo_instance,
        type_str="Error",
        num_stacks_to_drop=num_stacks_to_drop,
        debug_log=debug_log,
    )


@patch_to(Logger)
def log_warning(
    self: Logger,
    message,
    entity_id: Optional[str] = None,
    domo_instance: Optional[str] = None,
    debug_log=False,
    num_stacks_to_drop=3,
):
    """log a warning message"""

    return self._add_log(
        message=message,
        entity_id=entity_id,
        domo_instance=domo_instance,
        type_str="Warning",
        num_stacks_to_drop=num_stacks_to_drop,
        debug_log=debug_log,
    )


# %% ../../nbs/client/95_Logger.ipynb 16
@patch_to(Logger)
def output_log(self: Logger):
    """calls the user defined output function"""
    return self.output_fn(self.logs)
