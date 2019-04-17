from lxml import etree as et
from quicktions import Fraction

from musicscore.basic_functions import lcm, substitute
from musicscore.musictree.exceptions import MusicTreeError
from musicscore.musictree.treebeat import TreeBeat
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treenote import TreeNote
from musicscore.musicxml.elements import timewise as timewise
from musicscore.musicxml.elements.attributes import Attributes, Divisions
from musicscore.musicxml.elements.fullnote import Pitch
from musicscore.musicxml.elements.note import Beam, Type, Tie


class TreePart(timewise.Part):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attributes = self.add_child(Attributes())
        attributes.add_child(Divisions(1))
        self._accidental_steps = []
        self._beats = []
        self._chords = []

    @property
    def chords(self):
        return self._chords

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

    @property
    def remaining_duration(self):
        measure = self.up
        if self.chords:
            return measure.quarter_duration - self.chords[-1].end_position
        return measure.quarter_duration

    def add_chord(self, chord):
        measure = self.up
        if not measure:
            raise Exception('parent measure needed before adding chord to part')

        if not isinstance(chord, TreeChord):
            raise TypeError()

        remain = chord.quarter_duration - self.remaining_duration

        if self.remaining_duration == 0:
            return chord

        elif remain > 0:
            split = self._split_chord(chord, [chord.quarter_duration - remain, remain])
            split[0].parent_part = self
            self.chords.append(split[0])
            return split[1]
        else:
            self.chords.append(chord)
            chord.parent_part = self

    def chord_to_notes(self):
        for chord in self.chords:
            for note in chord._notes:
                self.add_child(note)

    def _group_beats(self, grouping_list):
        # todo test grouping list
        if False:
            raise Exception()
        else:
            chords = self.chords
            grouped_chords = []
            group_positions = [0]
            for group in grouping_list:
                # todo list of beat_types

                beat_type = self.up.time.beat_type
                if isinstance(beat_type, list):
                    raise NotImplementedError()

                group_positions.append(group_positions[-1] + group * (4. / beat_type.value))
            current_chord_index = 0
            group_positions.pop(0)
            for group_position in group_positions:
                current_grouped_chords = []
                while current_chord_index < len(chords) and chords[current_chord_index].offset < group_position:
                    current_grouped_chords.append(chords[current_chord_index])
                    current_chord_index = current_chord_index + 1

                grouped_chords.append(current_grouped_chords)
            return grouped_chords

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

        def _set_beams(grouped_chords):

            for group in grouped_chords:
                begin_beam = True
                continue_end_beam = False

                for i in range(len(group)):
                    chord = group[i]
                    if chord.get_children_by_type(Type)[0].value in ('eighth', '16th', '32nd'):
                        beam = chord.add_child(Beam(None))
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
            grouped_chords = self._group_beats(grouping_list)
            _set_beams(grouped_chords)
        else:
            raise NotImplementedError('group_beams with values other than None')

    def update_divisions(self):
        attributes = self.get_children_by_type(Attributes)[0]
        divisions = attributes.get_children_by_type(Divisions)[0]
        divisions.value = self.get_divisions()

    def get_previous_measure_last_notes(self):
        previous_measure_last_notes = []
        try:
            previous_measure = self.up.previous
        except AttributeError:
            previous_measure = None
        if previous_measure:
            part = [p for p in previous_measure.get_children_by_type(TreePart) if p.id == self.id][0]
            previous_measure_last_chord = part.chords[-1]
            previous_measure_last_notes = previous_measure_last_chord._notes
        return previous_measure_last_notes


    def update_accidentals(self, mode):
        def _get_previous_measure_last_signed_notes():
            previous_measure_last_notes = self.get_previous_measure_last_notes()
            return [n for n in previous_measure_last_notes if isinstance(n.event, Pitch) and n.pitch.alter and n.pitch.alter.value != 0]

        if mode == 'normal':
            _hide_accidental = []
            _set_natural = []
            pitched_notes = [note for note in self.get_children_by_type(TreeNote) if isinstance(note.event, Pitch)]
            _first_chord_natural = [note.pitch.step.value for note in _get_previous_measure_last_signed_notes()]

            for note in pitched_notes:
                if note.pitch.alter is not None and note.pitch.alter.value != 0 and note.pitch.step.value not in _hide_accidental:
                    if 'stop' not in [t.type for t in note.get_children_by_type(Tie)]:
                        note.accidental.show = True
                        _hide_accidental.append(note.pitch.step.value)
                    _set_natural.append(note.pitch.step.value)
                elif (
                        note.pitch.alter is None or note.pitch.alter.value == 0):
                    if note.pitch.step.value in _set_natural:
                        try:
                            _hide_accidental.remove(note.pitch.step.value)
                        except ValueError:
                            pass
                        _set_natural.remove(note.pitch.step.value)
                        note.accidental.show = True
                    elif note.offset == 0 and note.pitch.step.value in _first_chord_natural:
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

    @staticmethod
    def _split_chord(chord, ratios):
        if not isinstance(chord, TreeChord):
            raise TypeError()

        new_chords = chord.split(ratios)
        if chord.midis[0].value != 0:
            for new_chord in new_chords[:-1]:
                new_chord.add_tie('start')

            for new_chord in new_chords[1:]:
                new_chord.add_tie('stop')

        return new_chords

    def _add_chords_to_beats(self):
        beats = iter(self.beats)
        current_beat = beats.__next__()
        next_beat = beats.__next__()
        while_loop = True

        for chord in self.chords:
            while while_loop and (chord.offset < current_beat.offset or chord.offset >= next_beat.offset):
                try:
                    current_beat = next_beat
                    next_beat = beats.__next__()
                except StopIteration:
                    while_loop = False

            current_beat.add_chord(chord)

    def _split_chords_beatwise(self):
        for beat in self.beats:
            if beat.chords:
                first_chords = beat.chords[0]

                if beat.offset < first_chords.offset:
                    previous_chord = first_chords.previous
                    tail_duration = (previous_chord.end_position - beat.offset)
                    ratios = [previous_chord.quarter_duration - tail_duration, tail_duration]
                    split = self._split_chord(previous_chord, ratios)
                    self._chords = substitute(self._chords, previous_chord, split)
                    beat.chords.insert(0, split[1])
                    split[1].parent_beat = beat

        for beat in self.beats:
            if beat.chords and len(beat.chords) != 1:
                last_chord = beat.chords[-1]
                if last_chord.end_position > beat.end_position:
                    head_duration = (beat.end_position - last_chord.offset)
                    ratios = [head_duration, last_chord.quarter_duration - head_duration]
                    split = self._split_chord(last_chord, ratios)
                    self._chords = substitute(self._chords, last_chord, split)
                    beat.next.chords.insert(0, split[1])
                    split[1].parent_beat = beat.next

    def quantize(self):
        self._add_chords_to_beats()
        self._split_chords_beatwise()
        for beat in self.beats:
            beat.quantize()

    def fill_with_rest(self):
        if self.remaining_duration > 0:
            if self.chords and self.chords[-1].midis[0].value == 0:
                self.chords[-1].quarter_duration += Fraction(self.remaining_duration)
            else:
                rest = TreeChord(midis=0, quarter_duration=self.remaining_duration)
                self.add_chord(rest)

    def finish(self):
        if not self.beats:
            self.set_beats()

        self.fill_with_rest()

        self.quantize()

        for beat in self.beats:
            beat.check_notatability()

        # self.update_chord_accidentals(mode='show')

        for chord in self.chords:
            chord.update_type()
            chord.update_dot()

        self.group_beams()

        self.chord_to_notes()

        self.update_divisions()
        self.update_accidentals(mode='normal')
        for note in self.get_children_by_type(TreeNote):
            note.update_duration(self.get_divisions())

    def to_string(self):
        self.finish()
        self.close_dtd()
        xml = self._to_xml()
        return et.tounicode(xml, pretty_print=True)
