from typing import List, Optional, Sequence, Union

from aidkit_client.resources.pipeline import PipelineRun


def convert_pipeline_runs_to_ids(
    report_pipeline_run_ids: List[int],
    pipeline_runs: Optional[Sequence[Union[PipelineRun, int]]] = None,
) -> List[int]:
    """
    Given a sequence of pipeline runs or integers as well as a list of pipeline run IDs as integers,
    transforms the sequence into a list of integers corresponding to the pipeline run IDs of
    the pipeline runs given.

    :param report_pipeline_run_ids: List of integers representing pipeline run IDs.
    :param pipeline_runs: Optional sequence of pipeline runs and pipeline run IDs.
    :raises ValueError: If some pipeline run IDs of `pipeline_runs` are not present in
        `report_pipeline_run_ids`.
    :return: The IDs of the pipeline runs provided. If `pipeline_runs` is set to none, return
        `preport_pipeline_run_ids` instead.
    """
    if pipeline_runs:
        pipeline_run_ids = [
            pipeline_run.id if isinstance(pipeline_run, PipelineRun) else pipeline_run
            for pipeline_run in pipeline_runs
        ]
        if not set(pipeline_run_ids) <= set(report_pipeline_run_ids):
            raise ValueError(
                "The pipeline runs with ID in "
                f"{set(pipeline_run_ids) - set(report_pipeline_run_ids)} are not "
                "included in this report."
            )
        return pipeline_run_ids
    else:
        return report_pipeline_run_ids
