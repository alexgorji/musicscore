import inspect

from musicscore import Score, Part, Time, Chord, C
from musicscore.tests.util import IdTestCase, generate_repetitions, generate_path
from musicscore.util import _chord_is_in_a_repetition


# MyXMLTestSuite test_cautionary

class TestShowAccidentalSigns(IdTestCase):
    def setUp(self):
        super().setUp()
        self.score = Score()
        self.part = self.score.add_part('part')
        self.measure_1 = self.part.add_measure()
        self.measure_2 = self.part.add_measure()
        self.staff_1_1 = self.measure_1.add_staff()
        self.staff_1_2 = self.measure_1.add_staff()
        self.staff_2_1 = self.measure_2.add_staff()
        self.staff_2_2 = self.measure_2.add_staff()
        self.voice_1_1_1 = self.staff_1_1.add_voice()
        self.voice_1_1_2 = self.staff_1_1.add_voice()
        self.voice_2_1_1 = self.staff_2_1.add_voice()
        self.voice_2_1_2 = self.staff_2_1.add_voice()
        all_names = ['score', 'part', 'measure_1', 'measure_2', 'staff_1_1', 'staff_1_2', 'staff_2_1', 'staff_2_2',
                     'voice_1_1_2', 'voice_2_1_1', 'voice_2_1_2']
        self.all = [eval(f"self.{name}", {'self': self}) for name in all_names]

    def reset_show_signs(self):
        for obj in self.all:
            obj.show_accidental_signs = None

    def test_show_accidental_signs_property(self):
        for obj in self.all:
            assert obj.show_accidental_signs == 'modern'
        self.score.show_accidental_signs = 'traditional'
        for obj in self.all:
            assert obj.show_accidental_signs == 'traditional'
        self.part.show_accidental_signs = 'modern'
        assert self.score.show_accidental_signs == 'traditional'
        for obj in self.all:
            if obj != self.score:
                assert obj.show_accidental_signs == 'modern'

        self.reset_show_signs()
        self.score.show_accidental_signs = 'traditional'
        for obj in self.all:
            assert obj.show_accidental_signs == 'traditional'

        self.measure_1.show_accidental_signs = 'modern'

        for obj in self.all:
            if obj in [self.score, self.part, self.measure_2, self.staff_2_1, self.staff_2_2, self.voice_2_1_1,
                       self.voice_2_1_2]:
                assert obj.show_accidental_signs == 'traditional'
            else:
                assert obj.show_accidental_signs == 'modern'

    def test_show_accidental_signs_repetition_signs_simple(self):
        s = Score()
        p = s.add_part('p1')
        p.add_measure(Time(3, 4))
        for qd in 3 * [1]:
            p.add_chord(Chord(C(5, '#'), qd))
        s.export_xml(generate_path(inspect.currentframe()))
        for index, chord in enumerate(p.get_chords()):
            if index == 0:
                assert _chord_is_in_a_repetition(chord) is False
            else:
                assert _chord_is_in_a_repetition(chord) is True

        for index, chord in enumerate(p.get_chords()):
            if index == 0:
                assert chord.midis[0].accidental.show is True
            else:
                assert chord.midis[0].accidental.show is False
