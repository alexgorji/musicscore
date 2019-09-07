from musicscore.musicxml.elements.note import Notehead, Type


class TreeChordFlag3(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NoiseFlag3(TreeChordFlag3):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __deepcopy__(self, memodict={}):
        return self.__class__()

    def implement(self, chord):
        chord.add_child(Notehead('square'))
        return [chord]
