import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple, Union

from IPython.display import display  # type: ignore[import-untyped]
from pandas import DataFrame, concat
from tqdm import tqdm

from aidkit_client._download_manager.async_download_manager import AsyncDownloadManager
from aidkit_client._download_manager.caching_file_getter_proxy import (
    CachingFileGetterProxy,
)
from aidkit_client._download_manager.download_images_to_memory import (
    DownloadImagesToMemoryDownloadManager,
)
from aidkit_client._download_manager.download_storage import OnDiskDownloadStorage
from aidkit_client._download_manager.downloaded_files_progress_tracker import (
    DownloadedFilesProgressTracker,
)
from aidkit_client._download_manager.http_download import HttpFileGetter
from aidkit_client._download_manager.key_hashing_for_key_value_storage_proxy import (
    KeyHashingForKeyValueStorageProxy,
)
from aidkit_client._download_manager.local_path_for_storage_path_getter_proxy import (
    LocalPathForStoragePathGetterProxy,
)
from aidkit_client._download_manager.progress_tracking_file_getter_proxy import (
    ProgressTrackingFileGetterProxy,
)
from aidkit_client._download_manager.retrying_file_getter_proxy import (
    RetryingFileGetterProxy,
)
from aidkit_client._endpoints.models import PaginationResponse, ReportResponse
from aidkit_client._endpoints.pagination import PaginationParameters
from aidkit_client._endpoints.report import ReportAPI
from aidkit_client.aidkit_api import HTTPService
from aidkit_client.configuration import get_api_client
from aidkit_client.resources.pipeline import PipelineRun
from aidkit_client.resources.report import (
    ConfigurationName,
    MethodConfiguration,
    MethodConfigurationParameterString,
    MethodName,
    ReportConfiguration,
)
from aidkit_client.resources.report._utils import convert_pipeline_runs_to_ids
from aidkit_client.resources.report.tables.augmentation_examples_table import (
    AugmentationExamplesTable,
)
from aidkit_client.resources.report.tables.summary_table import (
    SummaryTable,
)

_DOWNLOAD_MAX_RETRIES = 3
_DOWNLOAD_MAX_SIMULTANEOUS = 32


class Report:
    """
    Report holding information about the pipeline run.
    """

    def __init__(
        self,
        api_service: HTTPService,
        report_response: ReportResponse,
        pipeline_run_ids: List[int],
    ) -> None:
        self._api_service = api_service

        method_configurations: Dict[
            MethodName, Dict[ConfigurationName, MethodConfiguration]
        ] = defaultdict(dict)
        method_configuration_names: Dict[
            MethodName, Dict[MethodConfigurationParameterString, MethodName]
        ] = defaultdict(dict)
        for (
            method_name,
            configuration,
        ) in report_response.configuration.method_configurations.items():
            for configuration_name, configuration_parameters in configuration.items():
                method_configurations[method_name][configuration_name] = MethodConfiguration(
                    **configuration_parameters.dict()
                )

                method_configuration_names[method_name][
                    json.dumps(configuration_parameters.parameters)
                ] = configuration_name

        self.configuration = ReportConfiguration(
            dataset_name=report_response.configuration.dataset_name,
            subset_name=report_response.configuration.subset_name,
            pipeline_run_ids=pipeline_run_ids,
            odd_tags={
                int(observation_id): odd_tags
                for observation_id, odd_tags in report_response.configuration.odd_tags.items()
            },
            number_of_frames=report_response.configuration.number_of_frames,
            method_configurations=dict(method_configurations),
            method_configuration_names=dict(method_configuration_names),
        )

    @classmethod
    async def get(cls, pipeline_runs: Sequence[Union[PipelineRun, int]]) -> "Report":
        """
        Get a report from the aidkit deployment for multiple pipeline runs. Pipeline runs need to
        have been configured using the same subset to be aggregated together.

        :param pipeline_runs: Sequence of pipeline runs to get a report for. If an integer is
            passed, it is considered as a pipeline run ID.
        :return: The report associated with the given pipeline run.
        """
        pipeline_run_ids = [
            pipeline_run.id if isinstance(pipeline_run, PipelineRun) else pipeline_run
            for pipeline_run in pipeline_runs
        ]

        api_service = get_api_client()
        report = Report(
            api_service=api_service,
            report_response=await ReportAPI(api_service).get_report(
                pipeline_run_ids=pipeline_run_ids
            ),
            pipeline_run_ids=pipeline_run_ids,
        )

        return report

    def display_summary_table(
        self,
        selected_augmentation: Optional[str] = None,
        as_html: bool = True,
        dark_mode: bool = True,
    ) -> None:
        """
        Display the report summary table. Note that display of HTML tables outside jupyter
        notebook environments may result in undesirable behavior.

        :param selected_augmentation: If provided, render only information about the chosen
            augmentation.
        :param as_html: If true, render a table in HTML format instead of ASCII.
        :param dark_mode: Render HTML tables in dark mode.
        """
        summary_table = SummaryTable(self.configuration).render(
            selected_augmentation=selected_augmentation,
            as_html=as_html,
            dark_mode=dark_mode,
        )

        if as_html:
            display(summary_table)
        else:
            print(str(summary_table))

    async def display_augmentation_examples_table(
        self,
        method_name: str,
        method_configuration_names: Optional[List[str]] = None,
        number_of_observations: int = 3,
        number_of_augmented_observations: int = 3,
        dark_mode: bool = True,
    ) -> None:
        """
        Display a table showing the effect of the augmentations applied on a few observations.

        :param method_name: Name of the augmentation method for which examples are displayed.
        :param method_configuration_names: Method configurations to include in the table. If not
            specified, every configuration for the requested method is included.
        :param number_of_observations: Maximum number of observations to display in the table.
        :param number_of_augmented_observations: Maximum number of augmented observations to display
            for each observation.
        :param dark_mode: Display the table using a dark color palette.
        :raises KeyError: If the method name provided does not correpond to the name of an
            augmentation method configured for this report.
        :raises KeyError: If a method configuration name provided does not correpond to the name
            of a method configuration of the augmentation method selected for this table.
        """
        if method_name not in self.configuration.method_configuration_names:
            raise KeyError(
                f"This report does not include data for the augmentation method '{method_name}'."
                "Available method names are "
                f"{list(self.configuration.method_configuration_names.keys())}"
            )

        if not method_configuration_names:
            method_configuration_parameters_strings = list(
                self.configuration.method_configuration_names[method_name].keys()
            )
        else:
            method_configuration_parameters_strings = []
            for configuration_name in method_configuration_names:
                if configuration_name not in self.configuration.method_configurations[method_name]:
                    raise KeyError(
                        "This report does not include a configuration with name "
                        f"'{configuration_name}' for the augmentation method '{method_name}'. "
                        "Available configuration names are "
                        f"{list(self.configuration.method_configurations[method_name].keys())}"
                    )

                method_configuration_parameters_strings.append(
                    json.dumps(
                        self.configuration.method_configurations[method_name][
                            configuration_name
                        ].parameters
                    )
                )

        augmented_data_list = await ReportAPI(
            self._api_service
        ).get_augmentation_example_table_data(
            pipeline_run_ids=self.configuration.pipeline_run_ids,
            method_name=method_name,
            method_configuration_parameters_strings=method_configuration_parameters_strings,
            number_of_observations=number_of_observations,
        )

        table = AugmentationExamplesTable(
            example_data=augmented_data_list,
            report_configuration=self.configuration,
            number_of_example_augmentations=number_of_augmented_observations,
            number_of_example_observations=number_of_observations,
        )

        image_paths = []
        for _, row in table.dataframe.iterrows():
            image_paths.append(row[0]["observation_url"])
            for augmented_frame in row["Augmented Frames"]:
                image_paths.append(augmented_frame["augmentation_url"])

        download_manager = DownloadImagesToMemoryDownloadManager(
            client=self._api_service,
            max_width_height=table.thumbnail_width_height,
        )

        downloaded_images = await download_manager.download(image_paths)

        rendered_table = table.render(images=downloaded_images, dark_mode=dark_mode)
        display(rendered_table)

    async def download_augmented_observations(
        self, download_directory: Path, print_progress: bool = True
    ) -> None:
        """
        Download the augmented observations resulting from the pipeline runs considered in this
        report to the specified location.

        :param download_directory: Path to the directory in which the augmented observations are
            downloaded
        :param print_progress: If true, prints a progress bar.
        """
        progress_tracker = DownloadedFilesProgressTracker()

        uri_to_file_name_dictionary: Dict[str, str] = {}
        download_storage = OnDiskDownloadStorage(base_path=str(download_directory))
        download_storage_proxy = KeyHashingForKeyValueStorageProxy(
            uri_to_key_factory=lambda uri: uri_to_file_name_dictionary[uri],
            storage=download_storage,
        )
        local_path_getter_proxy = LocalPathForStoragePathGetterProxy(
            uri_to_key_factory=lambda uri: uri_to_file_name_dictionary[uri],
            local_path_getter=download_storage,
        )

        download_manager = AsyncDownloadManager(
            getter=ProgressTrackingFileGetterProxy(
                file_getter=CachingFileGetterProxy(
                    file_getter=RetryingFileGetterProxy(
                        file_getter=HttpFileGetter(client=self._api_service),
                        number_of_retries=_DOWNLOAD_MAX_RETRIES,
                    ),
                    storage=download_storage_proxy,
                ),
                progress_tracker=progress_tracker,
            ),
            storage=download_storage_proxy,
            number_of_parallel_asynchronous_requests=_DOWNLOAD_MAX_SIMULTANEOUS,
            local_path_getter=local_path_getter_proxy,
        )

        offset = 0
        all_data_processed = False

        with tqdm(
            total=100,
            ascii=True,
            postfix="Downloading...",
            unit="%",
            disable=not print_progress,
        ) as progress_bar:

            def update_with_computed_progress(new_progress: int) -> None:
                old_progress = progress_bar.n
                progress_increase = new_progress - old_progress
                progress_bar.update(progress_increase)

            progress_tracker.subscribe(update_with_computed_progress)

            while not all_data_processed:
                response = await ReportAPI(self._api_service).get_augmented_observation_information(
                    pipeline_run_ids=self.configuration.pipeline_run_ids,
                    pagination_parameters=PaginationParameters(offset=offset),
                )

                progress_tracker.set_total(response.filter.pagination.total_number_of_items)

                uri_to_file_name_dictionary = {}
                for augmented_observation_information in response.items:
                    configuration_name = self.configuration.method_configuration_names[
                        augmented_observation_information.method_name
                    ][augmented_observation_information.method_parameters]
                    download_file_name = (
                        f"{augmented_observation_information.method_name}/"
                        f"{configuration_name}/"
                        f"{augmented_observation_information.augmented_observation_id}_"
                        f"{augmented_observation_information.observation_file_name}"
                    )
                    uri_to_file_name_dictionary[
                        augmented_observation_information.augmented_observation_url
                    ] = download_file_name

                await download_manager.download(
                    storage_paths=list(uri_to_file_name_dictionary.keys())
                )

                offset += response.filter.pagination.limit
                all_data_processed = offset >= response.filter.pagination.total_number_of_items

    async def get_data_page(
        self,
        pipeline_runs: Optional[Sequence[Union[PipelineRun, int]]] = None,
        offset: int = 0,
        limit: int = 100,
    ) -> Tuple[DataFrame, PaginationResponse]:
        """
        Get the raw report data limited to a page with offset and limit.

        :param pipeline_runs: The pipeline runs to include in the raw data. If not provided, all
            the pipeline runs used to get the report will be included.
        :param offset: Specifies with which index to start the page.
        :param limit: Specifies how many entries the page should have.

        :returns: The dataframe holding the report data and the PaginationResponse.
        """
        pipeline_run_ids = convert_pipeline_runs_to_ids(
            self.configuration.pipeline_run_ids, pipeline_runs
        )

        df, pagination_response = await _get_dataframe_and_pagination_response(
            pipeline_run_ids, PaginationParameters(offset=offset, limit=limit)
        )
        return df, pagination_response

    async def get_data(
        self,
        pipeline_runs: Optional[Sequence[Union[PipelineRun, int]]] = None,
    ) -> DataFrame:
        """
        Get the full raw report data.

        If you want to limit the data you receive use `get_data_page` instead.

        :param pipeline_runs: The pipeline runs to include in the raw data. If not provided, all
            the pipeline runs used to get the report will be included.

        :returns: The dataframe holding all the report data.
        """
        pipeline_run_ids = convert_pipeline_runs_to_ids(
            self.configuration.pipeline_run_ids, pipeline_runs
        )
        offset = 0

        df, pagination_response = await _get_dataframe_and_pagination_response(
            pipeline_run_ids, PaginationParameters(offset=offset)
        )

        offset += pagination_response.limit
        total_number_of_items = pagination_response.total_number_of_items

        while offset < total_number_of_items:
            new_df, pagination_response = await _get_dataframe_and_pagination_response(
                pipeline_run_ids, PaginationParameters(offset=offset)
            )

            df = concat([df, new_df], axis=0, ignore_index=True)
            offset += pagination_response.limit
        return df


async def _get_dataframe_and_pagination_response(
    pipeline_run_ids: List[int], pagination_parameters: PaginationParameters
) -> Tuple[DataFrame, PaginationResponse]:
    api_service = get_api_client()
    report_data_response = await ReportAPI(api_service).get_report_data(
        pipeline_run_ids, pagination_parameters=pagination_parameters
    )

    return (
        DataFrame.from_records(report_data_response.dict()["items"]),
        report_data_response.filter.pagination,
    )
