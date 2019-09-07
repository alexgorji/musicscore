from musicscore.musictree.midi import Midi
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treeclef import TREBLE_CLEF, BASS_CLEF, HIGH_TREBLE_CLEF, LOW_BASS_CLEF
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treepart import TreePart
from musicscore.musicxml.groups.common import Voice
from musicscore.musicxml.types.simple_type import PositiveInteger


class StreamVoice(object):
    """"""

    def __init__(self, voice_number=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._chords = []
        self._voice = None
        self.voice_number = voice_number

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

    def add_chord(self, chord):
        chord.voice_number = self.voice_number
        self._chords.append(chord)

    def add_to_part(self, part, chords=None):
        if chords is None:
            chords = self.chords

        for i in range(len(chords)):
            chord = chords[i]
            remain = part.add_chord(chord, self.voice_number)
            if remain:
                remaining_chords = [remain] + chords[i + 1:]
                return remaining_chords

    def add_to_score(self, score, first_measure=1, part_number=1):
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
            remain = self.add_to_part(part, chords)
            return remain

        remain = _add_to_part()

        while remain:
            measure_number += 1
            measure = _get_measure()
            remain = _add_to_part(remain)


class StreamChordFormula(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def condition(self, chord):
        pass

    def change_chord(self, chord):
        pass


class SimpleFormat(object):
    def __init__(self, durations=None, midis=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._durations = None
        self._midis = None
        self._set_durations(durations)
        self._set_midis(midis)
        self._chords = None

    @property
    def durations(self):
        return [chord.quarter_duration for chord in self.chords]
        # return self._durations

    @property
    def midis(self):
        return [chord.midis for chord in self.chords]

    @property
    def chords(self):
        if self._chords is None:
            self._generate_chords()
        return self._chords

    @staticmethod
    def _check_duration(durations):
        for duration in durations:
            if duration < 0:
                raise ValueError('SimpleFormat(): wrong duration {}'.format(duration))

    def _set_durations(self, durations):
        if durations is None:
            durations = []
        else:
            try:
                durations = list(durations)
            except TypeError:
                durations = [durations]

        self._check_duration(durations)

        self._durations = durations

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

    def get_durations(self):
        return [chord.duration for chord in self.chords]

    def get_midis(self):
        return [chord.midis for chord in self.chords]

    def _generate_chords(self):
        if self._durations == [] and self._midis == []:
            pass
        else:
            self._chords = []
            for i in range(len(self._durations) - len(self._midis)):
                self._midis.append(71)

            for i in range(len(self._midis) - len(self._durations)):
                self._durations.append(1)

            for d, m in zip(self._durations, self._midis):
                self._chords.append(TreeChord(m, d))

    def add_chord(self, chord):
        if self._chords is None:
            self._chords = []
        if chord.get_children_by_type(Voice):
            raise Exception('SimpleFormat Chords cannot have a voice child.')
        self._chords.append(chord)
        return chord

    def to_stream_voice(self, voice_number=1):
        output = StreamVoice(voice_number)
        for chord in self.chords:
            output.add_chord(chord.__deepcopy__())
            # output.add_chord(chord)
        return output

    def __deepcopy__(self, memodict={}):
        output = SimpleFormat()
        for chord in self.chords:
            output.add_chord(chord.deepcopy_for_SimpleFormat())
        return output

    def auto_clef(self):
        clefs = []
        chords = self.chords

        # ranges
        high_treble = (87, 120)
        treble = (67, 86.5)
        treble_bass = (56, 66.5)
        bass = (36, 55.5)
        low_bass = (20, 35.5)

        for chord in [chord for chord in chords if not chord.is_rest]:
            try:
                last_clef = clefs[-1]
            except IndexError:
                last_clef = None

            if high_treble[0] <= chord.midis[0].value <= high_treble[1]:
                clef = HIGH_TREBLE_CLEF
            elif treble[0] <= chord.midis[0].value <= treble[1]:
                clef = TREBLE_CLEF
            elif treble_bass[0] <= chord.midis[0].value <= treble_bass[1]:
                if last_clef == LOW_BASS_CLEF:
                    clef = BASS_CLEF
                elif not last_clef or last_clef == HIGH_TREBLE_CLEF:
                    clef = TREBLE_CLEF
                else:
                    clef = None

            elif bass[0] <= chord.midis[0].value <= bass[1]:
                clef = BASS_CLEF
            elif low_bass[0] <= chord.midis[0].value <= low_bass[1]:
                clef = LOW_BASS_CLEF
            else:
                raise ValueError('midi {} not in clef ranges'.format(chord.midis[0].value))

            if clef and clef != last_clef:
                chord.add_clef(clef)
                clefs.append(clef)

    def change_chord(self, *chord_formulas):
        for formula in chord_formulas:
            if not isinstance(formula, StreamChordFormula):
                raise TypeError

        for chord in self.chords:
            for formula in chord_formulas:
                if formula.condition(chord):
                    formula.change_chord(chord)
                    break

    def extend(self, simple_format):
        # self.chords
        for chord in simple_format.chords:
            self.add_chord(chord)

    def transpose(self, interval):
        for ch in self.chords:
            ch.transpose(interval)
