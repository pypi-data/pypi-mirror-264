import numpy.typing as npt
from typing import Union

from rhythmoscope.envelope import Envelope

class RhythmSpectrogram:
    """
    Object

        Args:
            sr (int): Sampling rate of the signal
            signal (npt.ArrayLike[int | float]): A one dimentional array containing the raw values
                                                 of the signal.

    """

    def __init__(
        self, sr: int, signal: npt.NDArray, Envelope: Envelope
    ) -> None:
        pass
