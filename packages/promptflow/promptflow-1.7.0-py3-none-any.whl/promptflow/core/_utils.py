# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
import multiprocessing
from pathlib import Path
from typing import Dict, Union

from promptflow._constants import DEFAULT_ENCODING, FLOW_META_JSON, FLOW_META_JSON_GEN_TIMEOUT, PROMPT_FLOW_DIR_NAME
from promptflow._utils.context_utils import _change_working_dir, inject_sys_path
from promptflow._utils.flow_utils import is_flex_flow, resolve_entry_file, resolve_flow_path
from promptflow._utils.logger_utils import LoggerFactory
from promptflow._utils.yaml_utils import load_yaml
from promptflow.core._errors import GenerateFlowMetaJsonError

logger = LoggerFactory.get_logger(name=__name__)


def _generate_meta_from_file(working_dir, source_path, entry, meta_dict, exception_list):
    from promptflow._core.tool_meta_generator import generate_flow_meta_dict_by_file

    with _change_working_dir(working_dir), inject_sys_path(working_dir):
        try:
            result = generate_flow_meta_dict_by_file(
                path=source_path,
                entry=entry,
            )
            meta_dict.update(result)
        except Exception as e:
            exception_list.append(str(e))


def _generate_flow_meta(
    flow_directory: Path,
    source_path: str,
    entry: str,
    timeout: int,
    *,
    load_in_subprocess: bool = True,
) -> Dict[str, dict]:
    """Generate tool meta from files.

    :param flow_directory: flow directory
    :param tools: tool list
    :param raise_error: whether raise error when generate meta failed
    :param timeout: timeout for generate meta
    :param include_errors_in_output: whether include errors in output
    :param load_in_subprocess: whether load tool meta with subprocess to prevent system path disturb. Default is True.
        If set to False, will load tool meta in sync mode and timeout need to be handled outside current process.
    :return: tool meta dict
    """
    if load_in_subprocess:
        # use multiprocess generate to avoid system path disturb
        manager = multiprocessing.Manager()
        meta_dict = manager.dict()
        exception_list = manager.list()
        p = multiprocessing.Process(
            target=_generate_meta_from_file, args=(flow_directory, source_path, entry, meta_dict, exception_list)
        )
        p.start()
        p.join(timeout=timeout)
        if p.is_alive():
            logger.warning(f"Generate meta timeout after {timeout} seconds, terminate the process.")
            p.terminate()
            p.join()
    else:
        meta_dict, exception_list = {}, []

        #  There is no built-in method to forcefully stop a running thread/coroutine in Python
        #  because abruptly stopping a thread can cause issues like resource leaks,
        #  deadlocks, or inconsistent states.
        #  Caller needs to handle the timeout outside current process.
        logger.warning(
            "Generate meta in current process and timeout won't take effect. "
            "Please handle timeout manually outside current process."
        )
        _generate_meta_from_file(flow_directory, source_path, entry, meta_dict, exception_list)
    # directly raise error if failed to generate meta
    if len(exception_list) > 0:
        error_message = "Generate meta failed, detail error:\n" + str(exception_list)
        raise GenerateFlowMetaJsonError(error_message)
    return dict(meta_dict)


def generate_flow_meta(
    flow_directory: Union[str, Path],
    source_path: str,
    entry: str,
    dump: bool = True,
    timeout: int = FLOW_META_JSON_GEN_TIMEOUT,
    load_in_subprocess: bool = True,
) -> dict:
    """Generate flow.json for a flow directory."""

    flow_meta = _generate_flow_meta(
        flow_directory=flow_directory,
        source_path=source_path,
        entry=entry,
        timeout=timeout,
        load_in_subprocess=load_in_subprocess,
    )

    if dump:
        # dump as flow.tools.json
        promptflow_folder = flow_directory / PROMPT_FLOW_DIR_NAME
        promptflow_folder.mkdir(exist_ok=True)
        with open(promptflow_folder / FLOW_META_JSON, mode="w", encoding=DEFAULT_ENCODING) as f:
            json.dump(flow_meta, f, indent=4)

    return flow_meta


def init_executable(*, flow_dag: dict = None, flow_path: Path = None, working_dir: Path = None):
    if flow_dag and flow_path:
        raise ValueError("flow_dag and flow_path cannot be both provided.")
    if not flow_dag and not flow_path:
        raise ValueError("flow_dag or flow_path must be provided.")
    if flow_dag and not working_dir:
        raise ValueError("working_dir must be provided when flow_dag is provided.")

    if flow_path:
        flow_dir, flow_filename = resolve_flow_path(flow_path)
        flow_dag = load_yaml(flow_dir / flow_filename)
        if not working_dir:
            working_dir = flow_dir

    from promptflow.contracts.flow import EagerFlow as ExecutableEagerFlow
    from promptflow.contracts.flow import Flow as ExecutableFlow

    if is_flex_flow(yaml_dict=flow_dag):

        entry = flow_dag.get("entry")
        entry_file = resolve_entry_file(entry=entry, working_dir=working_dir)

        # TODO(2991934): support environment variables here
        meta_dict = generate_flow_meta(
            flow_directory=working_dir,
            source_path=entry_file,
            entry=entry,
            dump=False,
        )
        return ExecutableEagerFlow.deserialize(meta_dict)

    # for DAG flow, use data to init executable to improve performance
    return ExecutableFlow._from_dict(flow_dag=flow_dag, working_dir=working_dir)
