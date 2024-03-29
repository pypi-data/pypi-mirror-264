from typing import List, Optional

from aidkit_client._endpoints.constants import Constants
from aidkit_client._endpoints.models import (
    ListAggregatedAugmentationExampleTableDataResponse,
    ListAugmentedObservationInformationResponse,
    ReportAdversarialResponse,
    ReportCoreMethodOutputDetailResponse,
    ReportCorruptionResponse,
    ReportDataResponse,
    ReportResponse,
    ReportWithInferenceRequest,
)
from aidkit_client._endpoints.pagination import PaginationParameters
from aidkit_client.aidkit_api import HTTPService


class ReportAPI:
    api: HTTPService

    def __init__(self, api: HTTPService):
        self.api = api

    async def get_report(self, pipeline_run_ids: List[int]) -> ReportResponse:
        result = await self.api.post_json(
            path=f"{Constants.REPORT_PATH}",
            parameters=None,
            body={"pipeline_run_ids": pipeline_run_ids},
        )

        return ReportResponse(
            **result.body_dict_or_error(
                f"Error fetching Report for pipeline runs '{pipeline_run_ids}'."
            )
        )

    async def get_augmented_observation_information(
        self,
        pipeline_run_ids: List[int],
        pagination_parameters: Optional[PaginationParameters] = None,
    ) -> ListAugmentedObservationInformationResponse:
        result = await self.api.post_json(
            path=f"{Constants.REPORT_PATH}/augmented_observations",
            parameters=pagination_parameters.dict() if pagination_parameters else None,
            body={"pipeline_run_ids": pipeline_run_ids},
        )

        return ListAugmentedObservationInformationResponse(
            **result.body_dict_or_error(
                f"Error fetching Report for pipeline runs '{pipeline_run_ids}'."
            )
        )

    async def get_report_data(
        self,
        pipeline_run_ids: List[int],
        pagination_parameters: Optional[PaginationParameters] = None,
    ) -> ReportDataResponse:
        result = await self.api.post_json(
            path=f"{Constants.REPORT_PATH}/data",
            parameters=pagination_parameters.dict() if pagination_parameters else None,
            body={"pipeline_run_ids": pipeline_run_ids},
        )

        return ReportDataResponse(
            **result.body_dict_or_error(
                f"Error fetching Report for pipeline runs '{pipeline_run_ids}'."
            )
        )

    async def get_augmentation_example_table_data(
        self,
        pipeline_run_ids: List[int],
        method_name: str,
        method_configuration_parameters_strings: List[str],
        number_of_observations: int,
    ) -> ListAggregatedAugmentationExampleTableDataResponse:
        table_data_response = await self.api.post_json(
            path=f"{Constants.REPORT_PATH}/augmentation_examples_table_data",
            parameters=None,
            body={
                "pipeline_run_ids": pipeline_run_ids,
                "method_name": method_name,
                "method_configuration_parameters_strings": method_configuration_parameters_strings,
                "number_of_observations": number_of_observations,
            },
        )
        return ListAggregatedAugmentationExampleTableDataResponse(
            **table_data_response.body_dict_or_error(
                f"Error fetching Augmentation example data for pipeline runs '{pipeline_run_ids}'."
            )
        )

    async def get_corruption_report(
        self, request: ReportWithInferenceRequest
    ) -> ReportCorruptionResponse:
        result = await self.api.post_json(
            path=f"{Constants.REPORT_PATH}/corruptions",
            parameters=None,
            body=request.dict(),
        )
        return ReportCorruptionResponse(
            **result.body_dict_or_error(
                f"Error fetching Corruption Report for model '{request.model}'."
            )
        )

    async def get_adversarial_report(
        self, request: ReportWithInferenceRequest
    ) -> ReportAdversarialResponse:
        result = await self.api.post_json(
            path=f"{Constants.REPORT_PATH}/adversarial_examples",
            parameters=None,
            body=request.dict(),
        )
        return ReportAdversarialResponse(
            **result.body_dict_or_error(
                f"Error fetching Adversarial Report for model '{request.model}'."
            )
        )

    async def get_perturbed_observation_details(
        self, perturbed_observation_id: int
    ) -> ReportCoreMethodOutputDetailResponse:
        result = await self.api.get(
            path=f"{Constants.REPORT_PATH}/artifact_details/{perturbed_observation_id}",
            parameters=None,
        )
        return ReportCoreMethodOutputDetailResponse(
            **result.body_dict_or_error(
                f"Error fetching inference results for remote file '{perturbed_observation_id}'."
            )
        )
