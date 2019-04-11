from quicktions import Fraction

from musicscore.musictree.midi import Midi
from musicscore.musictree.treenote import TreeNote
from musicscore.musicxml.elements.fullnote import Chord


class TreeChord(object):
    """"""

    def __init__(self, *midis, quarter_duration=1, **kwargs):
        super().__init__(**kwargs)
        self.parent_part = None
        self._offset = None
        self._quarter_duration = None
        self.quarter_duration = quarter_duration
        self._midis = None
        self.midis = midis
        self.is_tied = False

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
        new_ratios = [Fraction(ratio / sum(ratios)) for ratio in ratios]
        old_duration = self.quarter_duration
        self.quarter_duration *= new_ratios[0]
        output = [self.split_copy(quarter_duration=ratio * old_duration) for ratio in new_ratios[1:]]
        output.insert(0, self)
        return output

    @property
    def notes(self):
        output = []
        for index, midi in enumerate(self.midis):
            note = TreeNote(event=midi.get_pitch_rest(), quarter_duration=self.quarter_duration)
            if index > 0:
                note.add_child(Chord())
            output.append(note)
        return output
