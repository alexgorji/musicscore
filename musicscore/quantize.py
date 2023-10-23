from typing import Optional, List

from musicscore.quarterduration import QuarterDuration
from musicscore.util import isinstance_as_string


class QuantizeMixin:
    _ATTRIBUTES = {'get_quantized'}

    def __init__(self, get_quantized=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._possible_subdivisions = {}
        self._get_quantized = None
        self.get_quantized = get_quantized

    def _get_beat_quarter_duration(self):
        if isinstance_as_string(self, 'Beat'):
            beat_quarter_duration = self.quarter_duration
        else:
            beat_quarter_duration = QuarterDuration(1)
        return beat_quarter_duration

    @property
    def get_quantized(self) -> bool:
        """
        :obj:`~musicscore.quantize.QuantizeMixin` property

        - If ``get_quantized`` is set to None the first ``get_quantized`` of ancestors which is ``False`` or ``True`` will be returned.
        - If :obj:`musicscore.score.Score.get_quantized` is set to None it will be converted to ``False``
        - :obj:`musicscore.measure.Measure.finalize()` loops over all beats. If :obj:`musicscore.beat.Beat.get_quantized` returns ``True``
          :obj:`musicscore.beat.Beat.quantize_quarter_durations()` is called.

        :type: Optional[bool]
        :rtype: bool
        """
        if self._get_quantized is None:
            if self.up:
                return self.up.get_quantized
            else:
                return False
        return self._get_quantized

    @get_quantized.setter
    def get_quantized(self, val):
        self._get_quantized = val

    def get_possible_subdivisions(self, beat_quarter_duration: Optional[QuarterDuration] = None) -> List[int]:
        """
        :obj:`~musicscore.quantize.QuantizeMixin` method

        This method is used by :obj:`~musicscore.beat.Beat`'s :obj:`~musicscore.beat.Beat.quantize_quarter_durations()`.

        Possible subdivisions dictionary can be set with :obj:`~musicscore.quantize.QuantizeMixin.set_possible_subdivisions()`. Keys in the subdivisions dictionary correspond to beat quarter durations (e.g. 1, 1/2 etc.)
        For example if get_possible_subdivisions()[1] ==  [3, 5, 8] a beat with a quarter duration of 1 can after quantization consists only of eighth triplets, quintuplets and 32ths.
        If this dictionary is not set or ``beat_quarter_duration`` as key does not exist, the parent's possible subdivisions dictionary will be checked.

        :obj:`~musicscore.score.Score` has a default :obj:`~musicscore.score.POSSIBLE_SUBDIVISIONS` dictionary which will be used if no other
        musicscore node on the path from self to root has its own possible subdivisions dictionary with ``beat_quarter_duration`` as a
        key. For setting possible subdivisions dictionary use always :obj:`~musicscore.quantize.QuantizeMixin.set_possible_subdivisions()`.

        :param beat_quarter_duration: Used as key in possible subdivisions dictionary.
               If ``None`` and self is a :obj:`~musicscore.beat.Beat` ``self.quarter_duration`` is used.
               If ``None`` and self is not a :obj:`~musicscore.beat.Beat` it is set to 1.
        :return: A list of possible subdivisions of a :obj:`~musicscore.beat.Beat`. This is used by beat's
                 :obj:`~musicscore.beat.Beat.quantize_quarter_durations()`
        :rtype: List[int]
        """
        if beat_quarter_duration is None:
            beat_quarter_duration = self._get_beat_quarter_duration()
        subdivisions = self._possible_subdivisions.get(beat_quarter_duration)
        if subdivisions is None and self.up is not None and self.up.get_possible_subdivisions(
                beat_quarter_duration) is not None:
            subdivisions = self.up.get_possible_subdivisions(beat_quarter_duration)[:]
        return subdivisions

    def set_possible_subdivisions(self, subdivisions: list[int],
                                  beat_quarter_duration: Optional[QuarterDuration] = None) -> None:
        """
        :obj:`~musicscore.quantize.QuantizeMixin` method

        This method is used to set or change possible subdivisions dictionary of a beat or its ascendants.
        For example if get_possible_subdivisions()[1] ==  [3, 5, 8] a beat with a quarter duration of 1 can after quantization consists only of eighth triplets, quintuplets and 32ths.

        :param subdivisions: list of possible subdivisions to be used in :obj:`musicscore.beat.Beat.quantize_quarter_durations()`
        :param beat_quarter_duration: If ``None`` and self is a :obj:`~musicscore.beat.Beat` ``self.quarter_duration`` is used.
                                      If ``None`` and self is not a :obj:`~musicscore.beat.Beat` it is set to 1.
        :return: None
        """
        if beat_quarter_duration is None:
            beat_quarter_duration = self._get_beat_quarter_duration()
        elif isinstance_as_string(self, 'Beat') and beat_quarter_duration != self.quarter_duration:
            raise ValueError(
                f"beat_quarter_duration '{beat_quarter_duration}' must be None or equal to the beat quarter_duration '{self.quarter_duration}'")

        if not isinstance(beat_quarter_duration, QuarterDuration):
            beat_quarter_duration = QuarterDuration(beat_quarter_duration)
        try:
            subdivisions = list(subdivisions)
        except TypeError:
            subdivisions = [subdivisions]
        self._possible_subdivisions[beat_quarter_duration] = subdivisions
