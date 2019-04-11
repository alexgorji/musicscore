from quicktions import Fraction

from musicscore.basic_functions import lcm
from musicscore.dtd.dtd import Element
from musicscore.musictree.exceptions import MusicTreeError
from musicscore.musictree.treebeat import TreeBeat
from musicscore.musictree.treenote import TreeNote
from musicscore.musicxml.elements import timewise as timewise
from musicscore.musicxml.elements.attributes import Attributes, Divisions
from musicscore.musicxml.elements.fullnote import Pitch
from musicscore.musicxml.elements.note import Beam, Tie


class TreePart(timewise.Part):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attributes = self.add_child(Attributes())
        attributes.add_child(Divisions(1))
        self._accidental_steps = []
        self._beats = []

    def get_divisions(self):
        duration_denominators = [note.quarter_duration.denominator for note in
                                 self.get_children_by_type(TreeNote)]

        if len(duration_denominators) == 0:
            return 1
        elif len(duration_denominators) == 1:
            return duration_denominators[0]
        else:
            return lcm(duration_denominators)

    @property
    def notes(self):
        return self.get_children_by_type(TreeNote)

    def add_note(self, note):
        if not isinstance(note, TreeNote):
            raise TypeError()

        self.add_child(note)
        previous_note = note.previous
        if previous_note and previous_note.is_tied:
            note.add_tie('stop')

    # def update_note_offsets(self):
    #     notes = self.notes
    #     for index, note in enumerate(notes):
    #         if not note.offset:
    #             if index == 0:
    #                 note._offset = 0
    #             else:
    #                 previous_note = notes[index - 1]
    #                 note._offset = previous_note.offset + previous_note.quarter_duration

    def _group_beats(self, grouping_list):
        # todo test grouping list
        if False:
            raise Exception()
        else:
            notes = self.notes
            grouped_notes = []
            group_positions = [0]
            for group in grouping_list:
                # todo list of beat_types

                beat_type = self.up.time.beat_type
                if isinstance(beat_type, list):
                    raise NotImplementedError()

                group_positions.append(group_positions[-1] + group * (4. / beat_type.value))
            current_note_index = 0
            group_positions.pop(0)
            for group_position in group_positions:
                current_grouped_notes = []
                while current_note_index < len(notes) and notes[current_note_index].offset < group_position:
                    current_grouped_notes.append(notes[current_note_index])
                    current_note_index = current_note_index + 1

                grouped_notes.append(current_grouped_notes)
            return grouped_notes

    def group_beams(self, grouping_list=None):

        def _generate_grouping_list():
            grouping_list = []
            for (beats, beat_type) in self.up.time.get_time_signatures():
                if beats.value % 3 == 0 and beat_type.value != 4:
                    for x in range(beats.value // 3):
                        grouping_list.append(3)
                else:
                    for x in range(beats.value):
                        grouping_list.append(1)
            return grouping_list

        def _set_beams(grouped_notes):
            for group in grouped_notes:
                begin_beam = True
                continue_end_beam = False

                for i in range(len(group)):
                    note = group[i]
                    if note.type.value in ('eighth', '16th', '32nd'):
                        beam = note.add_child(Beam(None))
                        if i != len(group) - 1:
                            if begin_beam:
                                beam.value = 'begin'
                                begin_beam = False
                                continue_end_beam = True

                            elif continue_end_beam:
                                if i == len(group) - 1:
                                    beam.value = 'end'
                                    begin_beam = True
                                    continue_end_beam = False
                                else:
                                    beam.value = 'continue'
                        elif len(group) > 1 and group[i - 1] != []:
                            beam.value = 'end'

                    elif i != 0:
                        try:
                            beam = group[i - 1].beam

                            if beam.value == 'begin':
                                group[i - 1].remove_child(beam)
                                begin_beam = True
                                continue_end_beam = False
                            elif beam.value == 'continue':
                                group[i - 1].beam.value = 'end'
                                begin_beam = True
                                continue_end_beam = False
                        except AttributeError:
                            pass

        if grouping_list is None:
            grouping_list = _generate_grouping_list()
            grouped_notes = self._group_beats(grouping_list)
            _set_beams(grouped_notes)
        else:
            raise NotImplementedError('group_beams with values other than None')

    def update_divisions(self):
        attributes = self.get_children_by_type(Attributes)[0]
        divisions = attributes.get_children_by_type(Divisions)[0]
        divisions.value = self.get_divisions()

    def update_accidentals(self, mode):
        if mode == 'normal':
            self._accidental_steps = []
            pitched_notes = [note for note in self.get_children_by_type(TreeNote) if isinstance(note.event, Pitch)]
            for note in pitched_notes:
                if note.pitch.alter is not None and note.pitch.alter.value != 0 and note.pitch.step.value not in self._accidental_steps:
                    note.accidental.show = True
                    self._accidental_steps.append(note.pitch.step.value)
                elif (
                        note.pitch.alter is None or note.pitch.alter.value == 0) and note.pitch.step.value in self._accidental_steps:
                    self._accidental_steps.remove(note.pitch.step.value)
                    note.accidental.show = True
        else:
            raise MusicTreeError('mode {} is not known to update accidentals'.format(mode))

    def set_beats(self, list_of_beats=None):
        if not self.up:
            raise Exception('part must be a child of a measure to be able to set beats')
        if list_of_beats is None:
            list_of_beats = []
            for time_signature in self.up.time.get_time_signatures():
                (beats, beat_type) = time_signature
                for b in range(beats.value):
                    tree_beat = TreeBeat(duration=4. / beat_type.value)
                    list_of_beats.append(tree_beat)
                    tree_beat._part = self
        else:
            duration = 0
            for beat in list_of_beats:
                beat._part = self
                duration += beat.duration
            if self.up.quarter_duration != duration:
                raise ValueError('sum of beat durations must be equal to measure duration')

        self._beats = list_of_beats

    @property
    def beats(self):
        return self._beats

    def split_note(self, note, ratios):
        if not isinstance(note, TreeNote):
            raise TypeError()

        new_notes = note.split(ratios)
        for new_note in new_notes[:-1]:
            new_note.add_child(Tie())

        insert_index = note.node._xml_children.index(note) + 1

        for new_note in new_notes[1:].__reversed__():
            self.add_child(new_note)
            note.node._xml_children.remove(new_note)
            note.node._xml_children.insert(insert_index, new_note)
            self.update_current_children()

        return new_notes

    def add_notes_to_beats(self):
        notes = self.get_children_by_type(TreeNote)
        beats = iter(self.beats)
        current_beat = beats.__next__()
        next_beat = beats.__next__()
        while_loop = True

        for note in notes:
            while while_loop and (note.offset < current_beat.offset or note.offset >= next_beat.offset):
                try:
                    current_beat = next_beat

                    next_beat = beats.__next__()
                except StopIteration:
                    while_loop = False

            current_beat.add_note(note)

    def split_notes_beatwise(self):
        for beat in self.beats:
            if beat.notes:
                first_note = beat.notes[0]

                if beat.offset < first_note.offset:
                    previous_note = first_note.previous
                    tail_duration = (previous_note.end_position - beat.offset)
                    ratios = [previous_note.quarter_duration - tail_duration, tail_duration]
                    split = self.split_note(previous_note, ratios)
                    # for note in split:
                    beat.notes.insert(0, split[1])

        for beat in self.beats:
            if beat.notes and len(beat.notes) != 1:
                last_note = beat.notes[-1]
                if last_note.end_position > beat.end_position:
                    head_duration = (beat.end_position - last_note.offset)
                    ratios = [head_duration, last_note.quarter_duration - head_duration]
                    split = self.split_note(last_note, ratios)
                    beat.next.notes.insert(0, split[1])

    def quantize(self):
        self.add_notes_to_beats()
        self.split_notes_beatwise()
        for beat in self.beats:
            beat.quantize()

    def finish(self):
        if not self.beats:
            self.set_beats()

        self.quantize()

        self.update_divisions()
        self.update_accidentals(mode='normal')

        for note in self.get_children_by_type(TreeNote):
            note.update_duration(self.get_divisions())

        for note in self.get_children_by_type(TreeNote):
            note.update_type()
            note.update_dot()

        self.group_beams()
