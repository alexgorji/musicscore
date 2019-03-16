from musicscore.musictree.exceptions import MusicTreeError
from musicscore.musicxml.elements.note import Note, Type, Dot
from musicscore.musicxml.elements.fullnote import Event, Rest
from musicscore.musicxml.elements.attributes import Attributes, Divisions, Time, SenzaMisura, Beats, BeatType
from quicktions import Fraction
from musicscore.basic_functions import lcm


#
# class MusicNote(Note):
#     """"""
#
#     def __init__(self, event=Rest(), quarter_duration=1, *args, **kwargs):
#         super().__init__(duration=None, *args, **kwargs)
#         self.quarter_duration = quarter_duration
#         self.event = event
#
#     @property
#     def quarter_duration(self):
#         return self._quarter_duration
#
#     @quarter_duration.setter
#     def quarter_duration(self, value):
#         if value <= 0:
#             raise ValueError('quarter_duration must be a positive number or fraction not {}'.format(value))
#         self._quarter_duration = value
#
#     @property
#     def event(self):
#         return self._event
#
#     @event.setter
#     def event(self, value):
#         if not isinstance(value, Event):
#             raise TypeError('event.value must be of type  not{}'.format(type(value)))
#         self._event = self.add_child(value)
#
#     def update_duration(self):
#         duration = self.up.get_divisions() * self.quarter_duration
#         self.duration = int(duration)
#
#     def update_type(self):
#         """get type of a Note() depending on its quantized duration and return it [whole, half, quarter, eighth, 16th, 32nd, 64th]"""
#         _types = {(1, 12): '32nd',
#                   (1, 11): '32nd',
#                   (2, 11): '16th',
#                   (3, 11): '16th',
#                   (4, 11): 'eighth',
#                   (6, 11): 'eighth',
#                   (8, 11): 'quarter',
#                   (1, 10): '32nd',
#                   (3, 10): '16th',
#                   (1, 9): '32nd',
#                   (2, 9): '16th',
#                   (4, 9): 'eighth',
#                   (8, 9): 'quarter',
#                   (1, 8): '32nd',
#                   (3, 8): '16th',
#                   (7, 8): 'eighth',
#                   (1, 7): '16th',
#                   (2, 7): 'eighth',
#                   (3, 7): 'eighth',
#                   (4, 7): 'quarter',
#                   (6, 7): 'quarter',
#                   (1, 6): '16th',
#                   (1, 5): '16th',
#                   (2, 5): 'eighth',
#                   (3, 5): 'eighth',
#                   (4, 5): 'quarter',
#                   (1, 4): '16th',
#                   (2, 4): 'eighth',
#                   (3, 4): 'eighth',
#                   (7, 4): 'quarter',
#                   (1, 3): 'eighth',
#                   (2, 3): 'quarter',
#                   (3, 2): 'quarter',
#                   (1, 2): 'eighth',
#                   (1, 1): 'quarter',
#                   (2, 1): 'half',
#                   (3, 1): 'half',
#                   (4, 1): 'whole',
#                   (6, 1): 'whole',
#                   (8, 1): 'breve'}
#
#         try:
#             note_type = self.get_children_by_type(Type)[0]
#         except IndexError:
#             note_type = self.add_child(Type('quarter'))
#
#         note_type.value = _types[(self.quarter_duration.numerator, self.quarter_duration.denominator)]
#
#     def update_dot(self):
#         _dot = 0
#         if self.quarter_duration.numerator % 3 == 0:
#             _dot = 1
#         elif self.quarter_duration == Fraction(1, 2) and (
#                 self.up.divisions == 3 or self.up.divisions == 6 or self.up.divisions == 12):
#             _dot = 1
#         elif self.quarter_duration == Fraction(1, 4) and (
#                 self.up.divisions == 3 or self.up.divisions == 6 or self.up.divisions == 12):
#             _dot = 1
#         elif (self.quarter_duration == Fraction(3, 9) or self.quarter_duration == Fraction(6,
#                                                                                            9)) and self.up.divisions == 9:
#             _dot = 1
#         elif self.quarter_duration == Fraction(7, 8):
#             _dot = 2
#         elif self.quarter_duration == Fraction(7, 4):
#             _dot = 2
#         else:
#             _dot = 0
#
#         for dot in self.get_children_by_type(Dot):
#             self.remove_child(dot)
#
#         for i in range(_dot):
#             self.add_child(Dot())


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
                'TreeTime can have senza_misura or (beats, beat_type)* as arguments not {}'.format(time_signature))

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

#
# class TreeMeasure(MeasureTimewise):
#     """"""
#
#     def __init__(self, time=(4, 4), *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._time = None
#
#     @property
#     def time(self):
#         return self._time
#
#     @time.setter
#     def time(self, value):
#         self._time = value
#
#
# class Part(PartTimewise):
#     """"""
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         attributes = self.add_child(Attributes())
#         attributes.add_child(Divisions(1))
#
#     def get_divisions(self):
#         duration_denominators = [note.quarter_duration.denominator for note in
#                                  self.get_children_by_type(MusicNote)]
#
#         if len(duration_denominators) == 0:
#             return 1
#         elif len(duration_denominators) == 1:
#             return duration_denominators[0]
#         else:
#             return lcm(duration_denominators)
#
#     def update_divisions(self):
#         attributes = self.get_children_by_type(Attributes)[0]
#         divisions = attributes.get_children_by_type(Divisions)[0]
#         divisions.value = self.get_divisions()
#
#     def quantize(self):
#         for note in self.get_children_by_type(MusicNote):
#             note.quarter_duration = Fraction(note.quarter_duration).limit_denominator(12)
#
#     def finish(self):
#         self.quantize()
#
#         self.update_divisions()
#
#         for note in self.get_children_by_type(MusicNote):
#             note.update_duration()
#
#         for note in self.get_children_by_type(MusicNote):
#             note.update_type()
#             note.update_dot()
#
#
# class Timwise(ScoreTimewise):
#     """"""
#
#     _auto_part_number = 1
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._part_list = self.add_child(XMLPartList())
#
#     def _generate_score_part(self):
#         id = 'p' + str(self._auto_part_number)
#         self._auto_part_number += 1
#         return XMLScorePart(id=id)
#
#     def get_score_parts(self):
#         return self._part_list.get_children()
#
#     def add_part(self, name='none', print_object='no'):
#         new_score_part = self._generate_score_part()
#         new_score_part.get_children_by_type(XMLPartName)[0].name = name
#         new_score_part.get_children_by_type(XMLPartName)[0].print_object = print_object
#         self._part_list.add_child(new_score_part)
#         for measure in self.get_children_by_type(TreeMeasure):
#             measure.add_child(Part(id=new_score_part.id))
#
#     def add_measure(self):
#         new_measure = TreeMeasure(number=0)
#         self.add_child(new_measure)
#         new_measure.number = len(self.get_children()) - 1
#         for score_part in self.get_score_parts():
#             new_measure.add_child(Part(id=score_part.id))
#         return new_measure
#
#     def add_note(self, measure_number, part_number, note):
#         if not isinstance(note, MusicNote):
#             raise TypeError('add_note note must be of type Note not {}'.format(type(note)))
#         measure = self.get_children_by_type(TreeMeasure)[measure_number - 1]
#         part = measure.get_children_by_type(Part)[part_number - 1]
#         part.add_child(note)
#
#     def add_midi(self, measure_number, part_number, midi=Midi(60), quarter_duration=1):
#         note = MusicNote(event=midi.get_pitch_rest(), quarter_duration=quarter_duration)
#         self.add_note(measure_number, part_number, note)
#
#     def finish(self):
#         for measure in self.get_children_by_type(TreeMeasure):
#             for part in measure.get_children_by_type(Part):
#                 part.finish()
