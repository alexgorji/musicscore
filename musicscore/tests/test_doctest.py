from musicscore.chord import Chord
from musicscore.midi import Midi
from musicscore.quarterduration import QuarterDuration


def something():
    """
    >>> something()
    False
    """
    return False


def get_quarter_duration_value(qd: QuarterDuration):
    """
    >>> get_quarter_duration_value(QuarterDuration(3, 2))
    Fraction(3, 2)
    >>> get_quarter_duration_value(QuarterDuration(0))
    Fraction(0, 1)
    """
    return qd.value


class A:
    def __init__(self):
        self._midi = None

    def something(self):
        """
        >>> A().something()
        True
        """
        return True

    @property
    def midi(self):
        """
        >>> 1==1
        True
        >>> a = A()
        >>> a.midi = 60
        >>> type(a.midi)
        <class 'musicscore.midi.Midi'>
        >>> m = Midi(40)
        >>> a.midi = m
        >>> a.midi.value
        40
        >>> ch = Chord(quarter_duration=1, midis=[60, 50])
        >>> [m.value for m in ch.midis]
        [50, 60]
        """
        return self._midi

    @midi.setter
    def midi(self, val):
        if not isinstance(val, Midi):
            val = Midi(val)
        self._midi = val
