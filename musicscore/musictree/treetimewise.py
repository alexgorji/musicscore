from musicscore.musictree.exceptions import MusicTreeError
from musicscore.musictree.midi import Midi
from musicscore.musictree.treenote import TreeNote
from musicscore.musicxml.elements.attributes import Attributes, Divisions, Time, SenzaMisura, Beats, BeatType
from quicktions import Fraction
from musicscore.basic_functions import lcm
import musicscore.musicxml.elements.timewise as timewise
from musicscore.musicxml.elements.fullnote import Pitch
from musicscore.musicxml.elements.score_header import PartList, ScorePart, PartName


class TreeTime(Time):

    def __init__(self, *time_signature, **kwargs):
        super().__init__(**kwargs)
        self._quarter_duration = None
        self.pars_arguments(time_signature)

    def pars_arguments(self, time_signatures):
        if len(time_signatures) == 1 and time_signatures[0] == 'senza_misura':
            self.add_child(SenzaMisura())
            self._quarter_duration = None
        elif len(time_signatures) % 2 == 0:
            self._quarter_duration = 0
            for time_signature in zip(time_signatures[0::2], time_signatures[1::2]):
                self.set_time_signature(time_signature)
                (beats, beat_type) = time_signature
                self._quarter_duration += beats / beat_type * 4
        else:
            raise MusicTreeError(
                'TreeTime can have senza_misura or (beats, beat_type)* as arguments not {}'.format(time_signatures))

    def set_time_signature(self, time_signature):
        (beats, beat_type) = time_signature
        self.add_child(Beats(beats))
        permitted = (1, 2, 4, 8, 16, 32, 64)
        if beat_type not in permitted:
            raise MusicTreeError('beat_type {} must be in {}'.format(beats, permitted))
        else:
            self.add_child(BeatType(beat_type))

    @property
    def quarter_duration(self):
        return self._quarter_duration


class TreeMeasure(timewise.Measure):
    """"""

    def __init__(self, time=(4, 4), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.time = time
        self._time = None

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value


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


class TreeScoreTimewise(timewise.Score):
    """"""

    _auto_part_number = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._part_list = self.add_child(PartList())
        self.version = '3.0'

    def _generate_score_part(self):
        id_ = 'p' + str(self._auto_part_number)
        self._auto_part_number += 1
        return ScorePart(id=id_)

    def get_score_parts(self):
        return self._part_list.get_children()

    def add_part(self, name='none', print_object='no'):
        new_score_part = self._generate_score_part()
        part_name = new_score_part.add_child(PartName(name=name))
        part_name.print_object = print_object
        self._part_list.add_child(new_score_part)
        for measure in self.get_children_by_type(TreeMeasure):
            measure.add_child(Part(id=new_score_part.id))

    def add_measure(self):
        new_measure = TreeMeasure(number='0')
        self.add_child(new_measure)
        new_measure.number = str(len(self.get_children()) - 1)
        for score_part in self.get_score_parts():
            new_measure.add_child(Part(id=score_part.id))
        return new_measure

    def add_note(self, measure_number, part_number, note):
        if not isinstance(note, TreeNote):
            raise TypeError('add_note note must be of type Note not {}'.format(type(note)))
        measure = self.get_children_by_type(TreeMeasure)[measure_number - 1]
        part = measure.get_children_by_type(Part)[part_number - 1]
        part.add_child(note)
        part.quantize()
        divisions = part.get_divisions()
        note.update_duration(divisions=divisions)
        note.update_type()
        note.update_dot()

    def add_midi(self, measure_number, part_number, midi=Midi(60), quarter_duration=1):
        note = TreeNote(event=midi.get_pitch_rest(), quarter_duration=quarter_duration)
        self.add_note(measure_number, part_number, note)

    def finish(self):
        for measure in self.get_children_by_type(TreeMeasure):
            for part in measure.get_children_by_type(Part):
                part.finish()
