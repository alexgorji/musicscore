from typing import List

from math import trunc
from quicktions import Fraction

from musicscore.chord import _split_copy, _group_chords, Chord
from musicscore.config import SPLITTABLES, GENERALSPLITTABLES, SPLITTEXCEPTIONS
from musicscore.exceptions import BeatWrongDurationError, BeatIsFullError, BeatHasNoParentError, \
    ChordHasNoQuarterDurationError, \
    ChordHasNoMidisError, AlreadyFinalizedError, BeatNotFullError, AddChordError, QuarterDurationIsNotWritable, \
    BeatUpdateChordTupletsError, ChordTypeNotSetError
from musicscore.finalize import FinalizeMixin
from musicscore.musictree import MusicTree
from musicscore.quantize import QuantizeMixin
from musicscore.quarterduration import QuarterDuration, QuarterDurationMixin
from musicscore.tuplet import Tuplet
from musicscore.util import lcm, split_list

__all__ = ['Beat', 'beam_chord_group', 'get_chord_group_subdivision']


def _convert_to_quarter_duration_splittables_dictionary(simple_splittalbes):
    output = {}
    for key, value in simple_splittalbes.items():
        output[QuarterDuration(*key)] = {
            QuarterDuration(*k): [QuarterDuration(*qd) for qd in v] for k, v in value.items()
        }
    return output


_SPLITTABLE_QUARTER_DURATIONS = _convert_to_quarter_duration_splittables_dictionary(SPLITTABLES)


def _find_nearest_quantized_value(quantized_values, values):
    output = []
    for value in values:
        nearest_quantized = min(enumerate(quantized_values), key=lambda x: abs(x[1] - value))[1]
        delta = nearest_quantized - value
        output.append((nearest_quantized, delta))
    return output


def _find_q_delta(quantized_locations, values):
    qs = _find_nearest_quantized_value(quantized_locations, values)
    d = 0
    for q in qs:
        d += abs(q[1])
    return d


def _find_quantized_locations(duration, subdivision):
    output = range(subdivision + 1)
    fr = duration / subdivision
    output = [x * fr for x in output]
    return output


def get_chord_group_subdivision(chords):
    qds = [ch.quarter_duration for ch in chords if ch.quarter_duration != 0]
    if len(qds) == 1:
        return qds[0].denominator
    qd_sum = sum(qds)
    if qd_sum in [3 / 2, 3 / 4, 3, 6]:
        denominators = list(dict.fromkeys([qd.denominator for qd in qds]))
        l_c_m = lcm(denominators)
        if l_c_m not in [1, 2, 4, 8, 16]:
            raise NotImplementedError
        else:
            return l_c_m
    permitted_sums = [1 / 4, 1 / 2, 1, 2, 4, 8]
    if qd_sum not in permitted_sums:
        raise ValueError(f'sum of chords {qd_sum} must be in {permitted_sums}')
    qds = [qd / qd_sum for qd in qds]
    denominators = list(dict.fromkeys([qd.denominator for qd in qds]))
    if len(denominators) > 1:
        l_c_m = lcm(denominators)
        if l_c_m not in denominators and l_c_m > 16:
            return None
        else:
            return l_c_m
    else:
        return denominators[0]


def beam_chord_group(chord_group: List['Chord']) -> None:
    # print('setting beams', [ch.quarter_duration for ch in chord_group])
    """
    Function for setting beams of a list of chords (chord_group). This function is used to create or update beams inside a beat.
    Chord types must be set first.

    """
    chord_group = [ch for ch in chord_group if ch.quarter_duration != 0]
    for ch in chord_group:
        if ch.type is None:
            raise ChordTypeNotSetError('Beaming chord groups not possible if chord types are not set.')

    def remove_rests_from_both_ends(chords):
        is_rest_list = [ch.is_rest for ch in chords]
        if False not in is_rest_list:
            return []
        if True in is_rest_list:
            first_non_chord_index = is_rest_list.index(False)
            output = chords[first_non_chord_index:]
            is_rest_list = is_rest_list[first_non_chord_index:]
            if is_rest_list[-1] is True:
                last_non_chord_index = next(i for i in reversed((range(len(is_rest_list)))) if is_rest_list[i] is True)
                output = output[:last_non_chord_index]
            return output
        else:
            return chords

    chord_group = remove_rests_from_both_ends(chord_group)
    if not chord_group:
        return

    # valid values for XMLBeam are: 'begin', 'continue', 'end', 'forward hook', 'backward hook'
    def add_beam_to_chord(chord, number, value):
        if chord.beams is not None and not chord.beams.get(number):
            chord.set_beam(number, value)

    def add_last_beam(chord, last_number_of_beams, current_number_of_beams, cont=False):
        """
        cont=True will be for example used to continue one beam (eight beam) in the middle of the beat with 32nds.
        """
        if last_number_of_beams <= current_number_of_beams:
            if cont:
                add_beam_to_chord(chord, 1, 'continue')
                for num in range(2, last_number_of_beams + 1):
                    add_beam_to_chord(chord, num, 'end')
            else:
                for n in range(1, last_number_of_beams + 1):
                    add_beam_to_chord(chord, n, 'end')
        else:
            if current_number_of_beams != 0:
                if cont:
                    add_beam_to_chord(chord, 1, 'continue')
                    for n in range(2, current_number_of_beams + 1):
                        add_beam_to_chord(chord, n, 'end')
                else:
                    for n in range(1, current_number_of_beams + 1):
                        add_beam_to_chord(chord, n, 'end')
                for n in range(current_number_of_beams + 1, last_number_of_beams + 1):
                    add_beam_to_chord(chord, n, 'backward')

    current_number_of_beams = 0

    # adding all necessary beams to all notes save the notes of the last chord. For last chord add_last_beam() will be used.
    index = 0
    while index != len(chord_group) - 1:
        # print('index', index)
        # print('current', current_number_of_beams)
        chord = chord_group[index]
        next_chord = chord_group[index + 1]
        # types is a list of tuples with three values: (beam value, number of the begining beam, number of the ending beam)
        types = []
        b1, b2 = chord.number_of_beams, next_chord.number_of_beams
        # print(chord.quarter_duration, next_chord.quarter_duration)
        # print(b1, b2, current_number_of_beams)
        if chord.is_rest:
            pass
            'do nothing'
        else:
            if not b1:
                pass
                'do nothing'
            elif next_chord.is_rest:
                if current_number_of_beams == 0:
                    types.append(('begin', 1, 1))
                    if b1 > 1:
                        types.append(('forward', 1, b1))
                else:
                    types.append(('continue', 1, 1))
                    if b1 > 1:
                        if b1 <= current_number_of_beams:
                            types.append(('end', 2, b1))
                        else:
                            types.append(('end', 2, current_number_of_beams))
                            types.append(('forward', current_number_of_beams + 1, b1))

                current_number_of_beams = 1
            else:
                'do something regular'
                if b1 and not b2:
                    add_last_beam(chord, b1, current_number_of_beams)
                else:
                    if b2 < b1 <= current_number_of_beams:
                        # print('huhu')
                        types.append(('continue', 1, b2))
                        types.append(('end', b2 + 1, b1))
                    elif b2 < b1 > current_number_of_beams:
                        if current_number_of_beams == 0:
                            types.append(('begin', 1, b2))
                            types.append(('forward', b2 + 1, b1))
                        else:
                            if current_number_of_beams > b2:
                                types.append(('continue', 1, b2))
                                types.append(('end', b2 + 1, current_number_of_beams))
                                types.append(('backward', current_number_of_beams + 1, b1))
                            elif current_number_of_beams < b2:
                                types.append(('continue', 1, current_number_of_beams))
                                types.append(('begin', current_number_of_beams + 1, b2))
                                types.append(('forward', b2 + 1, b1))
                            else:
                                types.append(('continue', 1, b2))
                                types.append(('forward', b2 + 1, b1))
                            #
                            # if (chord.quarter_duration == QuarterDuration(1, 6) and chord.offset == QuarterDuration(1,
                            #                                                                                         3)
                            # ) or (
                            #         chord.quarter_duration == QuarterDuration(1, 8) and chord.offset == QuarterDuration(
                            #     3, 8)
                            # ):
                            #     types.append(('backward', b2 + 1, b1))
                            # else:
                            #     types.append(('forward', b2 + 1, b1))

                        # current_number_of_beams = b1
                    elif b2 == b1 <= current_number_of_beams:
                        types.append(('continue', 1, b1))
                        # current_number_of_beams = b1

                    elif b2 == b1 > current_number_of_beams:
                        if current_number_of_beams == 0:
                            types.append(('begin', 1, b2))
                        else:
                            types.append(('continue', 1, current_number_of_beams))
                            types.append(('begin', current_number_of_beams + 1, b2))

                    elif b2 > b1 <= current_number_of_beams:
                        types.append(('continue', 1, b1))

                    elif b2 > b1 > current_number_of_beams:
                        if current_number_of_beams == 0:
                            types.append(('begin', 1, b1))
                        else:
                            types.append(('continue', 1, current_number_of_beams))
                            types.append(('begin', current_number_of_beams + 1, b1))
        for t in types:
            for num in range(t[1], t[2] + 1):
                add_beam_to_chord(chord, num, t[0])
        if chord.beams:
            current_number_of_beams = len([v for v in chord.beams.values() if v in ['continue', 'begin']])
            # print('setting current to', current_number_of_beams)
        if index == len(chord_group) - 2 and b2:
            add_last_beam(next_chord, b2, current_number_of_beams)
        index += 1


class Beat(MusicTree, QuarterDurationMixin, QuantizeMixin, FinalizeMixin):
    """
    Parent type: :obj:`~musicscore.voice.Voice`

    Child type: :obj:`~musicscore.chord.Chord`

    Beat is the direct ancestor of chords. Each :obj:`~musicscore.chord.Chord` is placed with an offset between 0 and beat's
    quarter duration inside the beat as its child .

    Quarter duration of a beat's :obj:`~musicscore.chord.Chord` child can exceed its own quarter duration. If a
    :obj:`~musicscore.chord.Chord` is longer than the quarter duration of beat's parent :obj:`~musicscore.voice.Voice`,
    a leftover :obj:`~musicscore.chord.Chord` will be added as leftover property to the :obj:`~musicscore.voice.Voice` which will be added
    to next measure's appropriate voice .

    Beat manages splitting of each child :obj:`~musicscore.chord.Chord` into appropriate tied :obj:`~musicscore.chord.Chord` s if needed,
    for example if this chord has a non-writable quarter duration like 5/6.

    The dots and tuplets are also added here to :obj:`~musicscore.chord.Chord` or directly to their :obj:`~musicscore.note.Note` children.

    Beaming and quantization are also further important tasks of a beat.
    """

    _PERMITTED_DURATIONS = {4, 2, 1, 0.5}

    def __init__(self, quarter_duration=1):
        super().__init__(quarter_duration=quarter_duration)
        self._filled_quarter_duration = 0
        self.leftover_chord = None
        self._subdivision = None

    def _add_child(self, child):
        child._parent = self
        self._children.append(child)
        try:
            self.up.up.up.up.set_current_measure(staff_number=self.up.up.number, voice_number=self.up.number,
                                                 measure=self.up.up.up)
        except AttributeError:
            pass

    def _add_chord(self, chord=None):
        if chord is None:
            chord = Chord(midis=60, quarter_duration=self.quarter_duration)
        return self.add_child(chord)

    def _change_children_quarter_durations(self, quarter_durations):
        if len(quarter_durations) != len(self.get_children()):
            raise ValueError
        if sum(quarter_durations) != self.quarter_duration:
            raise ValueError
        for qd, ch in zip(quarter_durations, self.get_children()):
            ch._quarter_duration = qd

    def _check_permitted_duration(self, val):
        for d in self._PERMITTED_DURATIONS:
            if val == d:
                return
        raise BeatWrongDurationError(f"Beat's quarter duration {val} is not allowed.")

    def _get_quantized_locations(self, subdivision):
        return _find_quantized_locations(self.quarter_duration, subdivision)

    def _get_quantized_quarter_durations(self, quarter_durations):
        if sum(quarter_durations) != self.quarter_duration:
            raise ValueError(
                f"Sum of quarter_durations '{quarter_durations}: {sum(quarter_durations)}' is not equal to beat quarter_duration "
                f"'{self.quarter_duration}'")

        def _get_positions():
            output = [0]
            for i, qd in enumerate(quarter_durations):
                output.append(output[i] + qd)
            return output

        positions = _get_positions()
        permitted_divs = self.get_possible_subdivisions()[:]
        best_div = permitted_divs.pop(0)
        last_q_delta = _find_q_delta(self._get_quantized_locations(subdivision=best_div), positions)

        for div in permitted_divs:
            current_q_delta = _find_q_delta(self._get_quantized_locations(subdivision=div), positions)

            if current_q_delta < last_q_delta:
                best_div = div
                last_q_delta = current_q_delta

            elif (current_q_delta == last_q_delta) and (div < best_div):
                best_div = div

        quantized_positions = [f[0] for f in
                               _find_nearest_quantized_value(self._get_quantized_locations(subdivision=best_div),
                                                             positions)]

        quantized_durations = []

        for i in range(len(quarter_durations)):
            fr = Fraction(
                quantized_positions[i + 1] - quantized_positions[i]).limit_denominator(
                trunc(best_div / self.quarter_duration))
            quantized_durations.append(QuarterDuration(fr))
        return quantized_durations

    @staticmethod
    def _split_chord(chord, quarter_durations):
        output = [chord]
        chord._quarter_duration = quarter_durations[0]
        for qd in quarter_durations[1:]:
            copied = _split_copy(chord, qd)
            output.append(copied)
        for index, ch in enumerate(output[:-1]):
            next_ch = output[index + 1]
            ch.add_tie('start')
            next_ch.add_tie('stop')
            for midi in next_ch.midis:
                midi.accidental.show = False
        return output

    def _split_not_writable(self, chord, offset):
        if _SPLITTABLE_QUARTER_DURATIONS.get(offset) and _SPLITTABLE_QUARTER_DURATIONS.get(offset).get(
                chord.quarter_duration):
            quarter_durations = _SPLITTABLE_QUARTER_DURATIONS.get(offset).get(
                chord.quarter_duration)
            if quarter_durations:
                quarter_durations = [QuarterDuration(qd) for qd in quarter_durations]
                return self._split_chord(chord, quarter_durations)
        elif GENERALSPLITTABLES.get(chord.quarter_duration.numerator):
            quarter_durations = [QuarterDuration(x, chord.quarter_duration.denominator) for x in
                                 GENERALSPLITTABLES.get(chord.quarter_duration.numerator)]
            return self._split_chord(chord, quarter_durations)
        else:
            try:
                split_qds = SPLITTEXCEPTIONS.get(self.quarter_duration.value).get(self.get_subdivision()).get(
                    chord.quarter_duration.as_integer_ratio())
                if split_qds:
                    quarter_durations = [QuarterDuration(qd[0], qd[1]) for qd in split_qds]
                    return self._split_chord(chord, quarter_durations)
            except AttributeError:
                pass

    def _update_chord_types(self):
        for ch in self.get_chords():
            if not ch.type:
                if self.get_subdivision() and not ch.quarter_duration.beat_subdivision:
                    ch.quarter_duration.beat_subdivision = self.get_subdivision()
                try:
                    ch.type = ch.quarter_duration.get_type()
                except QuarterDurationIsNotWritable as err:
                    raise QuarterDurationIsNotWritable(
                        f'Chord {ch.get_coordinates_in_tree()} with offset {ch.offset}: {err} Consider setting type, number_of_dots and tuplet properties of the chord manually or splitting it into writable chords.')

    def _update_chord_number_of_dots(self):
        for ch in self.get_chords():
            if ch.number_of_dots is None:
                if self.get_subdivision() and not ch.quarter_duration.beat_subdivision:
                    ch.quarter_duration.beat_subdivision = self.get_subdivision()
                ch.number_of_dots = ch.quarter_duration.get_number_of_dots()

    def _update_chord_tuplets(self):
        if None not in {ch.tuplet for ch in self.get_chords()}:
            return
        if {ch.tuplet for ch in self.get_chords()} != {None}:
            raise BeatUpdateChordTupletsError(
                'Beat cannot manage tuplets automatically if it contains chords with manually set tuplet properties.')

        def _update_tuplets(chord_group, actual_notes, quarter_duration=1):
            if actual_notes <= 16 or actual_notes == 32:
                if actual_notes not in [1, 2, 4, 8, 16, 32]:
                    for chord in chord_group:
                        chord.tuplet = Tuplet(actual_notes=actual_notes, quarter_duration=quarter_duration)
                        if chord == chord_group[0]:
                            chord.tuplet.bracket_type = 'start'
                        elif chord == chord_group[-1]:
                            chord.tuplet.bracket_type = 'stop'
                        else:
                            pass
            else:
                raise NotImplementedError('tuplets of actual_notes > 16 cannot be implemented.')

        actual_notes = get_chord_group_subdivision(self.get_children())
        if not actual_notes:
            if self.quarter_duration == 1:
                grouped_chords = _group_chords(self.get_children(), [1 / 2, 1 / 2])
                if grouped_chords:
                    for g in grouped_chords:
                        actual_notes = get_chord_group_subdivision(g)
                        _update_tuplets(g, actual_notes, 1 / 2)
                    return
                else:
                    raise NotImplementedError(
                        'Beat cannot be halved. It cannot manage the necessary grouping of chords.')
            else:
                raise NotImplementedError(
                    'Beat with quarter_duration other than one cannot manage more than one group of chords.')

        _update_tuplets(self.get_children(), actual_notes, self.quarter_duration)

    def _update_chord_beams(self):
        chords = self.get_chords()
        if chords:
            ## update types
            for ch in chords:
                if ch.type is None:
                    self._update_chord_types()
            ## group chords
            chord_groups = None
            continue_eighth_beam = False
            # group inside beat
            if self.get_subdivision() == 8 and self.quarter_duration == 1:
                chord_groups = _group_chords(chords, [1 / 2, 1 / 2])
                if chord_groups and not 1 in {len(group) for group in chord_groups}:
                    continue_eighth_beam = True
                else:
                    chord_groups = None
            if not chord_groups:
                chord_groups = [chords]
            # break beams
            broken_chord_groups = []
            for group in chord_groups:
                split_indices = [index for index, chord in enumerate(group) if chord.broken_beam]
                for broken_group in split_list(group, split_indices):
                    broken_chord_groups.append(broken_group)
            # create beams
            for group in broken_chord_groups:
                beam_chord_group(group)
            # continue eighth beam
            if continue_eighth_beam and 1 not in {len(group) for group in broken_chord_groups}:
                for index, group in enumerate(broken_chord_groups):
                    if index < len(broken_chord_groups) - 1:
                        group[-1].beams[1] = 'continue'
                    if index > 0:
                        group[0].beams[1] = 'continue'

    def _remove_zero_quarter_durations(self):
        def _get_next_chord(chord):
            next_chord = chord.next
            if not next_chord:
                next_beat = chord.up.next
                while next_beat and not next_chord:
                    try:
                        next_chord = next_beat.get_children()[0]
                    except IndexError:
                        next_beat = next_beat.next
            if not next_chord:
                voice_number = chord.up.up.number
                staff_number = chord.up.up.up.number
                if not staff_number:
                    staff_number = 1
                next_measure = chord.up.up.up.up.next
                if next_measure:
                    next_measure_voice = next_measure.get_chord(staff_number=staff_number,
                                                                voice_number=voice_number)
                    if next_measure_voice:
                        next_beat = next_measure_voice.get_children()[0]
                        while next_beat and not next_chord:
                            try:
                                next_chord = next_beat.get_children()[0]
                            except IndexError:
                                next_beat = next_beat.next

            return next_chord

        def _get_previous_chord(chord):
            previous_chord = chord.previous
            if not previous_chord:
                previous_beat = chord.up.previous
                while previous_beat and not previous_chord:
                    try:
                        previous_chord = previous_beat.get_children()[-1]
                    except IndexError:
                        previous_beat = previous_beat.previous
            if not previous_chord:
                voice_number = chord.up.up.number
                staff_number = chord.up.up.up.number
                if not staff_number:
                    staff_number = 1
                previous_measure = chord.up.up.up.up.previous
                if previous_measure:
                    previous_measure_voice = previous_measure.get_chord(staff_number=staff_number,
                                                                        voice_number=voice_number)
                    if previous_measure_voice:
                        previous_beat = previous_measure_voice.get_children()[-1]
                        while previous_beat and not previous_chord:
                            try:
                                previous_chord = previous_beat.get_children()[-1]
                            except IndexError:
                                previous_beat = previous_beat.previous

            return previous_chord

        zeros = [ch for ch in self.get_children() if ch.quarter_duration == 0]
        for ch in zeros:
            if ch.all_midis_are_tied_to_next:
                next_chord = _get_next_chord(ch)
                # next_chord.add_lyric('I am next')
                if next_chord:
                    [m.remove_tie('stop') for m in next_chord.midis]
                    next_chord._xml_direction_types = ch._xml_direction_types
                    next_chord._xml_directions = ch._xml_directions
                    next_chord._xml_lyrics = ch._xml_lyrics
                    next_chord._xml_articulations = ch._xml_articulations
                    next_chord._xml_technicals = ch._xml_technicals
                    next_chord._xml_ornaments = ch._xml_ornaments
                    next_chord._xml_dynamics = ch._xml_dynamics
                    next_chord._xml_other_notations = ch._xml_other_notations
                    next_chord._note_attributes = ch._note_attributes
                ch.up.remove(ch)

            elif ch.all_midis_are_tied_to_previous:
                previous_chord = _get_previous_chord(ch)
                if previous_chord:
                    [m.remove_tie('start') for m in previous_chord.midis]
                ch.up.remove(ch)
            else:
                pass

    def _split_not_writable_chords(self) -> None:
        """
        This method checks if the quarter duration of all children chords must be split according to :obj:`~musicscore.beat.SPLITTABLES`
        dictionary. If chord's offset and its quarter duration exist in the dictionary a list of splitting quarter durations can be
        accessed like this: ``SPLITTABLES[chord.offset[chord.quarter_duration]]`` This dictionary can be manipulated by user during runtime
        if needed. Be careful with not writable quarter durations which have to be split (for example 5/6 must be split to 3/6,
        2/6 or some other writable quarter durations).

        :obj:`~musicscore.measure.Measure.finalize()` loops over all its beats calls this method.
        """
        for chord in self.get_children()[:]:
            split = self._split_not_writable(chord, chord.offset)
            if split:
                for ch in split:
                    ch._parent = self
                if chord == self.get_children()[-1]:
                    self._children = self.get_children()[:-1] + split
                else:
                    index = self.get_children().index(chord)
                    self._children = self.get_children()[:index] + split + self.get_children()[index + 1:]

    @property
    def is_filled(self) -> bool:
        """
        :return: ``True`` if no children can be added anymore. If ``False`` there is still room for further child or children.
        :rtype: bool
        """
        if self.filled_quarter_duration == self.quarter_duration:
            return True
        else:
            return False

    @property
    def filled_quarter_duration(self):
        """
        :return: How much of beat's quarter duration is already filled.
        :rtype: QuarterDuration
        """
        return self._filled_quarter_duration

    @property
    def number(self) -> int:
        """
        :return: Beat's number inside its parent's :obj:`musicscore.voice.Voice`
        :rtype: int
        """
        return self.up.get_children().index(self) + 1

    @property
    def offset(self) -> QuarterDuration:
        """
        :return: Offset in Beat's parent :obj:`musicscore.voice.Voice`
        :rtype: QuarterDuration
        """
        if not self.up:
            return None
        elif self.previous is None:
            return 0
        else:
            return self.previous.offset + self.previous.quarter_duration

    def add_child(self, child: Chord) -> List['Chord']:
        """
        If child's quarter duration is less than beat's remaining quarter duration: child is added to the beat.

        If child's quarter duration is greater than beat's remaining quarter duration: :obj:`~musicscore.chord.Chord`'s :obj:`~musicscore.chord.Chord._split_and_add_beatwise` is
        method called. It is possible to add a chord with a quarter duration exceeding the beat's quarter duration without splitting the chord.
        For example if the first beat in a 4/4 measure gets a chord with quarter duration 3, the chord will be added to this first beat as a
        child and the following two beats will be set to filled without having a child themselves and the parent
        :obj:`~musicscore.voice.Voice` returns the fourth beat if its :obj:`~musicscore.voice.Voice.get_current_beat` is called.

        If child's quarter duration exceeds the :obj:`~musicscore.voice.Voice`'s remaining quarter duration a leftover :obj:`~musicscore.chord.Chord` will be added to the voice and can be
        accessed when the next :obj:`~musicscore.measure.Measure` is created.

        :param child: :obj:`~musicscore.chord.Chord` to be added as child
        :return: list of split chords
        """
        if self._finalized is True:
            raise AlreadyFinalizedError(self, 'add_child')
        self._check_child_to_be_added(child)
        if not self.up:
            raise BeatHasNoParentError('A child Chord can only be added to a beat if it has a voice parent.')
        if child.quarter_duration is None:
            raise ChordHasNoQuarterDurationError('Chord with no quarter_duration cannot be added to Beat.')
        if not child.midis:
            raise ChordHasNoMidisError('Chord with no midis cannot be added to Beat.')
        if self.is_filled and child.quarter_duration != 0:
            raise BeatIsFullError()
        diff = child.quarter_duration - (self.quarter_duration - self.filled_quarter_duration)
        if diff <= 0:
            self._filled_quarter_duration += child.quarter_duration
            self._add_child(child)
            return [child]
        else:
            if child.split:
                remaining_quarter_duration = child.quarter_duration
                current_beat = self
                while remaining_quarter_duration and current_beat:
                    if current_beat.quarter_duration < remaining_quarter_duration:
                        current_beat._filled_quarter_duration += current_beat.quarter_duration
                        remaining_quarter_duration -= current_beat.quarter_duration
                        current_beat = current_beat.next
                    else:
                        current_beat._filled_quarter_duration += remaining_quarter_duration
                        break
                self._add_child(child)
                return [child]
            else:
                beats = self.up.get_children()[self.up.get_children().index(self):]
                return child._split_and_add_beatwise(beats)

    def add_chord(self, *args, **kwargs):
        raise AddChordError

    def fill_with_rests(self) -> None:
        """
        If :obj:`~musicscore.beat.Beat` is not filled, it will be filled with rest(s)
        """
        if not self.is_filled:
            self._add_chord(Chord(0, self.quarter_duration - sum([ch.quarter_duration for ch in self.get_chords()])))

    def finalize(self):
        """
        finalize can only be called once.

        - It calls finalize method of all :obj:`~musicscore.chord.Chord` children.

        - Following updates are triggered: _update_note_tuplets, _update_chord_beams, quantize_quarter_durations (if get_quantized is
          True), _split_not_writable_chords
        """
        if self._finalized:
            raise AlreadyFinalizedError(self)
        if self.is_filled is False:
            self.fill_with_rests()

        if self.get_children():
            self._update_chord_types()
            self._update_chord_number_of_dots()
            self._update_chord_tuplets()
            self._update_chord_beams()
            for chord in self.get_children():
                chord.finalize()

        self._finalized = True

    def get_subdivision(self):
        if self._subdivision is None:
            if not self.is_filled:
                raise BeatNotFullError()
            self._subdivision = get_chord_group_subdivision(self.get_chords())
        return self._subdivision

    def set_subdivision(self, val):
        self._subdivision = val

    def quantize_quarter_durations(self):
        """
        When called the positioning of children will be quantized according to :obj:`~musicscore.quantize.QuantizeMixin.get_possible_subdivisions()`
        This method is called by :obj:`~musicscore.measure.Measure`

        """
        if self.get_possible_subdivisions() and self.get_children():
            if get_chord_group_subdivision(self.get_children()) in self.get_possible_subdivisions():
                pass
            else:
                quarter_durations = [chord.quarter_duration for chord in self.get_children()]
                if len([d for d in quarter_durations if d != 0]) > 1:
                    self._change_children_quarter_durations(self._get_quantized_quarter_durations(quarter_durations))
                    self._remove_zero_quarter_durations()
