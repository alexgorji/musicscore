from musicscore.musicxml.attributes.position import Position
from musicscore.musicxml.elements.note import Notehead, TimeModification, Stem
from musicscore.musicxml.types.complextypes.timemodification import ActualNotes, NormalNotes


class TreeChordFlag(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_split(self, beat, chord):
        quarter_beat = {1.5: [2, 1], 2: [1, 1], 3: [1, 2], 4: [1, 3], 6: [1, 5]}
        eighth_beat = {1: [1, 1], 1.5: [1, 2], 2: [1, 3], 3: [1, 5], 4: [1, 7], 6: [1, 11]}
        if beat.duration == 1:
            try:
                return chord.split(*quarter_beat[chord.quarter_duration])
            except KeyError:
                return [chord]
        elif beat.duration == 0.5:
            try:
                return chord.split(*eighth_beat[chord.quarter_duration])
            except KeyError:
                return [chord]

    def implement_percussion_notation(self, chord, beat):
        if chord.is_tied_to_next:
            chord.remove_tie('start')
        if chord.is_tied_to_previous:
            chord.to_rest()
            output = [chord]
        elif chord.position_in_beat == 0:
            output = self._get_split(beat, chord)
            try:
                output[1].remove_flag(self)
                output[1].to_rest()
            except IndexError:
                pass
        else:
            output = [chord]
        return output


class PizzFlag(TreeChordFlag):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def implement(self, chord, beat):
        output = self.implement_percussion_notation(chord, beat)
        for ch in output:
            if not ch.is_rest:
                ch.add_words('pizz.')
        return output


class PercussionFlag(TreeChordFlag):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def implement(self, chord, beat):
        output = self.implement_percussion_notation(chord, beat)
        return output


class NoiseFlag(TreeChordFlag):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def implement(self, chord):
        chord.add_child(Notehead('square'))
        return [chord]


class BeatwiseFlag(TreeChordFlag):
    def __init__(self, slur='dashed', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slur = slur

    def _get_split(self, chord, beat):
        quarter_beat = {2: [1, 1], 3: [1, 2], 4: [1, 3], 6: [1, 5]}
        eighth_beat = {2: [1, 1], 3: [1, 2], 4: [1, 3], 6: [1, 5]}

        if beat.duration == 1:
            try:
                return chord.split(*quarter_beat[chord.quarter_duration])
            except KeyError:
                return [chord]

        elif beat.duration == 0.5:
            try:
                return chord.split(*eighth_beat[chord.quarter_duration])
            except KeyError:
                return [chord]

    def _substitute_ties(self, chord):
        if chord.is_tied_to_previous:
            if self.slur == 'tie':
                chord.is_adjoinable = False
            else:
                chord.remove_tie('stop')
                if self.slur is not None:
                    chord.add_slur('stop')

        if chord.is_tied_to_next:
            if self.slur == 'tie':
                chord.is_adjoinable = False
            else:
                chord.remove_tie('start')
                if self.slur is not None:
                    chord.add_slur('start', line_type=self.slur)

    def implement(self, chord, beat):
        output = self._get_split(chord, beat)
        self._substitute_ties(output[0])
        return output


class XFlag(BeatwiseFlag):
    def __init__(self, slur='dashed', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slur = slur

    def implement(self, chord, beat):
        output = super().implement(chord, beat)
        output[0].add_child(Notehead('x'))
        return output


class FingerTremoloFlag(BeatwiseFlag):
    def __init__(self, tremolo_chord, number=3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tremolo_chord = None
        self.tremolo_chord = tremolo_chord
        self.number = number
        self.slur = None

    @property
    def tremolo_chord(self):
        return self._tremolo_chord

    @tremolo_chord.setter
    def tremolo_chord(self, val):
        if val is not None:
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

    def implement(self, chord, beat):
        # output = super().implement(chord, beat)
        # output.insert(1, self.tremolo_chord)
        if self.tremolo_chord.midis[0].value < chord.midis[0].value:
            chord.add_words('\uF415', font_family='bravura', font_size=16, relative_x=30, relative_y=-50)
            chord.set_tie_orientation('over')
        else:
            chord.add_words('\uF417', font_family='bravura', font_size=16, relative_x=30, relative_y=-50)
            chord.set_tie_orientation('under')
        self.tremolo_chord.parent_voice = chord.parent_voice
        self.tremolo_chord.parent_beat = chord.parent_beat

        return [chord, self.tremolo_chord]
