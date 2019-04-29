from quicktions import Fraction

from musicscore.dtd.dtd import Sequence, Choice, Element, GroupReference
from musicscore.musictree.midi import Midi
from musicscore.musictree.treenote import TreeNote
from musicscore.musicxml.common.common import EditorialVoice, Staff, Voice
from musicscore.musicxml.elements.fullnote import Chord, FullNote
from musicscore.musicxml.elements.note import Cue, Tie, Instrument, Play, Lyric, Notations, Stem, TimeModification, \
    Type, Dot, Notehead, NoteheadText, Beam, Duration
from musicscore.musicxml.elements.xml_element import XMLTree
from musicscore.musicxml.types.complextypes.lyric import Text
from musicscore.musicxml.types.complextypes.notations import Tied, Tuplet, Ornaments, Dynamics, Technical, Articulations
from musicscore.musicxml.types.complextypes.timemodification import ActualNotes, NormalNotes, NormalType


class TreeChord(XMLTree):
    """"""

    _DTD = Sequence(
        Choice(
            Sequence(
                GroupReference(FullNote),
                Element(Duration),
                Element(Tie, 0, 2)
            ),
            Sequence(
                Element(Cue),
                GroupReference(FullNote),
                Element(Duration)
            ),
        ),
        Element(Instrument, 0),
        GroupReference(EditorialVoice, 0),
        Element(Type, 0),
        Element(Dot, 0, None),
        Element(TimeModification, 0, None),
        Element(Stem, 0),
        Element(Notehead, 0),
        Element(NoteheadText, 0),
        GroupReference(Staff, 0),
        Element(Beam, 0, 8),
        Element(Notations, 0, None),
        Element(Lyric, 0, None),
        Element(Play, 0)
    )

    def __init__(self, midis=71, quarter_duration=1, **kwargs):
        super().__init__(**kwargs)
        self.parent_voice = None
        self.parent_beat = None
        self._offset = None
        self._quarter_duration = None
        self.quarter_duration = quarter_duration
        self._midis = None
        self.midis = midis
        self._tail = False
        self._head = False

    @property
    def quarter_duration(self):
        return self._quarter_duration

    @quarter_duration.setter
    def quarter_duration(self, value):
        if not isinstance(value, int) and not isinstance(value, float) and not isinstance(value, Fraction):
            raise TypeError('quarter_duration must be of type int, float or Fraction not {}'.format(type(value)))

        if value < 0:
            raise ValueError('quarter_duration {} must be zero or positive'.format(value))

        if not isinstance(self.quarter_duration, Fraction):
            self._quarter_duration = Fraction(value).limit_denominator(1000)
        else:
            self._quarter_duration = value

    @property
    def midis(self):
        return self._midis

    @midis.setter
    def midis(self, values):
        try:
            values = list(values)
        except TypeError:
            values = [values]

        output = []
        for midi in values:
            if not isinstance(midi, Midi):
                output.append(Midi(midi))
            else:
                output.append(midi)

        for midi in output:
            if midi.value == 0 and len(values) > 1:
                raise ValueError('midi with value 0 must be alone.')

        self._midis = output

    @property
    def tie_types(self):
        return [tie.type for tie in self.get_children_by_type(Tie)]

    @property
    def position_in_beat(self):
        index_in_beat = self.parent_beat.chords.index(self)
        if index_in_beat == 0:
            return 0
        previous_in_beat = self.parent_beat.chords[index_in_beat - 1]

        return previous_in_beat.position_in_beat + previous_in_beat.quarter_duration

    @property
    def previous(self):
        index = self.parent_voice.chords.index(self)
        if index == 0:
            return None
        return self.parent_voice.chords[index - 1]

    @property
    def next(self):
        index = self.parent_voice.chords.index(self)
        if index == len(self.parent_voice.chords) - 1:
            return None
        return self.parent_voice.chords[index + 1]

    def update_offset(self):
        if self.previous:
            output = self.previous.offset + self.previous.quarter_duration
            self._offset = output
        else:
            self._offset = 0

    @property
    def offset(self):
        if self._offset is None:
            self.update_offset()
        return self._offset

    @property
    def end_position(self):
        return self.offset + self.quarter_duration

    def split_copy(self, quarter_duration):
        new_chord = TreeChord(quarter_duration=quarter_duration)
        new_chord.midis = self.midis
        new_chord.parent_voice = self.parent_voice
        new_chord.parent_beat = self.parent_beat
        new_chord._offset = None
        try:
            voice = self.get_children_by_type(Voice)[0]
            new_chord.add_child(voice)
        except IndexError:
            pass

        return new_chord

    def split(self, *ratios):
        if len(ratios) == 1:
            ratios = ratios[0]

        new_ratios = [Fraction(Fraction(ratio), Fraction(sum(ratios))) for ratio in ratios]

        old_duration = self.quarter_duration

        self.quarter_duration *= new_ratios[0]

        new_chords = [self.split_copy(quarter_duration=ratio * old_duration) for ratio in new_ratios[1:]]

        if 'start' in self.tie_types:
            new_chords[-1].add_tie('start')

        new_chords.insert(0, self)

        if self.midis[0].value != 0:
            for new_chord in new_chords[1:]:
                new_chord.add_tie('stop')

            for new_chord in new_chords[:-1]:
                new_chord.add_tie('start')

        return new_chords

    @property
    def _notes(self):
        output = []
        for index, midi in enumerate(self.midis):
            note = TreeNote(event=midi.get_pitch_rest(), quarter_duration=self.quarter_duration)

            for child in self.get_children():
                if isinstance(child, Lyric) and index != 0:
                    pass
                elif isinstance(child, Notehead) and index != 0:
                    pass
                elif isinstance(child, Notations) and index != 0:
                    grandchildren = child.get_children()
                    for grandchild in grandchildren:
                        if type(grandchild) not in (Ornaments, Technical, Articulations, Dynamics):
                            note._add_notations(grandchild)

                else:
                    note.add_child(child)
            if index > 0:
                note.add_child(Chord())
            output.append(note)
        return output

    def add_tie(self, value):
        if value not in ('stop', 'start'):
            raise NotImplementedError('value {} cannot be a tie value'.format(value))

        try:
            notations = self.get_children_by_type(Notations)[0]
        except IndexError:
            notations = self.add_child(Notations())

        # print('add_tie types')
        # print(types)

        if value == 'start' and 'start' not in self.tie_types:
            self.add_child(Tie('start'))
            notations.add_child(Tied('start'))

        elif value == 'stop' and 'stop' not in self.tie_types:
            self.add_child(Tie('stop'))
            notations.add_child(Tied('stop'))

    def remove_tie(self, type):
        if type in self.tie_types:
            notations = self.get_children_by_type(Notations)[0]
            tie = [t for t in self.get_children_by_type(Tie) if t.type == type][0]
            self.remove_child(tie)

            tied = [t for t in notations.get_children_by_type(Tied) if t.type == type][0]
            notations.remove_child(tied)
            if not notations.get_children():
                self.remove_child(notations)

    def add_tuplet(self, position, number=1):
        normals = {3: 2, 5: 4, 6: 4, 7: 4, 9: 8, 10: 8, 11: 8, 12: 8, 13: 8, 14: 8, 15: 8}
        types = {8: '32nd', 4: '16th', 2: 'eighth'}
        actual_notes = self.parent_beat.best_div
        normal_notes = normals[actual_notes]
        normal_type = types[normal_notes / self.parent_beat.duration]
        if position != 'continue':
            try:
                notations = self.notations
            except AttributeError:
                notations = self.add_child(Notations())
            notations.add_child(Tuplet(type=position, number=number, bracket='yes', placement='above'))

        tm = self.add_child(TimeModification())
        tm.add_child(ActualNotes(actual_notes))
        tm.add_child(NormalNotes(normal_notes))
        tm.add_child(NormalType(normal_type))

    def update_type(self):
        """get type of a Note() depending on its quantized duration and return it [whole, half, quarter, eighth, 16th,
        32nd, 64th]"""
        _types = {(1, 12): '32nd',
                  (1, 11): '32nd',
                  (2, 11): '16th',
                  (3, 11): '16th',
                  (4, 11): 'eighth',
                  (6, 11): 'eighth',
                  (8, 11): 'quarter',
                  (1, 10): '32nd',
                  (3, 10): '16th',
                  (1, 9): '32nd',
                  (2, 9): '16th',
                  (4, 9): 'eighth',
                  (8, 9): 'quarter',
                  (1, 8): '32nd',
                  (3, 8): '16th',
                  (7, 8): 'eighth',
                  (1, 7): '16th',
                  (2, 7): 'eighth',
                  (3, 7): 'eighth',
                  (4, 7): 'quarter',
                  (6, 7): 'quarter',
                  (1, 6): '16th',
                  (1, 5): '16th',
                  (2, 5): 'eighth',
                  (3, 5): 'eighth',
                  (4, 5): 'quarter',
                  (1, 4): '16th',
                  (2, 4): 'eighth',
                  (3, 4): 'eighth',
                  (7, 4): 'quarter',
                  (1, 3): 'eighth',
                  (2, 3): 'quarter',
                  (3, 2): 'quarter',
                  (1, 2): 'eighth',
                  (1, 1): 'quarter',
                  (2, 1): 'half',
                  (3, 1): 'half',
                  (4, 1): 'whole',
                  (6, 1): 'whole',
                  (8, 1): 'breve'}

        if self.quarter_duration == 0:
            value = 'eighth'
        else:
            value = _types[(self.quarter_duration.numerator, self.quarter_duration.denominator)]

        try:
            chord_type = self.get_children_by_type(Type)[0]
            chord_type.value = value
        except IndexError:
            self.add_child(Type(value))

    def update_dot(self):
        _dot = 0

        division = self.parent_voice.part.get_divisions()
        if self.quarter_duration.numerator % 3 == 0:
            _dot = 1
        elif self.quarter_duration == Fraction(1, 2) and (
                division % 3 == 0):
            _dot = 1
        elif self.quarter_duration == Fraction(1, 4) and (
                division % 3 == 0):
            _dot = 1
        elif (self.quarter_duration == Fraction(3, 9) or self.quarter_duration == Fraction(6,
                                                                                           9)) and division % 9 == 0:
            _dot = 1
        elif self.quarter_duration == Fraction(7, 8):
            _dot = 2
        elif self.quarter_duration == Fraction(7, 4):
            _dot = 2
        else:
            _dot = 0

        for dot in self.get_children_by_type(Dot):
            self.remove_child(dot)

        for i in range(_dot):
            self.add_child(Dot())

    def copy(self):
        new_chord = TreeChord(quarter_duration=self.quarter_duration)
        new_chord.midis = self.midis
        for child in self.get_children():
            new_chord.add_child(child)

    def add_lyric(self, text, number=1):
        lyric = self.add_child(Lyric(number=str(number)))
        lyric.add_child(Text(str(text)))
        return lyric

    def __deepcopy__(self, memodict={}):
        new_chord = TreeChord(quarter_duration=self.quarter_duration)
        new_chord.midis = [midi.__deepcopy__() for midi in self.midis]
        for child in self.get_children():
            new_chord.add_child(child)
        return new_chord

    def remove_from_score(self):
        if 'stop' in self.tie_types:
            previous_chord = self.previous
            if not previous_chord:
                previous_chord = self.parent_beat.previous.chords[-1]
            previous_chord.remove_tie('start')
        elif 'start' in self.tie_types:
            next_chord = self.next
            if not next_chord:
                next_chord = self.parent_beat.next.chords[0]
            next_chord.remove_tie('stop')

        self.parent_beat.chords.remove(self)
        self.parent_voice.chords.remove(self)

    def deepcopy_for_SimplfeFormat(self):
        new_chord = TreeChord(quarter_duration=self.quarter_duration)
        new_chord.midis = [midi.__deepcopy__() for midi in self.midis]
        for child in self.get_children():
            if not isinstance(child, Voice):
                new_chord.add_child(child)
        return new_chord
