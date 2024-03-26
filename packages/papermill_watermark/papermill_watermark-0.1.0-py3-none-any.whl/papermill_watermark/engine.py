import logging
from datetime import datetime
from typing import Tuple

import nbformat
from nbformat.v4 import new_output
from papermill.engines import NBClientEngine, NotebookExecutionManager
from papermill.utils import nb_language

try:
    import py3nvml

    _USE_GPU = "True"
except ImportError:
    _USE_GPU = "False"

_DEFAULT_PYTHON_CELL = f"import watermark; print(watermark.watermark() + watermark.watermark(iversions=True, globals_=globals(), githash=True, gpu={_USE_GPU}))"
_DEFAULT_R_CELL = "sessionInfo()"


def append_watermark(nb_man: NotebookExecutionManager) -> bool:
    language = nb_language(nb_man.nb)
    if language == "python":
        code = _DEFAULT_PYTHON_CELL
    elif language == "R":
        code = _DEFAULT_R_CELL
    else:
        logging.error(
            f"papermill_watermark only works with R & Python. Found {language}!"
        )
        return False
    cell = nbformat.v4.new_code_cell(
        code,
        metadata={
            "tags": [],
            "papermill": {
                "exception": None,
                "start_time": None,
                "end_time": None,
                "duration": None,
                "status": "pending",
            },
        },
    )
    nb_man.nb.cells.append(
        cell,
    )
    return True


def format_time(timedelta: float) -> Tuple[float, str]:
    if timedelta > 3600:
        timeformat = "hours"
        timedelta = timedelta / 3600
        return timedelta, timeformat
    if timedelta > 60:
        timedelta = timedelta / 60
        timeformat = "minutes"
        return timedelta, timeformat
    timeformat = "seconds"
    return timedelta, timeformat


class WatermarkEngine(NBClientEngine):
    @classmethod
    def execute_managed_notebook(cls, nb_man, kernel_name, **kwargs):
        appended_watermark = append_watermark(nb_man=nb_man)
        start = datetime.now()
        super().execute_managed_notebook(nb_man, kernel_name, **kwargs)
        end = datetime.now()
        watermark = []
        if appended_watermark:
            watermark = nb_man.nb.cells[-1].outputs
            nb_man.nb.cells = nb_man.nb.cells[:-1]
        timedelta, timeformat = format_time(timedelta=(end - start).total_seconds())
        output_message = f"Notebook execution took {timedelta:.1f} {timeformat}"
        output_node = new_output("display_data", data={"text/plain": [output_message]})
        nb_man.nb.cells.append(
            nbformat.v4.new_code_cell(
                "# Execution information",
                metadata={
                    "tags": [],
                    "papermill": {
                        "exception": None,
                        "start_time": None,
                        "end_time": None,
                        "duration": None,
                        "status": "finished",
                    },
                },
            )
        )
        nb_man.nb.cells[-1].outputs = (
            nb_man.nb.cells[-1].outputs + watermark + [output_node]
        )
