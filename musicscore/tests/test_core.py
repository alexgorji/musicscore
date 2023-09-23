from musicscore import Score
from musicscore.tests.util import IdTestCase


class TestCore(IdTestCase):
    def setUp(self):
        super().setUp()
        self.score = Score()
        self.parts = [self.score.add_part(x) for x in ['p1', 'p2', 'p3']]
        self.measures = [self.parts[0].add_measure() for _ in range(3)]
        self.staves = [self.measures[0].get_children()[0]] + [self.measures[0].add_staff() for _ in range(3)]
        self.voices = [self.staves[0].get_children()[0]] + [self.staves[0].add_voice() for _ in range(3)]
        self.beats = self.voices[0].get_children()

    def test_score_get_descendents(self):
        for i in range(3):
            assert self.score.get_part(i + 1) == self.parts[i]
            assert self.score.get_part(part_number=i + 1) == self.parts[i]

        for i in range(3):
            assert self.score.get_measure(1, i + 1) == self.measures[i]
            assert self.score.get_measure(part_number=1, measure_number=i + 1) == self.measures[i]

        for i in range(4):
            assert self.score.get_staff(1, 1, i + 1) == self.staves[i]
            assert self.score.get_staff(part_number=1, measure_number=1, staff_number=i + 1) == self.staves[i]

        for i in range(4):
            assert self.score.get_voice(1, 1, 1, i + 1) == self.voices[i]
            assert self.score.get_voice(part_number=1, measure_number=1, staff_number=1, voice_number=i + 1) == \
                   self.voices[i]

        for i in range(4):
            assert self.score.get_beat(1, 1, 1, 1, i + 1) == self.beats[i]
            assert self.score.get_beat(part_number=1, measure_number=1, staff_number=1, voice_number=1,
                                       beat_number=i + 1) == self.beats[i]

    def test_part_get_descendents(self):
        first_part = self.parts[0]
        for i in range(3):
            assert first_part.get_measure(i + 1) == self.measures[i]
            assert first_part.get_measure(measure_number=i + 1) == self.measures[i]

        for i in range(4):
            assert first_part.get_staff(1, i + 1) == self.staves[i]
            assert first_part.get_staff(measure_number=1, staff_number=i + 1) == self.staves[i]

        for i in range(4):
            assert first_part.get_voice(1, 1, i + 1) == self.voices[i]
            assert first_part.get_voice(measure_number=1, staff_number=1, voice_number=i + 1) == \
                   self.voices[i]

        for i in range(4):
            assert first_part.get_beat(1, 1, 1, i + 1) == self.beats[i]
            assert first_part.get_beat(measure_number=1, staff_number=1, voice_number=1,
                                       beat_number=i + 1) == self.beats[i]

    def test_measure_get_descendents(self):
        first_measure = self.measures[0]

        for i in range(4):
            assert first_measure.get_staff(i + 1) == self.staves[i]
            assert first_measure.get_staff(staff_number=i + 1) == self.staves[i]

        for i in range(4):
            assert first_measure.get_voice(1, i + 1) == self.voices[i]
            assert first_measure.get_voice(staff_number=1, voice_number=i + 1) == \
                   self.voices[i]

        for i in range(4):
            assert first_measure.get_beat(1, 1, i + 1) == self.beats[i]
            assert first_measure.get_beat(staff_number=1, voice_number=1,
                                          beat_number=i + 1) == self.beats[i]

    def test_staff_get_descendents(self):
        first_staff = self.staves[0]

        for i in range(4):
            assert first_staff.get_voice(i + 1) == self.voices[i]
            assert first_staff.get_voice(voice_number=i + 1) == \
                   self.voices[i]

        for i in range(4):
            assert first_staff.get_beat(1, i + 1) == self.beats[i]
            assert first_staff.get_beat(voice_number=1,
                                        beat_number=i + 1) == self.beats[i]

    def test_voice_get_descendents(self):
        first_voice = self.voices[0]
        for i in range(4):
            assert first_voice.get_beat(i + 1) == self.beats[i]
            assert first_voice.get_beat(beat_number=i + 1) == self.beats[i]

    def test_wrong_number_of_arguments_or_keys(self):
        with self.assertRaises(ValueError):
            self.score.get_beat(1)
        with self.assertRaises(ValueError):
            self.parts[0].get_beat(1)
        with self.assertRaises(ValueError):
            self.measures[0].get_beat(voice_number=2, beat_number=1)
        with self.assertRaises(ValueError):
            self.measures[0].get_beat(measure_number=1, beat_number=2)

    def test_wrong_value(self):
        with self.assertRaises(TypeError):
            self.measures[0].get_staff(0)
        with self.assertRaises(TypeError):
            self.measures[0].get_staff(-1)
        with self.assertRaises(TypeError):
            self.measures[0].get_voice(staff_number=1, voice_number=-2)
