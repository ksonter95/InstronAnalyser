import csv
import dataclasses
from typing import Optional, cast
import mech_analyser.experiment.analyser as ma_analyser
import mech_analyser.experiment.instron_68tm.data as ma_data
import mech_analyser.experiment.instron_68tm.phase as ma_phase

from pathlib import Path


@dataclasses.dataclass
class Parameters(ma_analyser.Parameters):
    """
    Parameters of an Instron 68TM experiment.

    Args:
        tare_force_N: The force which will be used to tare the experiment.  All
            raw data points with force less than the tare force will be
            discarded, and all data points with force greater than the tare
            force will be offset accordingly.
        properties_file: The path to the properties file containing the cross-sectional
            area and initial length of the sample.
        cross_sectional_area_m2: The cross-sectional surface area of the sample.
        initial_length_m: The initial length of the sample.
    """

    tare_force_N: float = 0.0
    properties_file: Optional[Path] = None
    cross_sectional_area_m2: Optional[float] = None
    initial_length_m: Optional[float] = None

    def calculate_sample_parameters(self, name: str) -> None:
        """
        Calculates the sample parameters from the properties file if it is set.

        Args:
            name: The name of the sample.

        Raises:
            ValueError: If the sample is not found in the properties file and the
                cross-sectional area and/or initial length are not set.
        """

        if (
            self.properties_file is None
            and self.cross_sectional_area_m2 is None
            and self.initial_length_m is None
        ):
            return

        with self.properties_file.open(newline="", encoding="utf-8-sig") as csv_file:
            reader: csv.DictReader[str] = csv.DictReader(csv_file)

            for row in reader:
                if row["Name"] != name:
                    continue
                if self.cross_sectional_area_m2 is None:
                    self.cross_sectional_area_m2 = (
                        float(row["Cross-sectional area"]) * 1e-6
                    )
                if self.initial_length_m is None:
                    self.initial_length_m = float(row["Initial length"]) * 1e-3

                return

        raise ValueError(f"Sample '{name}' not found in {self.properties_file}")


class Analyser(ma_analyser.Analyser):
    """
    Base class for all Instron 68TM analysers.

    Args:
        input_file: The path to the input file containing the output of the Instron 68TM
            experiment.
        parameters: The parameters to use when analysing the experiment.
        raw_transcoder: The raw experiment data file transcoder.
        summary_data: The summary of the analysis.
        phases: The phases of the experiment.
        id: The unique identifier for the analyser.  If empty, a new identifier is
            generated.
    """

    def __init__(
        self,
        input_file: Path,
        parameters: Parameters,
        raw_transcoder: ma_data.RawTranscoder,
        summary_data: ma_data.SummaryData,
        phases: list[ma_phase.Phase] = [],
        id: str = "",
    ) -> None:

        super().__init__(
            parameters,
            ma_data.RawData.load(
                input_file,
                raw_transcoder,
                tare_force_N=parameters.tare_force_N,
            ),
            summary_data,
            [phase for phase in phases],
            id,
        )

    @property
    def parameters(self) -> Parameters:
        return cast(Parameters, self._parameters)

    @property
    def phases(self) -> list[ma_phase.Phase]:  # type: ignore
        return cast(list[ma_phase.Phase], self._phases)

    @property
    def raw_data(self) -> ma_data.RawData:
        return cast(ma_data.RawData, self._raw_data)

    @property
    def summary_data(self) -> ma_data.SummaryData:
        return cast(ma_data.SummaryData, self._summary_data)
