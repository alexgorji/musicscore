from quicktions import Fraction

from musicscore.basic_functions import lcm
from musicscore.musictree.exceptions import MusicTreeError
from musicscore.musictree.treenote import TreeNote
from musicscore.musicxml.elements import timewise as timewise
from musicscore.musicxml.elements.attributes import Attributes, Divisions
from musicscore.musicxml.elements.fullnote import Pitch


class Part(timewise.Part):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attributes = self.add_child(Attributes())
        attributes.add_child(Divisions(1))
        self._accidental_steps = []

    def get_divisions(self):
        duration_denominators = [note.quarter_duration.denominator for note in
                                 self.get_children_by_type(TreeNote)]

        if len(duration_denominators) == 0:
            return 1
        elif len(duration_denominators) == 1:
            return duration_denominators[0]
        else:
            return lcm(duration_denominators)

    def update_divisions(self):
        attributes = self.get_children_by_type(Attributes)[0]
        divisions = attributes.get_children_by_type(Divisions)[0]
        divisions.value = self.get_divisions()

    def update_accidentals(self, mode):
        if mode == 'normal':
            self._accidental_steps = []
            pitched_notes = [note for note in self.get_children_by_type(TreeNote) if isinstance(note.event, Pitch)]
            for note in pitched_notes:
                if note.pitch.alter.value != 0 and note.pitch.step.value not in self._accidental_steps:
                    note.accidental.show = True
                    self._accidental_steps.append(note.pitch.step.value)
                elif note.pitch.alter.value == 0 and note.pitch.step.value in self._accidental_steps:
                    self._accidental_steps.remove(note.pitch.step.value)
                    note.accidental.show = True
        else:
            raise MusicTreeError('mode {} is not known to update accidentals'.format(mode))

    def quantize(self):
        for note in self.get_children_by_type(TreeNote):
            note.quarter_duration = Fraction(note.quarter_duration).limit_denominator(12)

    def finish(self):
        self.quantize()

        self.update_divisions()

        self.update_accidentals(mode='normal')

        for note in self.get_children_by_type(TreeNote):
            note.update_duration(self.get_divisions())

        for note in self.get_children_by_type(TreeNote):
            note.update_type()
            note.update_dot()