import data
import pandas as pd

from pathlib import Path
from typing import Optional


class Analyser:
    """
    Base class for all data analysers.

    Args:
        input_csv: The path to the CSV file containing the output of the
            Instron.
        output_xlsx: The path to the Excel file which will contain the analysis
            results.
        summary: The summary of the analysis.
    """

    def __init__(
        self, input_csv: Path, output_xlsx: Path, summary: data.Summary
    ) -> None:

        self._processed_data: list[data.ProcessedData] = []
        self._summary: data.Summary

        self.output_xlsx: Path = output_xlsx
        self.raw_data: data.RawData = data.RawData(input_csv)
        self.processed_data = []
        self.summary = summary

    @property
    def processed_data(self) -> list[data.ProcessedData]:
        return self._processed_data

    @processed_data.setter
    def processed_data(self, value: list[data.ProcessedData]) -> None:
        self._processed_data = value

    @property
    def summary(self) -> data.Summary:
        return self._summary

    @summary.setter
    def summary(self, value: data.Summary) -> None:
        self._summary = value

    def analyse(self) -> None:
        """
        Analyses the processed data.
        """

        pass

    def save(self) -> None:
        """
        Saves the analysis results as well as the raw and processed data to an
        Excel file.
        """

        with pd.ExcelWriter(self.output_xlsx, engine="xlsxwriter") as writer:
            # Save the raw data
            self.raw_data.write_to_excel(writer)

            # Save all the processed data
            for d in self.processed_data:
                d.write_to_excel(writer)

            # Save the analysis summary
            self.summary.write_to_excel(writer)


class RelaxationAnalyser(Analyser):
    """
    The analyser used to analyse the Instron output for the relaxation stress
    test.

    Args:
        input_csv: The path to the CSV file containing the output of the
            Instron.
        output_xlsx: The path to the Excel file which will contain the analysis
            results.
        relaxation_intervals: The number of relaxation intervals within the raw
            data to include in the analysis.  This is used in combination with
            relaxation_step_pct to determine the relaxation strains to include
            in the analysis.  For instance, for relaxation_intervals = 6 and
            relaxation_step_pct = 5, the analysis will include the strains
            [5, 10, 15, 20, 25, 30].
        relaxation_step_pct: The difference between consecutive relaxation
            strains to use in the analysis.  This is used in combination with
            relaxation_intervals to determine the relaxation strains to include
            in the analysis.  For instance, for relaxation_intervals = 6 and
            relaxation_step_pct = 5, the analysis will include the strains
            [5, 10, 15, 20, 25, 30].
        epsilon_pct: Tolerance for the strain within which it is considered to
            be maintained for each relaxation interval.
        regression_data_points: Maximum number of data points to be included in
            the regression analysis.
    """

    def __init__(
        self,
        input_csv: Path,
        output_xlsx: Path,
        relaxation_intervals: int = 6,
        relaxation_step_pct: float = 5.0,
        epsilon_pct: float = 0.01,
        regression_data_points: Optional[int] = None,
    ) -> None:

        super().__init__(input_csv, output_xlsx, data.RelaxationSummary())

        self._relaxation_intervals: int = 0
        self._relaxation_step_pct: float = 0.0
        self._relaxation_strains_pct: list[float] = []

        self.relaxation_intervals = relaxation_intervals
        self.relaxation_step_pct = relaxation_step_pct
        self.epsilon_pct: float = epsilon_pct
        self.regression_data_points: Optional[int] = regression_data_points

    def __str__(self) -> str:

        summary = f"{self.output_xlsx.name}\n"
        summary += "Equation: F = a * e^(-t/tau) + b\n"
        summary += "\n"

        for i in range(self.relaxation_intervals):
            summary += f"Strain (%) = {self.relaxation_strains_pct[i]}\n"
            summary += f" - a   = {self.processed_data[i].a}\n"
            summary += f" - b   = {self.processed_data[i].b}\n"
            summary += f" - tau = {self.processed_data[i].tau}\n"

        summary += "\n"

        return summary

    @property
    def processed_data(self) -> list[data.RelaxationData]:  # type: ignore
        return super().processed_data  # type: ignore

    @processed_data.setter
    def processed_data(self, value: list[data.RelaxationData]) -> None:  # type: ignore
        super().processed_data[:] = value

    @property
    def relaxation_intervals(self) -> int:
        return self._relaxation_intervals

    @relaxation_intervals.setter
    def relaxation_intervals(self, value: int) -> None:
        self._relaxation_intervals = value

        # Resize the relaxation strains based on the required number of relaxation
        # intervals
        if len(self._relaxation_strains_pct) > self._relaxation_intervals:
            del self._relaxation_strains_pct[self._relaxation_intervals :]
        else:
            offset_pct: float = (
                self._relaxation_strains_pct[-1]
                if len(self._relaxation_strains_pct) > 0
                else 0
            )
            self._relaxation_strains_pct.extend(
                [
                    (i + 1) * self._relaxation_step_pct + offset_pct
                    for i in range(
                        self._relaxation_intervals - len(self._relaxation_strains_pct)
                    )
                ]
            )

        # Resize the relaxation data based on the required number of relaxation
        # intervals
        if len(self.processed_data) > self._relaxation_intervals:
            del self.processed_data[self._relaxation_intervals :]
        else:
            self.processed_data.extend(
                [
                    data.RelaxationData(self.raw_data.raw_data_frame)
                    for _ in range(
                        self._relaxation_intervals - len(self.processed_data)
                    )
                ]
            )

    @property
    def relaxation_step_pct(self) -> float:
        return self._relaxation_step_pct

    @relaxation_step_pct.setter
    def relaxation_step_pct(self, value: float) -> None:
        self._relaxation_step_pct = value

        self._relaxation_strains_pct = [
            (i + 1) * self._relaxation_step_pct
            for i in range(self._relaxation_intervals)
        ]

    @property
    def relaxation_strains_pct(self) -> list[float]:
        return self._relaxation_strains_pct

    @property
    def summary(self) -> data.RelaxationSummary:
        return super().summary  # type: ignore

    @summary.setter
    def summary(self, value: data.RelaxationSummary) -> None:  # type: ignore
        Analyser.summary = value

    def analyse(self) -> None:
        """
        Analyses the processed data.
        """

        self.summary.clear_all_rows()

        for i in range(self.relaxation_intervals):
            self.processed_data[i].process_raw_data(
                self.relaxation_strains_pct[i],
                self.epsilon_pct,
                self.regression_data_points,
            )

            self.summary.append_row(
                self.relaxation_strains_pct[i],
                self.processed_data[i].min_force_N,
                self.processed_data[i].max_force_N,
                self.processed_data[i].min_stress_MPa,
                self.processed_data[i].max_stress_MPa,
                self.processed_data[i].min_e_modulus_MPa,
                self.processed_data[i].max_e_modulus_MPa,
                self.processed_data[i].a,
                self.processed_data[i].b,
                self.processed_data[i].tau,
            )


class FailureAnalyser(Analyser):
    """
    The analyser used to analyse the Instron output for the compression to
    failure test.

    Args:
        input_csv: The path to the CSV file containing the output of the
            Instron.
        output_xlsx: The path to the Excel file which will contain the analysis
            results.
        abort_strain_pct: The strain threshold at which the test is considered
            to be aborted.
        toughness_strain_pct: The strain at which the toughness is calculated.
        stiffness_strain_pct: The strain at which the stiffness is calculated.
    """

    def __init__(
        self,
        input_csv: Path,
        output_xlsx: Path,
        abort_strain_pct: float,
        toughness_strain_pct: float,
        stiffness_strain_pct: float,
    ) -> None:

        super().__init__(input_csv, output_xlsx, data.FailureSummary())

        self.abort_strain_pct: float = abort_strain_pct
        self.toughness_strain_pct: float = toughness_strain_pct
        self.stiffness_strain_pct: float = stiffness_strain_pct

        self.processed_data.append(data.FailureData(self.raw_data.raw_data_frame))

    def __str__(self) -> str:

        # TODO
        return super().__str__()

    @property
    def processed_data(self) -> list[data.FailureData]:  # type: ignore
        return super().processed_data  # type: ignore

    @processed_data.setter
    def processed_data(self, value: list[data.FailureData]) -> None:  # type: ignore
        super().processed_data[:] = value

    @property
    def summary(self) -> data.FailureSummary:
        return super().summary  # type: ignore

    @summary.setter
    def summary(self, value: data.FailureSummary) -> None:  # type: ignore
        Analyser.summary = value

    def analyse(self) -> None:
        """
        Analyses the processed data.
        """

        self.summary.clear_all_rows()

        self.processed_data[0].process_raw_data(
            self.abort_strain_pct, self.toughness_strain_pct, self.stiffness_strain_pct
        )

        self.summary.append_row(
            self.processed_data[0].ultimate_strain_pct,
            self.processed_data[0].ultimate_force_N,
            self.processed_data[0].ultimate_strength_MPa,
            self.processed_data[0].aborted,
            self.processed_data[0].slipped,
            self.processed_data[0].yield_strain_pct,
            self.processed_data[0].yield_force_N,
            self.processed_data[0].yield_strength_MPa,
            self.processed_data[0].toughness_strain_pct,
            self.processed_data[0].toughness_MPa,
            self.processed_data[0].stiffness_strain_pct,
            self.processed_data[0].stiffness_MPa,
        )
