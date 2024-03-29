"""
Table containing a summary of the report information.
"""

from collections import Counter
from dataclasses import dataclass
from itertools import chain
from typing import Dict, List, Optional, Tuple, Union

from aidkit_client.resources.report import (
    MethodConfiguration,
    ReportConfiguration,
)
from aidkit_client.resources.report.configurations import MethodName
from aidkit_client.resources.report.tables.report_table import TableColor
from IPython.display import HTML  # type: ignore[import-untyped]
from tabulate import tabulate


class MethodConfigurationData:
    """
    Aggregates data from a MethodConfiguration instance in a way that suits the summary table.
    """

    name: MethodName
    number_of_variations: int
    sampled_parameters: Dict[str, Tuple[float, float]]
    configuration_parameters: Dict[str, str]

    def __init__(self, name: str, method_configuration: MethodConfiguration):
        self.name = name
        self.number_of_variations = method_configuration.augmentations_per_frame
        self.sampled_parameters = method_configuration.sampled_parameters_ranges
        self.configuration_parameters = {
            key: str(round(value, 2)) if isinstance(value, float) else str(value)
            for key, value in method_configuration.parameters.items()
        }


@dataclass
class SummaryTableData:
    """
    Aggregates data from a ReportConfiguration instance in a way that suits the summary table.
    """

    dataset: str
    subset: str
    augmentation_types: List[str]
    number_of_augmentation_types: int
    number_of_original_frames: int
    number_of_augmented_frames: int
    odd_tag_count: Counter
    method_configurations: List[MethodConfigurationData]

    @staticmethod
    def _get_method_configuration_data(
        report_configuration: ReportConfiguration,
    ) -> List[MethodConfigurationData]:
        """
        Extract the method configuration data from a report configuration object.
        If a method (such as Lens Flare or Fog) contains more than one configuration,
        the method configuration name is the method name with the configuration name
        in parentheses. If a method has only one configuration, the method configuration
        name is the method name.

        :param report_configuration: A report configuration object to extract the method
            configurations from.
        :return: A list of the method configurations.
        """
        method_configurations = []
        for (
            method_name,
            configuration_dict,
        ) in report_configuration.method_configurations.items():
            for configuration_name, parameters in configuration_dict.items():
                if len(configuration_dict) > 1:
                    name = f"{method_name} ({configuration_name})"
                else:
                    name = method_name
                method_configurations.append(MethodConfigurationData(name, parameters))
        return method_configurations


class SummaryTable:
    """
    Renders and displays a summary table.
    """

    data: SummaryTableData

    def __init__(self, report_configuration: ReportConfiguration):
        self.data = SummaryTableData(
            dataset=report_configuration.dataset_name,
            subset=report_configuration.subset_name,
            augmentation_types=list(report_configuration.method_configurations.keys()),
            number_of_augmentation_types=len(report_configuration.method_configurations),
            number_of_original_frames=report_configuration.number_of_frames,
            number_of_augmented_frames=(report_configuration.get_number_of_augmented_frames()),
            odd_tag_count=Counter(chain(*report_configuration.odd_tags.values())),
            method_configurations=SummaryTableData._get_method_configuration_data(
                report_configuration
            ),
        )

    def render(
        self,
        selected_augmentation: Optional[str] = None,
        as_html: bool = True,
        dark_mode: bool = True,
    ) -> Union[HTML, str]:
        """
        Computes the report summary and displays the output tables. Note that
        display of HTML tables outside jupyter notebook environments may
        result in undesirable behavior.

        :param selected_augmentation: If provided, render only information about the chosen
            augmentation.
        :param as_html: If true, render a table in HTML format instead of ASCII.
        :param dark_mode: Render HTML tables in dark mode.
        :return: The table as an HTML or ASCII string.
        """
        pipeline_table = self._render_pipeline_table(as_html=as_html)
        odd_table = self._render_odd_table(as_html=as_html)
        method_table = self._render_method_table(
            selected_augmentation=selected_augmentation, as_html=as_html
        )

        if as_html:
            if dark_mode:
                title_color = TableColor.WHITE.value
                background_color = TableColor.BLACK.value
                row_color = TableColor.GRAY.value
                cell_font_color = TableColor.DARK_GRAY.value
            else:
                title_color = TableColor.BLACK.value
                background_color = TableColor.WHITE.value
                row_color = TableColor.GRAY.value
                cell_font_color = TableColor.DARK_GRAY.value
            return HTML(
                f"""
                <style>
                    ._data_summary table {{
                        margin-bottom: 20px;
                    }}
                    ._data_summary table tr:nth-child(odd) {{
                        background-color: {row_color};
                    }}
                    ._data_summary table tr:nth-child(even) {{
                        background-color: {background_color};
                    }}
                    ._data_summary table th {{
                        color: {title_color};
                        text-align: center;
                        font-weight: bold;
                        background-color: {background_color};
                        border-top: 2px solid #A7B9D1 !important;
                    }}
                    ._data_summary table td:nth-child(even) {{
                        color: {cell_font_color};
                    }}
                    ._data_summary table td:nth-child(odd) {{
                        color: {title_color};
                    }}
                </style>
                <div class="_data_summary">{pipeline_table}</div>
                <div class="_data_summary">{odd_table}</div>
                <div class="_data_summary">{method_table}</div>
                """
            )

        return "\n\n".join((pipeline_table, odd_table, method_table))

    def _render_pipeline_table(self, as_html: bool = True) -> str:
        table_source = [
            [
                "# of Augmentation Types",
                self.data.number_of_augmentation_types,
                "Original Frames",
                self.data.number_of_original_frames,
            ],
            [
                "Augmented Frames",
                self.data.number_of_augmented_frames,
            ],
        ]
        augmentation_types = "Augmentation Types Applied: " + ", ".join(
            configuration.name for configuration in self.data.method_configurations
        )

        if as_html:
            table = str(tabulate(table_source, tablefmt="html"))
            table = table.replace("<td>", '<td style="text-align: left;">')
            augmentation_types_tag = (
                '<tr><td colspan="4" style="text-align: left;">' + augmentation_types + "</td></tr>"
            )
            tbody_close_index = table.index("</tbody>")
            table = table[:tbody_close_index] + augmentation_types_tag + table[tbody_close_index:]
        else:
            table = tabulate(table_source, tablefmt="simple")
            table += "\n" + augmentation_types + "\n"
            table += "-" * _longest_line_length(table)
        return table

    def _render_odd_table(self, as_html: bool = True) -> str:
        table = tabulate(
            [(tag, count) for tag, count in self.data.odd_tag_count.items()],
            headers=["ODD Tag", "Tag Count"],
            tablefmt="html" if as_html else "simple",
        )
        if as_html:
            table = str(table.replace("<td>", '<td style="text-align: left;">'))
        return table

    def _render_method_table(
        self, as_html: bool = True, selected_augmentation: Optional[str] = None
    ) -> str:
        if selected_augmentation is None:
            configurations = self.data.method_configurations
        else:
            configurations = [
                configuration
                for configuration in self.data.method_configurations
                if configuration.name == selected_augmentation
            ]
            if not configurations:
                raise ValueError(f"Augmentation {selected_augmentation} not found in report data.")

        table = ""
        for configuration in configurations:
            if selected_augmentation is not None and selected_augmentation != configuration.name:
                continue

            header = f"{configuration.name} Configuration:"
            sub_header = f"{configuration.number_of_variations} variation"
            if configuration.number_of_variations > 1:
                sub_header += "s, sampled uniformly"

            sampled_parameter_table = ""
            if configuration.sampled_parameters:
                sampled_parameter_table_source = [
                    (
                        parameter,
                        f"min: {round(min_, 2)}, max: {round(max_, 2)}",
                    )
                    for parameter, (
                        min_,
                        max_,
                    ) in configuration.sampled_parameters.items()
                ]
                sampled_parameter_table = tabulate(
                    sampled_parameter_table_source,
                    headers=["Sampled Parameter", "Range"],
                    tablefmt="html" if as_html else "simple",
                )

            fixed_parameter_table = ""
            if configuration.configuration_parameters:
                fixed_parameter_table_source = [
                    (parameter_name, parameter_value)
                    for parameter_name, parameter_value in configuration.configuration_parameters.items()
                ]
                fixed_parameter_table = tabulate(
                    fixed_parameter_table_source,
                    headers=["Fixed Parameter", "Value"],
                    tablefmt="html" if as_html else "simple",
                )

            if as_html:
                table += f"<h3>{header}</h3>"
                table += f"<p>{sub_header}</p>"
                if sampled_parameter_table and fixed_parameter_table:
                    table += sampled_parameter_table.replace("</table>", "")
                    table += fixed_parameter_table.replace("<table>", "")
                else:
                    table += sampled_parameter_table
                    table += fixed_parameter_table
                table = table.replace("<td>", '<td style="text-align: left;">')
                table = table.replace("<th>", '<th style="text-align: left;">')
            else:
                divider_1 = (
                    "\n"
                    + "-"
                    * _longest_line_length(f"{sampled_parameter_table}\n{fixed_parameter_table}")
                    + "\n"
                )
                divider_2 = divider_1 if sampled_parameter_table and fixed_parameter_table else ""
                table += f"{header}\n{sub_header}{divider_1}{sampled_parameter_table}{divider_2}{fixed_parameter_table}\n\n"
        return table


def _longest_line_length(string: str) -> int:
    return max(len(line) for line in string.split("\n"))
