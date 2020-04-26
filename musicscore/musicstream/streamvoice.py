from musicscore.basic_functions import dToX, xToD
from musicscore.musictree.midi import Midi
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treeclef import TREBLE_CLEF, BASS_CLEF, LOW_BASS_CLEF, HIGH_TREBLE_CLEF
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treepart import TreePart
from musicscore.musicxml.groups.common import Voice
from musicscore.musicxml.types.simple_type import PositiveInteger


class StreamVoice(object):

    def __init__(self, voice_number=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._chords = []
        self._voice = None
        self.voice_number = voice_number

    # //private methods

    # //public properties
    @property
    def chords(self):
        return self._chords

    @property
    def voice_number(self):
        return self._voice

    @voice_number.setter
    def voice_number(self, value):
        PositiveInteger(value)
        self._voice = value

    # //public methods
    # add
    def add_chord(self, chord):
        chord.voice_number = self.voice_number
        self._chords.append(chord)

    def add_to_part(self, part, chords=None, staff_number=None):
        if chords is None:
            chords = self.chords
        for i in range(len(chords)):
            chord = chords[i]
            remain = part.add_chord(chord, self.voice_number, staff_number)
            if remain:
                remaining_chords = [remain] + chords[i + 1:]
                return remaining_chords

    def add_to_score(self, score, part_number=1, staff_number=None, first_measure=1):

        measure_number = first_measure

        def _get_measure():
            try:
                measure = score.get_children_by_type(TreeMeasure)[measure_number - 1]
            except IndexError:
                measure = score.add_measure()

            return measure

        measure = _get_measure()
        for i in range(part_number - len(measure.get_children_by_type(TreePart))):
            score.add_part()

        def _add_to_part(chords=None):
            part = measure.get_children_by_type(TreePart)[part_number - 1]
            remain = self.add_to_part(part, chords, staff_number)
            return remain

        remain = _add_to_part()

        while remain:
            measure_number += 1
            measure = _get_measure()
            remain = _add_to_part(remain)


class SimpleFormat(object):
    def __init__(self, quarter_durations=None, midis=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._quarter_durations = None
        self._midis = None
        self._set_quarter_durations(quarter_durations)
        self._set_midis(midis)
        self._chords = None

    # //private methods
    @staticmethod
    def _check_quarter_duration(quarter_durations):
        for quarter_duration in quarter_durations:
            if quarter_duration < 0:
                raise ValueError('SimpleFormat(): wrong duration {}'.format(quarter_duration))

    def _generate_chords(self):
        if self._quarter_durations == [] and self._midis == []:
            pass
        else:
            self._chords = []
            for i in range(len(self._quarter_durations) - len(self._midis)):
                self._midis.append(71)

            for i in range(len(self._midis) - len(self._quarter_durations)):
                self._quarter_durations.append(1)

            for d, m in zip(self._quarter_durations, self._midis):
                self._chords.append(TreeChord(m, d))

    def _set_midis(self, midis):
        def _is_value(x):
            try:
                float(x)
                return True
            except (ValueError, TypeError):
                return False

        def _is_midi(x):
            if isinstance(x, Midi):
                return True
            else:
                return False

        if midis is None:
            midis = []
        else:
            try:
                midis = list(midis)
            except TypeError:
                midis = [midis]

        self._midis = []
        for m in midis:
            if _is_midi(m):
                self._midis.append(m)
            elif _is_value(m):
                self._midis.append(Midi(m))
            elif isinstance(m, list) or isinstance(m, tuple):
                tmp = []

                for midi in m:
                    if _is_midi(midi):
                        tmp.append(midi)
                    elif _is_value(midi):
                        tmp.append(Midi(midi))
                    else:
                        raise TypeError
                self._midis.append(tmp)
            else:
                raise TypeError

    def _set_quarter_durations(self, quarter_durations):
        if quarter_durations is None:
            quarter_durations = []
        else:
            try:
                quarter_durations = list(quarter_durations)
            except TypeError:
                quarter_durations = [quarter_durations]

        self._check_quarter_duration(quarter_durations)

        self._quarter_durations = quarter_durations

    # //public properties
    @property
    def chords(self):
        if self._chords is None:
            self._generate_chords()
        return self._chords

    @property
    def quarter_duration(self):
        return sum([chord.quarter_duration for chord in self.chords])

    @property
    def midis(self):
        return [chord.midis for chord in self.chords]

    # //public methods

    # add
    def add_chord(self, chord):
        if self._chords is None:
            self._chords = []
        if chord.get_children_by_type(Voice):
            raise Exception('SimpleFormat Chords cannot have a voice child.')
        self._chords.append(chord)
        return chord

    # get
    def get_chord_dict(self, attribute):
        output = {}
        for chord in self.chords:
            try:
                output[chord] = getattr(chord, attribute)
            except AttributeError:
                output[chord] = None
        return output

    def get_midis(self):
        return [chord.midis for chord in self.chords]

    def get_quarter_durations(self):
        return [chord.quarter_duration for chord in self.chords]

    def get_quarter_positions(self):
        return dToX(self.get_quarter_durations())

    # //other

    def auto_clef(self, clefs=None):
        if not clefs:
            clefs = [TREBLE_CLEF, BASS_CLEF, HIGH_TREBLE_CLEF, LOW_BASS_CLEF]
        current_clefs = []
        chords = self.chords

        def _get_possible_clefs(midi):
            output = []
            for clef in clefs:
                clef_in_range = False
                if None not in clef.optimal_range:
                    if clef.optimal_range[0] <= midi <= clef.optimal_range[1]:
                        clef_in_range = True
                elif clef.optimal_range[0] and clef.optimal_range[0] <= midi:
                    clef_in_range = True
                elif clef.optimal_range[1] and midi <= clef.optimal_range[1]:
                    clef_in_range = True
                if clef_in_range:
                    output.append(clef)
            return output

        for chord in [chord for chord in chords if not chord.is_rest]:
            try:
                last_clef = current_clefs[-1]
            except IndexError:
                last_clef = None
            midi = chord.midis[0]
            possible_clefs = _get_possible_clefs(midi)
            if not possible_clefs:
                raise ValueError(
                    'no possible clef war found for midi {} with value {}. Change clefs or optimal_range '
                    'of clefs.'.format(midi, midi.value))
            if not last_clef or last_clef not in possible_clefs:
                clef = possible_clefs[0]
            else:
                clef = None

            if clef and clef != last_clef:
                chord.add_clef(clef)
                current_clefs.append(clef)

    def change_chords(self, function):
        for chord in self.chords:
            function(chord)

    def extend(self, simple_format):
        # self.chords
        for chord in simple_format.chords:
            self.add_chord(chord)

    def mirror(self, pivot=None):
        if pivot is None:
            pivot = self.chords[0].midis[0]
        elif not isinstance(pivot, Midi):
            pivot = Midi(pivot)
        else:
            pass

        for midi in [m for ch in self.chords for m in ch.midis]:
            transposition_interval = (pivot.value - midi.value) * 2
            midi.transpose(transposition_interval)

    def multiply_quarter_durations(self, factor):
        for chord in self.chords:
            chord.quarter_duration *= factor

    @staticmethod
    def sum(*simple_formats, no_doubles=False):
        def _copied_position_dict(sf):
            output = {}
            for chord, position in zip(sf.chords, sf.get_quarter_positions()):
                output[position] = chord.__deepcopy__()
            return output

        def _key_sorted_dict(dict):
            output = {}
            for key in sorted(dict.keys()):
                output[key] = dict[key]
            return output

        def _trim_quarter_durations():
            quarter_durations = xToD(list(all_positioned_chords.keys()))
            chords = all_positioned_chords.values()
            for quarter_duration, chord in zip(quarter_durations, chords):
                chord.quarter_duration = quarter_duration

        all_positioned_chords = _copied_position_dict(simple_formats[0])
        for sf in simple_formats[1:]:
            other_positioned_chords = _copied_position_dict(sf)
            for other_position, other_chord in other_positioned_chords.items():
                if other_position in all_positioned_chords.keys():
                    chord = all_positioned_chords[other_position]
                    if chord.is_rest:
                        all_positioned_chords[other_position] = chord
                    elif not other_chord.is_rest:
                        for midi in other_chord.midis:
                            if not no_doubles or midi.value not in [m.value for m in chord.midis]:
                                chord.add_midi(midi)
                    else:
                        pass
                else:
                    all_positioned_chords[other_position] = other_chord
        all_positioned_chords = _key_sorted_dict(all_positioned_chords)
        _trim_quarter_durations()
        output = SimpleFormat()
        for chord in all_positioned_chords.values():
            output.add_chord(chord)
        return output

    def retrograde(self):
        self._chords = list(reversed(self.chords))

    def to_stream_voice(self, voice_number=1):
        output = StreamVoice(voice_number)
        for chord in self.chords:
            output.add_chord(chord.__deepcopy__())
        return output

    def transpose(self, interval_midi):
        if isinstance(interval_midi, Midi):
            interval = interval_midi.value - self.chords[0].midis[0].value
        else:
            interval = interval_midi
        for ch in self.chords:
            ch.transpose(interval)

    # //copy

    def __deepcopy__(self, memodict=None):
        output = SimpleFormat()
        for chord in self.chords:
            output.add_chord(chord.deepcopy_for_SimpleFormat())
        return output
