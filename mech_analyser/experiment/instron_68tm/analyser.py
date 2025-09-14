import dataclasses
from typing import cast
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
    """

    tare_force_N: float = 0.0


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
