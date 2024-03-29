"""
Module to implement the Augmentation Examples Table.
"""

import base64
import io
import json
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import pandas as pd
from aidkit_client._endpoints.models import (
    AggregatedAugmentationExampleTableDataResponse,
    ListAggregatedAugmentationExampleTableDataResponse,
)
from aidkit_client.resources.report import ReportConfiguration
from aidkit_client.resources.report.tables.report_table import TableColor
from pandas.io.formats.style import Styler  # type: ignore[import-untyped]
from pandas.io.formats.style_render import CSSDict  # type: ignore[import-untyped]
from PIL import Image as PILImage
from tabulate import tabulate

DOWNARROW = "&darr;"


class AugmentationExamplesTable:
    """
    Table displaying examples of an augmentation method output.
    """

    example_data: List[AggregatedAugmentationExampleTableDataResponse]
    report_configuration: ReportConfiguration
    dataframe: pd.DataFrame

    def __init__(
        self,
        example_data: ListAggregatedAugmentationExampleTableDataResponse,
        report_configuration: ReportConfiguration,
        number_of_example_augmentations: int = 3,
        number_of_example_observations: int = 3,
        thumbnail_width_height: Tuple[int, int] = (400, 200),
    ) -> None:
        self.report_configuration = report_configuration

        self.example_data = example_data.items
        self.dataframe = self._get_display_dataframe()
        self.thumbnail_width_height = thumbnail_width_height

        self.number_of_example_augmentations = min(
            number_of_example_augmentations,
            len(self.example_data[0].augmented_observations),
        )
        self.number_of_example_observations = number_of_example_observations

    def _get_display_dataframe(self) -> pd.DataFrame:
        """
        Compute the augmentation examples table from the report dataframe. This
        table contains the observation IDs, the model failure rates for each
        error mode, and the augmentation IDs including intensity parameters.

        :returns: A dataframe containing the computed data.
        """
        observations_records: List[Dict[str, str]] = [data.dict() for data in self.example_data]
        augmentation_records: List[List[Dict[str, Union[str, int]]]] = []
        for obs in self.example_data:
            augmentation_record: List[Dict[str, Union[str, int]]] = []
            for augmented_observation in obs.augmented_observations:
                displayed_params: Dict[str, Union[str, int]] = {
                    "augmentation_id": augmented_observation.augmented_observation_id,
                    "augmentation_url": augmented_observation.augmented_observation_url,
                    **augmented_observation.sampled_parameters,
                }
                augmentation_record.append(displayed_params)
            augmentation_records.append(augmentation_record)

        max_augmentations = max(
            len(augmentation_record) for augmentation_record in augmentation_records
        )
        for i, record in enumerate(augmentation_records):
            augmentation_records[i] = record + ([{}] * (max_augmentations - len(record)))

        return pd.concat(
            {
                "": pd.DataFrame(
                    columns=["Original Frame ID", "Original Frame"],
                    data=[
                        [observation["observation_id"], observation]
                        for observation in observations_records
                    ],
                ).set_index("Original Frame ID"),
                "Augmented Frames": pd.DataFrame(
                    columns=[
                        "Original Frame ID",
                        *[str(i) for i in range(max_augmentations)],
                    ],
                    data=[
                        [observation["observation_id"], *augmentations_row]
                        for observation, augmentations_row in zip(
                            observations_records, augmentation_records
                        )
                    ],
                ).set_index("Original Frame ID"),
            },
            axis=1,
        ).reset_index(drop=True)

    @staticmethod
    def _get_caption(
        table_name: str,
        table_description: str,
        report_information: Optional[List[Tuple[str, str]]] = None,
    ) -> str:
        """
        Generate a caption for a table.

        :param table_name: Name of the table.
        :param table_description: Description of the table.
        :param report_information: Additional information to display.
        :return: Formatted caption for the table.
        """
        info_table = ""
        if report_information:
            info_table = tabulate(report_information, tablefmt="html")

        return f"""
        <div style="font-size: 0.9em">
        <h3>{table_name}</h3>
        <p>{table_description}</p>
        {info_table}
        </div>
        """

    def _style_table(
        self,
        styler: Styler,
        dark_mode: bool,
    ) -> Styler:
        """
        Function to style the augmentation examples table.

        :param styler: Styler object of the DataFrame to be styled.
        :param dark_mode: Boolean to indicate whether the user has their system in
            dark mode or not.
        :return: Styled Styler object.
        """
        if dark_mode:
            title_color = TableColor.WHITE.value
            background_color = TableColor.BLACK.value
            row_color = TableColor.GRAY.value
            cell_font_color = TableColor.DARK_GRAY.value
        else:
            title_color = TableColor.BLACK.value
            background_color = TableColor.WHITE.value
            row_color = TableColor.LIGHT_GRAY.value
            cell_font_color = TableColor.DARK_GRAY.value

        def encode_image_in_base64(image_path: str) -> str:
            """
            Read an image from bytes and encodes it as base64.

            :param image_path: Path of the image to display.
            :return: image representation as base64 string
            """
            image_bytes = self.downloaded_images[image_path]
            image_buffer = io.BytesIO(image_bytes)
            image = PILImage.open(image_buffer)

            with io.BytesIO() as buffer:
                image.save(buffer, "jpeg")
                encoded_image = base64.b64encode(buffer.getvalue()).decode()

                return encoded_image

        def original_image_formatter(observation: dict) -> str:
            """
            Custom HTML formatter replacing an image frame ID with the
            corresponding image.

            :param observation: observation object as dict
            :return: view representation as html text
            """
            image_path = observation["observation_url"]
            configuration_name = self.report_configuration.method_configuration_names[
                observation["method_name"]
            ][observation["method_configuration_parameters_string"]]
            configuration_parameters = json.loads(
                observation["method_configuration_parameters_string"]
            )
            caption = [("Configuration name", str(configuration_name))] + [
                (configuration_param, f"{param_val}")
                for configuration_param, param_val in configuration_parameters.items()
            ]
            detail_info_html = [
                f"""
                    <div style="display: flex; flex-direction: row;
                    justify-content: space-between; padding: 0 0 5 0px;">
                    <p style="margin: 0; color: {cell_font_color}; text-align: start;
                    text-transform: uppercase;">{caption_detail[0]}</p>
                    <p style="margin: 0; color: {title_color};">{caption_detail[1]}</p>
                    </div>
                """
                for caption_detail in caption
            ]
            base64_image = encode_image_in_base64(image_path=image_path)
            flex_view_html = f"""
                    <div style = "display: flex; flex-direction: column; max-width: 400pt;">
                    <div style="display: flex; flex-direction: row; align-content: center;">
                        <figure style="margin: 40 0 10 0px; width:100%; ">
                            <img style="border-radius: 0.5rem;"
                            src="data:image/jpeg;base64,{base64_image}" title="ID={observation['observation_id']}">
                        </figure>
                    </div>
                    <div style="display: flex; flex-direction: row;
                        justify-content: space-between;padding: 0 0 10 0px;">
                        <p style="margin: 0; text-transform: uppercase;">Original Frame ID</p>
                        <p style="margin: 0; color: {title_color};">{observation['observation_id']}</p>
                    </div>
                    {"".join(detail_info_html)}
                    </div>
            """
            return flex_view_html

        def augmentation_formatter(augmentation: object) -> str:
            """
            Custom HTML formatter replacing multiple augmentation IDs with the
            corresponding images, adding captions to them.

            :param augmentation: augmentation object as dict
            :return: view representation as html text
            """
            if not isinstance(augmentation, dict):
                return str(augmentation)
            image_path = augmentation["augmentation_url"]
            caption = [("Augmentation ID", augmentation["augmentation_id"])] + [
                (augmentation_param, f"{param_val:.3f}")
                for augmentation_param, param_val in augmentation.items()
                if augmentation_param not in {"augmentation_id", "augmentation_url"}
            ]
            base64_image = encode_image_in_base64(image_path=image_path)
            detail_info_html = [
                f"""
                    <div style="display: flex; flex-direction: row;
                    justify-content: space-between; padding: 0 0 5 0px;">
                    <p style="margin: 0; color: {cell_font_color}; text-align: start;
                    text-transform: uppercase;">{caption_detail[0]}</p>
                    <p style="margin: 0; color: {title_color};">{caption_detail[1]}</p>
                    </div>
                """
                for caption_detail in caption
            ]
            flex_view_html = f"""
                        <div style = "display: flex; flex-direction: column; max-width: 400pt;
                        width: 90%; margin: auto; padding: 10 0 0 0px;">
                        <div style="display: flex; flex-direction: row; align-content: center;">
                            <figure style="margin: 40 0 10 0px; width:100%">
                                <img style="border-radius: 0.5rem;
                                " src="data:image/jpeg;base64,{base64_image}"">
                            </figure>
                        </div>
                            {"".join(detail_info_html)}
                        </div>

                """
            return flex_view_html

        def merged_cell_formatter(row: object) -> str:
            """
            Custom HTML formatter handling the display of the original observation

            :param row: dataframe merged-row object
            :return: view representation as html text
            """
            if not isinstance(row, list):
                return str(row)
            image_html = original_image_formatter(row[0])
            cell_html = f"""
                     <div style="
                            width: 100%;
                            padding: 10 0 40 0px;"
                            >
                    <div style="
                            width: 90%;
                            margin: auto;
                            display: flex;
                            flex-direction: column;
                            padding: 0 0 10 0px;
                            gap: 5px;"
                            >
                       {image_html}
                       <div style="min-height: 10px;"/>
                    </div>
                    </div>
                    """
            return cell_html

        cell_css: CSSDict = {
            "selector": "td",
            "props": f"vertical-align: top; color: {cell_font_color}; " "font-weight: normal;",
        }
        cells_without_spacing_css: CSSDict = {
            "selector": "tr, td",
            "props": "margin: 10px; padding: 0px; border: 0;",
        }
        col_headers_lvl0_css: CSSDict = {
            "selector": ".col_heading:not(:first-child)",
            "props": f"background-color: {background_color}; "
            "color: {title_color}; text-align: center;",
        }
        col_headers_line_css: CSSDict = {
            "selector": ".col_heading.level0",
            "props": "border-top: 2px solid #A7B9D1 !important; padding: 5 0 5 0px;",
        }
        first_cell_main_background_css: CSSDict = {
            "selector": "td:first-child, th:first-child",
            "props": f"background-color: {row_color}; ",
        }
        other_cell_main_background_css: CSSDict = {
            "selector": "td:not(:first-child)",
            "props": f"background-color: {background_color}; ",
        }
        caption_css: CSSDict = {
            "selector": "caption",
            "props": "caption-side: bottom; font-size:1.25em; "
            "text-align: left; padding-top: 10px;",
        }
        styler.set_table_styles(
            [
                col_headers_lvl0_css,
                col_headers_line_css,
                cell_css,
                caption_css,
                first_cell_main_background_css,
                other_cell_main_background_css,
                cells_without_spacing_css,
            ],
            overwrite=False,
        )
        styler.set_table_attributes(
            'style="border-collapse: collapse !important;border-spacing: 0;'
            ' width: 100%; table-layout: fixed; overflow-wrap: break-word;"'
        )

        styler.hide(axis="index")

        styler.relabel_index(
            [""] + ["Augmented Frames"] * self.number_of_example_augmentations,
            axis=1,
            level=0,
        )

        formatters: Dict[Any, Union[str, Callable[[dict], str], None]] = {}
        for i in range(self.number_of_example_augmentations):
            formatters[("Augmented Frames", str(i))] = augmentation_formatter
        formatters[("merged_columns", "")] = merged_cell_formatter
        styler.format(
            formatters,
            escape="html",
        )

        caption = self._get_caption(
            table_name="Augmentation examples",
            table_description=(
                "This table displays a selection of observations and shows the result of the "
                "augmentation method applied on them. The configuration parameters of the "
                "augmentation are listed in the first column. The parameters sampled randomly are "
                "listed below each augmented observation."
            ),
        )

        styler.set_caption(caption=caption)
        return styler

    def render(
        self,
        images: Dict[str, bytes],
        dark_mode: Optional[bool] = True,
    ) -> Styler:
        """
        Display the model error rate for different ODD tags and error modes.

        :param images: Dictionary mapping the url of images to display to the actual image in bytes.
        :param dark_mode: Boolean to indicate whether the user has their system in
            dark mode or not, default is True.
        :return: augmentation example table as a pandas Styler
        """
        dataframe = self.dataframe.reset_index(drop=True)
        self.downloaded_images = images
        dataframe.drop(
            labels=[
                ("Augmented Frames", f"{i}")
                for i in range(
                    self.number_of_example_augmentations,
                    len(self.example_data[0].augmented_observations),
                )
            ],
            axis=1,
            inplace=True,
        )

        dataframe["merged_columns"] = dataframe.apply(
            lambda row: [row[0]],
            axis=1,
        )
        dataframe.insert(0, ("merged_columns"), dataframe.pop("merged_columns"))

        dataframe.drop(
            labels=[("", "Original Frame")],
            axis=1,
            inplace=True,
        )

        styled_df: Styler = dataframe.style.pipe(
            self._style_table,
            dark_mode=dark_mode,
        )
        return styled_df
