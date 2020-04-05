from musicscore.musicxml.elements.note import Notehead, TimeModification, Stem, Beam
from musicscore.musicxml.groups.common import Voice
from musicscore.musicxml.types.complextypes.timemodification import ActualNotes, NormalNotes


class TreeChordFlag2(object):
    """
    These flags would be processed before updating type, dots and grouping beams
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __deepcopy__(self, memodict={}):
        return self.__class__()


class FingerTremoloFlag2(TreeChordFlag2):
    def __init__(self, tremolo_chord, number=3, mode='conventional', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mode = None
        self.mode = mode
        self._tremolo_chord = None
        self.tremolo_chord = tremolo_chord
        self.number = number
        self.slur = None

    def __deepcopy__(self, memodict={}):
        return self.__class__(tremolo_chord=self.tremolo_chord.copy_tremolo_flag(), number=self.number, mode=self.mode)

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, val):
        permitted = ['conventional', 'modern']
        if val not in permitted:
            raise ValueError('mode.value {} must be of in {}'.format(type(val), permitted))
        self._mode = val

    @property
    def tremolo_chord(self):
        return self._tremolo_chord

    @tremolo_chord.setter
    def tremolo_chord(self, val):
        if val is not None and self.mode == 'modern':
            val.is_finger_tremolo = True
            val.add_child(Stem('none'))
            val.set_manual_type('quarter', size='full')
            tm = TimeModification()
            tm.add_child(ActualNotes(0))
            tm.add_child(NormalNotes(1))
            val.add_child(tm)
            val.is_adjoinable = False
            val.quarter_duration = 0

        self._tremolo_chord = val

    def _implement_conventional(self, chord):

        output = [chord]
        chord.remove_tie('start')
        chord.remove_tie('stop')

        output[0].quarter_duration /= 2
        output[0].add_tremolo(type='start')

        if not self.tremolo_chord.tremoli:
            self.tremolo_chord.add_tremolo(type='stop')

        self.tremolo_chord.quarter_duration = chord.quarter_duration

        # self.tremolo_chord.parent_tree_part_voice = chord.parent_tree_part_voice
        self.tremolo_chord.parent_beat = chord.parent_beat
        # v = chord.get_children_by_type(Voice)[0]
        #
        # if not self.tremolo_chord.get_children_by_type(Voice):
        #     self.tremolo_chord.add_child(v)

        output.insert(1, self.tremolo_chord)

        return output

    def _implement_modern(self, chord):

        if self.tremolo_chord.midis[0].value < chord.midis[0].value:
            chord.add_words('\uF415', font_family='bravura', font_size=16, relative_x=30, relative_y=-50)
            chord.set_tie_orientation('over')
        else:
            chord.add_words('\uF417', font_family='bravura', font_size=16, relative_x=30, relative_y=-50)
            chord.set_tie_orientation('under')
        self.tremolo_chord.parent_tree_part_voice = chord.parent_tree_part_voice
        self.tremolo_chord.parent_beat = chord.parent_beat
        v = chord.get_children_by_type(Voice)[0]
        if not self.tremolo_chord.get_children_by_type(Voice):
            self.tremolo_chord.add_child(v)

        return [chord, self.tremolo_chord]

    def implement(self, chord):
        if self.mode == 'modern':
            return self._implement_modern(chord)
        elif self.mode == 'conventional':
            return self._implement_conventional(chord)


class NoiseFlag2(TreeChordFlag2):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def implement(self, chord):
        chord.add_child(Notehead('square'))
        return [chord]


class BowPositionFlag2(TreeChordFlag2):
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
