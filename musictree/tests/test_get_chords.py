from musictree.chord import Chord
from musictree.part import Part
from musictree.score import Score
from musictree.tests.util import IdTestCase


class TestGetChords(IdTestCase):
    def setUp(self):
        super().setUp()
        self.score = Score()
        p1 = self.score.add_child(Part('p1'))
        p2 = self.score.add_child(Part('p2'))
        p1.add_chord(Chord(60, 1))
        p1.add_chord(Chord(61, 3))
        p1.add_chord(Chord(62, 4))
        p1.add_chord(Chord(63, 2.5), voice_number=2)
        p1.add_chord(Chord(64, 1.5), voice_number=2)
        p2.add_chord(Chord(48, 8), staff_number=2, voice_number=2)

    def test_beat_get_chords(self):
        pass

    def test_voice_get_chords(self):
        v1111 = self.score.get_part(1).get_measure(1).get_staff(1).get_voice(1)
        v1112 = self.score.get_part(1).get_measure(1).get_staff(1).get_voice(2)
        v1121 = None
        v1122 = None
        v1211 = self.score.get_part(1).get_measure(2).get_staff(1).get_voice(1)
        v1212 = self.score.get_part(1).get_measure(2).get_staff(1).get_voice(2)
        v1221 = None
        v1222 = None
        v2111 = self.score.get_part(2).get_measure(1).get_staff(1).get_voice(1)
        v2112 = self.score.get_part(2).get_measure(1).get_staff(1).get_voice(2)
        v2121 = self.score.get_part(2).get_measure(1).get_staff(2).get_voice(1)
        v2122 = self.score.get_part(2).get_measure(1).get_staff(2).get_voice(2)
        v2211 = self.score.get_part(2).get_measure(2).get_staff(1).get_voice(1)
        v2212 = self.score.get_part(2).get_measure(2).get_staff(1).get_voice(2)
        v2221 = self.score.get_part(2).get_measure(2).get_staff(2).get_voice(1)
        v2222 = self.score.get_part(2).get_measure(2).get_staff(2).get_voice(2)

        chords = v1111.get_chords()
        assert [chord.midis[0].value for chord in chords] == [60, 61]
        assert [chord.quarter_duration for chord in chords] == [1, 3]

        chords = v1112.get_chords()
        assert [chord.midis[0].value for chord in chords] == [63, 63, 64, 64]
        assert [chord.quarter_duration for chord in chords] == [2, 0.5, 0.5, 1]

        chords = v1211.get_chords()
        assert [chord.midis[0].value for chord in chords] == [62]
        assert [chord.quarter_duration for chord in chords] == [4]

        assert v1212 is None

        chords = v2111.get_chords()
        assert [chord.midis[0].value for chord in chords] == []
        assert [chord.quarter_duration for chord in chords] == []

        assert v2112 is None

        chords = v2121.get_chords()
        assert [chord.midis[0].value for chord in chords] == []
        assert [chord.quarter_duration for chord in chords] == []

        chords = v2122.get_chords()
        assert [chord.midis[0].value for chord in chords] == [48]
        assert [chord.quarter_duration for chord in chords] == [4]

        chords = v2211.get_chords()
        assert [chord.midis[0].value for chord in chords] == []
        assert [chord.quarter_duration for chord in chords] == []

        assert v2212 is None

        chords = v2221.get_chords()
        assert [chord.midis[0].value for chord in chords] == []
        assert [chord.quarter_duration for chord in chords] == []

        chords = v2222.get_chords()
        assert [chord.midis[0].value for chord in chords] == [48]
        assert [chord.quarter_duration for chord in chords] == [4]

    def test_staff_get_chords(self):
        st111 = self.score.get_part(1).get_measure(1).get_staff(1)
        st121 = self.score.get_part(1).get_measure(2).get_staff(1)
        st211 = self.score.get_part(2).get_measure(1).get_staff(1)
        st221 = self.score.get_part(2).get_measure(2).get_staff(1)
        st212 = self.score.get_part(2).get_measure(1).get_staff(2)
        st222 = self.score.get_part(2).get_measure(2).get_staff(2)

        chords = st111.get_chords()
        assert [chord.midis[0].value for chord in chords] == [60, 61, 63, 63, 64, 64]
        assert [chord.quarter_duration for chord in chords] == [1, 3, 2, 0.5, 0.5, 1]

        chords = st121.get_chords()
        assert [chord.midis[0].value for chord in chords] == [62]
        assert [chord.quarter_duration for chord in chords] == [4]

        assert st211.get_chords() == []
        assert st221.get_chords() == []

        chords = st212.get_chords()
        assert [chord.midis[0].value for chord in chords] == [48]
        assert [chord.quarter_duration for chord in chords] == [4]

        chords = st222.get_chords()
        assert [chord.midis[0].value for chord in chords] == [48]
        assert [chord.quarter_duration for chord in chords] == [4]

    def test_part_get_chords(self):
        chords = self.score.get_part(1).get_chords()
        assert [chord.midis[0].value for chord in chords] == [60, 61, 63, 63, 64, 64, 62]
        assert [chord.quarter_duration for chord in chords] == [1, 3, 2, 0.5, 0.5, 1, 4]

    def test_score_get_chords(self):
        assert [ch.midis[0].value for ch in self.score.get_chords()] == [60, 61, 63, 63, 64, 64, 62, 48, 48]
        assert [ch.quarter_duration for ch in self.score.get_chords()] == [1, 3, 2, 0.5, 0.5, 1, 4, 4, 4]
