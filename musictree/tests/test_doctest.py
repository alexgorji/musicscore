from musictree.chord import Chord
from musictree.midi import Midi
from musictree.quarterduration import QuarterDuration


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
        <class 'musictree.midi.Midi'>
        >>> m = Midi(40)
        >>> a.midi = m
        >>> a.midi.value
        40
        >>> ch = Chord(midis=[60, 50])
        >>> [m.value for m in ch.midis]
        [60, 50]
        """
        return self._midi

    @midi.setter
    def midi(self, val):
        if not isinstance(val, Midi):
            val = Midi(val)
        self._midi = val
