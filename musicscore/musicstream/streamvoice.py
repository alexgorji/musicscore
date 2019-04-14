from musicscore.musictree.midi import Midi
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treepart import TreePart
from musicscore.musicxml.common.common import Voice
from musicscore.musicxml.types.simple_type import PositiveInteger


class StreamVoice(object):
    """"""

    def __init__(self, voice=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._chords = []
        self._voice = None
        self.voice = voice

    @property
    def chords(self):
        return self._chords

    @property
    def voice(self):
        return self._voice

    @voice.setter
    def voice(self, value):
        PositiveInteger(value)
        self._voice = value

    def add_chord(self, chord):
        chord.add_child(Voice(str(self.voice)))
        self._chords.append(chord)

    def add_to_score(self, score, part_number, first_measure=1):
        measure_index = first_measure - 1
        for chord in self.chords:
            try:
                measure = score.get_children_by_type(TreeMeasure)[measure_index]
            except IndexError:
                measure = score.add_measure()

            for i in range(part_number - len(measure.get_children_by_type(TreePart))):
                score.add_part()

            part = measure.get_children_by_type(TreePart)[part_number - 1]

            remain = part.add_chord(chord)
            if remain:
                measure_index += 1
                self.add_to_score(score, part_number, first_measure=measure_index + 1)


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
        if midis is None:
            midis = []
        else:
            try:
                midis = list(midis)
            except TypeError:
                midis = [midis]

        self._midis = [Midi(m) for m in midis]

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

    def to_voice(self, voice_number=1):
        output = StreamVoice(voice_number)
        for chord in self.chords:
            output.add_chord(chord)
        return output
