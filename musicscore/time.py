from typing import List, Optional

from musicscore.exceptions import TimeActualSignaturesNotValidError
from musicscore.quarterduration import QuarterDuration
from musicscore.util import isinstance_as_string
from musicxml.xmlelement.xmlelement import XMLTime, XMLBeats, XMLBeatType
from musicscore.xmlwrapper import XMLWrapper

__all__ = ['Time', 'flatten_times', 'CONVERSION_DICTIONARY']

#: If :obj:`Time.actual_signatures` is not set manually first this dictionary is used to create actual signature.
CONVERSION_DICTIONARY = {'2/8': [2, 8], '4/8': [2, 8, 2, 8], '5/8': [3, 8, 2, 8], '7/8': [4, 8, 3, 8]}


def _convert_signatures_to_ints(signatures):
    output = []
    for i in range(int(len(signatures) / 2)):
        beat = signatures[i * 2]
        beat_type = signatures[i * 2 + 1]
        if isinstance(beat, str):
            l = beat.split('+')
            if len(l) == 1:
                output.append(int(beat))
                output.append(int(beat_type))
            else:
                for x in l:
                    output.append(int(x))
                    output.append(int(beat_type))
        else:
            output.append(beat)
            output.append(int(beat_type))
    if not output:
        raise TimeActualSignaturesNotValidError
    return output


def _get_quarter_durations_from_ints(signatures):
    output = 0
    for i in range(int(len(signatures) / 2)):
        beat = signatures[i * 2]
        beat_type = signatures[i * 2 + 1]
        output += 4 * beat / beat_type
    return output


class Time(XMLWrapper):
    _ATTRIBUTES = {'signatures', 'actual_signatures', 'parent_measure', 'show'}
    XMLClass = XMLTime

    def __init__(self, *signatures, show=True, **kwargs):
        super().__init__()
        self._xml_object = self.XMLClass(**kwargs)
        self._parent_measure = None

        self._signatures = None
        self._actual_signatures = None
        self._intern_actual_signatures = None
        self._show = None

        self.signatures = signatures
        self.show = show

    def _calculate_actual_signatures(self):
        signatures = _convert_signatures_to_ints(self.signatures)
        signatures = [signatures[i:i + 2] for i in range(0, len(signatures), 2)]
        self._intern_actual_signatures = []
        for signature in signatures:
            key = "/".join([str(x) for x in signature])
            if key in CONVERSION_DICTIONARY:
                self._intern_actual_signatures.extend(CONVERSION_DICTIONARY[key])
            elif signature[1] % 8 == 0 and signature[0] % 3 == 0:
                self._intern_actual_signatures.extend([3, signature[1]] * (signature[0] // 3))
            else:
                self._intern_actual_signatures.extend([1, signature[1]] * signature[0])
        return self._intern_actual_signatures

    def _reset_actual_signatures(self) -> None:
        """
        Resets actual signatures to None.
        """
        self._actual_signatures = None
        self._intern_actual_signatures = None

    def _update_signature_objects(self):
        signatures = [self.signatures[i:i + 2] for i in range(0, len(self.signatures), 2)]
        for beats, beat_type in zip(self._xml_object.find_children('XMLBeats'),
                                    self._xml_object.find_children('XMLBeatType')):
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

    @property
    def actual_signatures(self) -> List[int]:
        """
        Set and gets actual signatures. If :obj:`parent_measure` exists its beats inside voices will be updated.

        :return: A list of int representing actual time signatures. If not set manually, it is calculated internally. For example a 4/4 time
                 signature gets automatically [1, 4, 1, 4, 1, 4, 1, 4] as actual_signatures if not set otherwise.

        .. seealso::
           :obj:`CONVERSION_DICTIONARY`
        """
        if self._actual_signatures is None:
            if self._intern_actual_signatures is None:
                self._calculate_actual_signatures()
            return self._intern_actual_signatures
        return self._actual_signatures

    @actual_signatures.setter
    def actual_signatures(self, val):
        if val is not None:
            val = _convert_signatures_to_ints(val)
        self._actual_signatures = val
        if self.parent_measure:
            self.parent_measure._update_voice_beats()

    @property
    def parent_measure(self) -> Optional["Measure"]:
        """
        Set and get parent :obj:`~musicscore.measure.Measure`.
        """
        return self._parent_measure

    @parent_measure.setter
    def parent_measure(self, val):
        if not val and not isinstance_as_string(val, "Measure"):
            raise TypeError
        self._parent_measure = val

    @property
    def signatures(self) -> List[int]:
        """
        Set and gets signatures. If :obj:`~parent_measure` exists, beats inside its voices will be updated. If it is set to ``None`` a 4/4 signature will be used.

        :return: A list of int representing time signature.
        """
        return self._signatures

    @signatures.setter
    def signatures(self, val):
        if not val:
            val = [4, 4]
        for v in val:
            if not isinstance(v, int) and not isinstance(v, str):
                raise TypeError
        self._signatures = val
        self._reset_actual_signatures()
        self._update_signature_objects()
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

    def get_beats_quarter_durations(self) -> List[QuarterDuration]:
        """
        :return: List of quarter durations according to :obj:`actual_signatures`
        """
        return [QuarterDuration(numerator, denominator) * 4 for numerator, denominator in
                [self.actual_signatures[i:i + 2] for i in range(0, len(self.actual_signatures), 2)]]

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
