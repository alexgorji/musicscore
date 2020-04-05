from musicscore.musicxml.elements.note import Notehead, TimeModification, Stem, Notations
from musicscore.musicxml.groups.common import Voice
from musicscore.musicxml.types.complextypes.timemodification import ActualNotes, NormalNotes


class TreeChordFlag1(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_split(self, beat, chord, minimum_duration):
        if minimum_duration == 1:
            spl = {1.5: [2, 1], 2: [1, 1], 3: [1, 2], 4: [1, 3], 6: [1, 5]}
        elif minimum_duration == 0.5:
            spl = {1: [1, 1], 1.5: [1, 2], 2: [1, 3], 3: [1, 5], 4: [1, 7], 6: [1, 11]}
        else:
            raise ValueError('minimum_duration can only be 1 or 0.5')

        try:
            return chord.split(*spl[chord.quarter_duration])
        except KeyError:
            return [chord]

    def implement(self, chord, beat):
        raise NotImplementedError('TreeChordFlag.implement() must be overwritten')

        # if beat.duration == 1:
        #     try:
        #         return chord.split(*spl[chord.quarter_duration])
        #     except KeyError:
        #         return [chord]

    def implement_percussion_notation(self, chord, beat, minimum_duration=1):
        if chord.is_tied_to_next:
            chord.remove_tie('start')
        if chord.is_tied_to_previous:
            chord.to_rest()
            output = [chord]
        elif chord.position_in_beat == 0 and chord.is_rest is False:
            output = self._get_split(beat, chord, minimum_duration)
            try:
                output[1].to_rest()
            except IndexError:
                pass
        else:
            output = [chord]
        for chord in output:
            chord.remove_flag(self)
        return output

    def __deepcopy__(self, memodict={}):
        return self.__class__()


class PizzFlag1(TreeChordFlag1):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def implement(self, chord, beat):
        output = self.implement_percussion_notation(chord, beat)
        # for ch in output:
        #     if not ch.is_rest:
        #         ch.add_words('pizz.')
        return output


class PercussionFlag1(TreeChordFlag1):
    def __init__(self, minimum_duration=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.minimum_duration = minimum_duration

    def implement(self, chord, beat):
        output = self.implement_percussion_notation(chord, beat, self.minimum_duration)
        return output

    def __deepcopy__(self, memodict={}):
        return self.__class__(minimum_duration=self.minimum_duration)


class BeatwiseFlag1(TreeChordFlag1):
    def __init__(self, slur='dashed', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slur = slur

    def __deepcopy__(self, memodict={}):
        return self.__class__(slur=self.slur)

    def _get_split(self, chord, beat):
        quarter_beat = {2: [1, 1], 3: [1, 2], 4: [1, 3], 6: [1, 5]}
        eighth_beat = {1: [1, 1], 1.5: [1, 2], 2: [1, 3], 3: [1, 5]}

        if beat.duration == 1:
            try:
                return chord.split(*quarter_beat[chord.quarter_duration])
            except KeyError:
                return [chord]

        elif beat.duration == 0.5:

            try:
                split = chord.split(*eighth_beat[chord.quarter_duration])
                # for ch in split:
                #     ch.force_tie()
                return split
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


class XFlag1(BeatwiseFlag1):
    def __init__(self, slur='dashed', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slur = slur

    def __deepcopy__(self, memodict={}):
        return self.__class__(slur=self.slur)

    def implement(self, chord, beat):
        output = super().implement(chord, beat)
        output[0].add_child(Notehead('x'))
        return output


class FingerTremoloFlag1(BeatwiseFlag1):
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

    def _implement_conventional(self, chord, beat):
        self.slur = None
        output = super().implement(chord, beat)
        # output = [chord]

        output[0].quarter_duration /= 2
        output[0].add_tremolo(type='start')

        if not self.tremolo_chord.tremoli:
            self.tremolo_chord.add_tremolo(type='stop')

        self.tremolo_chord.quarter_duration = chord.quarter_duration
        self.tremolo_chord.parent_tree_part_voice = chord.parent_tree_part_voice
        self.tremolo_chord.parent_beat = chord.parent_beat
        v = chord.get_children_by_type(Voice)[0]

        if not self.tremolo_chord.get_children_by_type(Voice):
            self.tremolo_chord.add_child(v)

        output.insert(1, self.tremolo_chord)
        return output

    def _implement_modern(self, chord, beat):

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

    def implement(self, chord, beat):
        if self.mode == 'modern':
            return self._implement_modern(chord, beat)
        elif self.mode == 'conventional':
            return self._implement_conventional(chord, beat)


class GlissFlag1(BeatwiseFlag1):
    def __init__(self, mode=1, clef='bass', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._head = True
        self.slur = None
        self.clef = clef
        self.mode = mode

    def __deepcopy__(self, memodict={}):
        copied = self.__class__(mode=self.mode, clef=self.clef)
        copied._head = False
        return copied

    def implement(self, chord, beat):
        output = super().implement(chord, beat)
        if not self._head:
            if output[0].quarter_duration == 1:
                if self.clef == 'bass':
                    midi = 59
                elif self.clef == 'treble':
                    midi = 79
                else:
                    raise NotImplementedError()
                output[0].midis = [midi]
            output[0].add_child(Notehead('none'))

        else:
            if self.mode != 1:
                output[0].add_slide('stop')
            output[0].add_slide('start')
        return output
