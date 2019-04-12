from quicktions import Fraction

from musicscore.dtd.dtd import Sequence, Choice, Element, GroupReference
from musicscore.musictree.midi import Midi
from musicscore.musictree.treenote import TreeNote
from musicscore.musicxml.common.common import EditorialVoice, Staff
from musicscore.musicxml.elements.fullnote import Chord, FullNote
from musicscore.musicxml.elements.note import Cue, Tie, Instrument, Play, Lyric, Notations, Stem, TimeModification
from musicscore.musicxml.elements.xml_element import XMLTree
from musicscore.musicxml.types.complextypes.notations import Tied
from musicscore.basic_functions import substitute


class TreeChord(XMLTree):
    """"""

    _DTD = Sequence(
        Choice(
            Sequence(
                Element(Cue),
                GroupReference(FullNote),
            ),
            Sequence(
                GroupReference(FullNote),
                Element(Tie, 0, 2)
            )
        ),
        Element(Instrument, 0),
        GroupReference(EditorialVoice, 0),
        Element(TimeModification, 0, None),
        Element(Stem, 0),
        GroupReference(Staff, 0),
        Element(Notations, 0, None),
        Element(Lyric, 0, None),
    )

    def __init__(self, *midis, quarter_duration=1, **kwargs):
        super().__init__(**kwargs)
        self.parent_part = None
        self.parent_beat = None
        self._offset = None
        self._quarter_duration = None
        self.quarter_duration = quarter_duration
        self._midis = None
        self.midis = midis

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
        if values:
            output = []
            for midi in values:
                if not isinstance(midi, Midi):
                    output.append(Midi(midi))
                else:
                    output.append(midi)

            for midi in output:
                if midi.value == 0 and len(values) > 1:
                    raise ValueError('midi with value must be alone.')
        else:
            output = None

        self._midis = output

    @property
    def previous(self):
        index = self.parent_part.chords.index(self)
        if index == 0:
            return None
        return self.parent_part.chords[index - 1]

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
        new_chord.parent_part = self.parent_part
        return new_chord

    def split(self, ratios):
        ratios = [int(ratio*100000) for ratio in ratios]

        new_ratios = [Fraction(ratio, sum(ratios)) for ratio in ratios]
        old_duration = self.quarter_duration
        self.quarter_duration *= new_ratios[0]
        output = [self.split_copy(quarter_duration=ratio * old_duration) for ratio in new_ratios[1:]]
        output.insert(0, self)

        if self.parent_part:
            p = self.parent_part
            p._chords = substitute(p._chords, self, output)

        if self.parent_beat:
            b = self.parent_beat
            print('b._chords', b._chords)
            b._chords = substitute(b._chords, self, output)

        return output

    @property
    def notes(self):
        output = []
        for index, midi in enumerate(self.midis):
            note = TreeNote(event=midi.get_pitch_rest(), quarter_duration=self.quarter_duration)
            for child in self.get_children():
                note.add_child(child)
            if index > 0:
                note.add_child(Chord())
            output.append(note)
        return output

    def add_tie(self, value):
        if value == 'start':
            self.add_child(Tie('start'))
            notations = self.add_child(Notations())
            notations.add_child(Tied('start'))
        elif value == 'stop':
            self.add_child(Tie('stop'))
            notations = self.add_child(Notations())
            notations.add_child(Tied('stop'))
        else:
            raise NotImplementedError('value {} cannot be a tie value'.format(value))
