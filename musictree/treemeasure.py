from common.helpers import _check_type
from musictree.treechord import TreeChord
from musictree.treetimesignature import TreeTimeSignature


class TreeMeasure(object):
    """
    This class represents a partwise measure as the second layer of musical score's tree structure.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._chords = []
        self._time_signature = TreeTimeSignature()

    @property
    def time_signature(self):
        """
        Property to get measures time signature
        :return: TreeTimeSignature
        """
        return self._time_signature

    @time_signature.setter
    def time_signature(self, time_signature):
        """
        Property to set measures time signature
        :param time_signature: TreeTimeSignature
        :return: None
        """
        _check_type('time_signature', time_signature, TreeTimeSignature, none=False)
        self._time_signature = time_signature

    @property
    def chords(self):
        """
        Property returns all TreeChords added to measure. To add a chord use methode add_chord
        :return: *TreeChord
        """
        return self._chords

    def add_chord(self, chord=None):
        """
        Add a TreeChord object to measure

        :param chord: None or TreeChord
        :return: TreeChord
        """
        _check_type('chord', chord, TreeChord)
        if chord is None:
            chord = TreeChord()
        self.chords.append(chord)
        return chord
