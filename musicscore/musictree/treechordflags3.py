from musicscore.musicxml.elements.note import Notehead, Stem, Beam


class TreeChordFlag3(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __deepcopy__(self, memodict={}):
        return self.__class__()


class NoiseFlag3(TreeChordFlag3):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def implement(self, chord):
        chord.add_child(Notehead('square'))
        return [chord]


class BowPositionFlag(TreeChordFlag3):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def implement(self, chord):
        if chord.is_tied_to_previous:
            chord.remove_previous_tie()
            chord.add_child(Notehead('none'))
            chord.add_child(Stem('none'))
        elif chord.is_tied_to_next:
            chord.add_child(Stem('none'))

        else:
            chord.add_child(Stem('none'))
        beams = chord.get_children_by_type(Beam)
        for beam in beams:
            chord.remove_child(beam)
        return [chord]


class CheckPreviousFlag(TreeChordFlag3):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def implement(self, chord):
        # print('CheckPrevious:')
        # print(chord.previous_in_score_part)
        return [chord]

