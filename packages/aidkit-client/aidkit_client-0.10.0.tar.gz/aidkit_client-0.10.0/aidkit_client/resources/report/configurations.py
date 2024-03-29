from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

MethodName = str
ConfigurationName = str
MethodConfigurationParameterString = str


@dataclass(frozen=True)
class MethodConfiguration:
    """
    Information about a particular augmentation method configuration. This includes the configured
    parameters for the method, the number of augmentations per frames produced by this method as
    well as the ranges for the method parameters sampled randomly.
    """

    parameters: Dict[str, Any]
    augmentations_per_frame: int
    sampled_parameters_ranges: Dict[str, Tuple[float, float]]


@dataclass(frozen=True)
class ReportConfiguration:
    """
    Configuration parameters and general information about the report retrieved.
    """

    pipeline_run_ids: List[int]
    dataset_name: str
    subset_name: str
    number_of_frames: int
    odd_tags: Dict[int, List[str]]
    method_configurations: Dict[MethodName, Dict[ConfigurationName, MethodConfiguration]]
    method_configuration_names: Dict[
        MethodName, Dict[MethodConfigurationParameterString, ConfigurationName]
    ]

    def get_number_of_augmented_frames(self) -> int:
        """
        Get the total number of augmented frames in the pipeline. The total number of augmented
        frames is the number of original frames times the number of augmentations per frame.
        :return: Total number of augmented frames.
        """
        total_number_of_augmentations_per_frame = 0
        for configuration in self.method_configurations.values():
            for parameter in configuration.values():
                total_number_of_augmentations_per_frame += parameter.augmentations_per_frame
        return self.number_of_frames * total_number_of_augmentations_per_frame
