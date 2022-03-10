from typing import List

from musictree.quarterduration import QuarterDuration
from musicxml.xmlelement.xmlelement import XMLTime, XMLBeats, XMLBeatType
from musictree.xmlwrapper import XMLWrapper

__all__ = ['Time', 'flatten_times']


class Time(XMLWrapper):
    _ATTRIBUTES = {'signatures', 'actual_signatures', '_intern_actual_signatures', 'parent_measure', 'show'}
    XMLClass = XMLTime

    def __init__(self, *signatures, show=True, **kwargs):
        super().__init__()
        self._xml_object = self.XMLClass(**kwargs)
        self.parent_measure = None

        self._signatures = None
        self.signatures = signatures
        self._actual_signatures = None
        self._intern_actual_signatures = None
        self._show = None
        self.show = show

    def _calculate_actual_signatures(self):
        signatures = [self.signatures[i:i + 2] for i in range(0, len(self.signatures), 2)]
        self._intern_actual_signatures = []
        for signature in signatures:
            if signature[1] % 8 == 0 and signature[0] % 3 == 0:
                self._intern_actual_signatures.extend([3, signature[1]] * (signature[0] // 3))
            else:
                self._intern_actual_signatures.extend([1, signature[1]] * signature[0])
        return self._intern_actual_signatures

    @property
    def actual_signatures(self) -> List[int]:
        """
        Set and gets actual signatures. If parent measure exists its beats inside voices will be updated.

        :type: Optional[List[int]]
        :return: A list of int representing actual time signatures. If not set manually, it is calculated internally. For example a 4/4 time
                 signature gets automatically [1, 4, 1, 4, 1, 4, 1, 4] as actual_signatures if not set otherwise.
        :rtype: List[int]
        """
        if self._actual_signatures is None:
            if self._intern_actual_signatures is None:
                self._calculate_actual_signatures()
            return self._intern_actual_signatures
        return self._actual_signatures

    @actual_signatures.setter
    def actual_signatures(self, val):
        self._actual_signatures = val
        if self.parent_measure:
            self.parent_measure._update_voice_beats()

    @property
    def signatures(self) -> List[int]:
        """
        Set and gets signatures. If parent measure exists, beats inside its voices will be updated. If val is None, a 4/4 signature is set.

        :type: Optional[List[int]]
        :return: A list of int representing time signature. If not set manually, it is calculated internally. For example a 4/4 time
                 signature gets automatically [1, 4, 1, 4, 1, 4, 1, 4] as actual_signatures if not set otherwise.
        :rtype: List[int]
        """
        return self._signatures

    @signatures.setter
    def signatures(self, val):
        if not val:
            val = [4, 4]
        for v in val:
            if not isinstance(v, int):
                raise TypeError
        self._signatures = val
        self._update_signature()
        self._intern_actual_signatures = None
        if self.parent_measure:
            self.parent_measure._update_voice_beats()

    @property
    def show(self) -> bool:
        """
        If time signature is shown or not.

        :type: bool
        :return: bool
        """
        return self._show

    @show.setter
    def show(self, val):
        if not isinstance(val, bool):
            raise TypeError
        self._show = val

    @XMLWrapper.xml_object.getter
    def xml_object(self) -> XMLClass:
        return super().xml_object

    def _update_signature(self):
        signatures = [self.signatures[i:i + 2] for i in range(0, len(self.signatures), 2)]
        for beats, beat_type in zip(self._xml_object.find_children('XMLBeats'), self._xml_object.find_children('XMLBeatType')):
            if signatures:
                signature = signatures.pop(0)
                beats.value_ = str(signature[0])
                beat_type.value_ = str(signature[1])
            else:
                beats.up.remove(beats)
                beat_type.up.remove(beat_type)
        for beats, beat_type in signatures:
            self._xml_object.add_child(XMLBeats(str(beats)))
            self._xml_object.add_child(XMLBeatType(str(beat_type)))

    def get_beats_quarter_durations(self) -> List[QuarterDuration]:
        """
        :return: List of quarter durations according to :obj:`actual_signatures`
        """
        return [QuarterDuration(numerator, denominator) * 4 for numerator, denominator in [self.actual_signatures[i:i + 2] for i in range(0,
                                                                                                                                          len(self.actual_signatures),
                                                                                                                                          2)]]

    def reset_actual_signatures(self) -> None:
        """
        Resets actual signatures to None.
        """
        self._actual_signatures = None
        self._intern_actual_signatures = None

    def __copy__(self):
        cp = self.__class__(*self.signatures, show=self.show)
        cp._actual_signatures = self._actual_signatures
        return cp

    def __rmul__(self, other):
        return [self.__copy__() for _ in range(other)]


def flatten_times(times) -> List[Time]:
    """
    :param times: an expandable list of times or tuples representing times. For example [x * Time(3, 8)] return x time intances of Time(3, 8)
    :return: List[Time]

    >>> ts = [2 * Time(3, 8), (3, 4), 3 * [(1, 8)], Time(1, 8, 3, 4), Time(3, 4)]
    >>> [t.signatures for t in flatten_times(ts)]
    [(3, 8), (3, 8), (3, 4), (1, 8), (1, 8), (1, 8), (1, 8, 3, 4), (3, 4)]
    """
    output = []
    for time in times:
        if isinstance(time, Time):
            output.append(time)
        elif hasattr(time, '__iter__'):
            if {isinstance(t, int) for t in time} == {True}:
                output.append(Time(*time))
            else:
                for t in time:
                    if isinstance(t, Time):
                        output.append(t)
                    else:
                        output.append(Time(*t))
    return output
