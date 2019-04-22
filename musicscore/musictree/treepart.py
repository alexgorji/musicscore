from lxml import etree as et
from quicktions import Fraction

from musicscore.basic_functions import lcm, substitute
from musicscore.musictree.exceptions import MusicTreeError
from musicscore.musictree.treebeat import TreeBeat
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treenote import TreeNote, TreeBackup
from musicscore.musicxml.common.common import Voice
from musicscore.musicxml.elements import timewise as timewise
from musicscore.musicxml.elements.attributes import Attributes, Divisions
from musicscore.musicxml.elements.fullnote import Pitch
from musicscore.musicxml.elements.musicdata import Backup
from musicscore.musicxml.elements.note import Beam, Type, Tie


class TreePartVoice(object):
    def __init__(self, number=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._number = None
        self.number = number
        self._chords = []
        self._beats = None

    @property
    def chords(self):
        return self._chords

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        if not isinstance(value, int):
            raise TypeError('number.value must be of type int not{}'.format(type(value)))
        self._number = value

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

    def add_chord(self, chord):
        remain = chord.quarter_duration - self.remaining_duration
        if self.remaining_duration == 0:
            return chord

        elif remain > 0:
            split = self._split_chord(chord, [chord.quarter_duration - remain, remain])
            self.chords.append(split[0])
            split[0].tree_part_voice = self
            split[0].add_child(Voice(str(self.number)))
            return split[1]
        else:
            self.chords.append(chord)
            chord.tree_part_voice = self
            chord.add_child(Voice(str(self.number)))

    @property
    def remaining_duration(self):
        measure = self.part.up
        if self.chords:
            return measure.quarter_duration - self.chords[-1].end_position
        return measure.quarter_duration

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

                beat_type = self.part.up.time.beat_type
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
            for (beats, beat_type) in self.part.up.time.get_time_signatures():
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

    def set_beats(self, list_of_beats=None):
        if not self.part.up:
            raise Exception('voice must have a part as child of a measure to be able to set beats')
        if list_of_beats is None:
            list_of_beats = []
            for time_signature in self.part.up.time.get_time_signatures():
                (beats, beat_type) = time_signature
                for b in range(beats.value):
                    tree_beat = TreeBeat(duration=4. / beat_type.value)
                    list_of_beats.append(tree_beat)
                    tree_beat._tree_part_voice = self
        else:
            duration = 0
            for beat in list_of_beats:
                beat._tree_part_voice = self
                duration += beat.duration
            if self.part.up.quarter_duration != duration:
                raise ValueError('sum of beat durations must be equal to measure duration')

        self._beats = list_of_beats

    @property
    def beats(self):
        return self._beats

    def _add_chords_to_beats(self):
        if not self._beats:
            self.set_beats()

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


class TreePart(timewise.Part):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attributes = self.add_child(Attributes())
        attributes.add_child(Divisions(1))
        self._voices = {}
        self._finished = False

    @property
    def chords(self):
        output = []
        for voice in self.voices.values():
            output.extend(voice.chords)
        return output

    @property
    def voices(self):
        return self._voices

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

    def set_voice(self, voice_number):
        self.voices[voice_number] = TreePartVoice(voice_number)
        self.voices[voice_number].part = self
        return self.voices[voice_number]

    def get_voice(self, voice_number):
        try:
            return self.voices[voice_number]
        except KeyError:
            return self.set_voice(voice_number)

    def add_chord(self, chord, voice_number=1):
        measure = self.up
        if not measure:
            raise Exception('parent measure needed before adding chord to part')

        if not isinstance(chord, TreeChord):
            raise TypeError()

        voice = self.get_voice(voice_number)
        return voice.add_chord(chord)

    def group_beams(self):
        for voice in self.voices.values():
            voice.group_beams()

    def chord_to_notes(self):
        for index, voice in enumerate(self.voices.values()):
            if index != 0:
                self.add_child(TreeBackup(quarter_duration=voice.part.up.quarter_duration))
            for chord in voice.chords:
                for note in chord._notes:
                    self.add_child(note)

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
            voices = part.voices.values()
            previous_measure_last_chords = []
            for voice in voices:
                previous_measure_last_chords.append(voice.chords[-1])

            previous_measure_last_notes = []
            for chord in previous_measure_last_chords:
                previous_measure_last_notes.extend(chord._notes)
        return previous_measure_last_notes

    def update_accidentals(self, mode):
        def _get_previous_measure_last_signed_notes():
            previous_measure_last_notes = self.get_previous_measure_last_notes()
            return [n for n in previous_measure_last_notes if
                    isinstance(n.event, Pitch) and n.pitch.alter and n.pitch.alter.value != 0]

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
                    elif note.offset == 0 and note.pitch.step.value in _first_chord_natural and 'stop' not in [t.type
                                                                                                               for t in
                                                                                                               note.get_children_by_type(
                                                                                                                   Tie)]:
                        note.accidental.show = True
        else:
            raise MusicTreeError('mode {} is not known to update accidentals'.format(mode))

    def fill_with_rest(self):
        if self.voices == {}:
            self.set_voice(1)
        for voice in self.voices.values():
            voice.fill_with_rest()

    def quantize(self):
        for voice in self.voices.values():
            voice.quantize()

    def finish(self):
        if not self._finished:
            self.fill_with_rest()

            self.quantize()

            for voice in self.voices.values():
                for beat in voice.beats:
                    beat.check_notatability()

            for chord in self.chords:
                chord.update_type()
                chord.update_dot()

            self.group_beams()

            self.chord_to_notes()

            self.update_divisions()
            self.update_accidentals(mode='normal')
            for note in self.get_children_by_type(TreeNote):
                note.update_duration(self.get_divisions())
            for backup in self.get_children_by_type(TreeBackup):
                backup.update_duration(self.get_divisions())

            self.close_dtd()
            self._finished = True

    def to_string(self):
        self.finish()
        xml = self._to_xml()
        return et.tounicode(xml, pretty_print=True)
