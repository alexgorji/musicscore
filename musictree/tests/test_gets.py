from unittest.mock import Mock, patch

from musictree.beat import Beat
from musictree.chord import Chord
from musictree.measure import Measure
from musictree.part import Part
from musictree.score import Score
from musictree.staff import Staff
from musictree.tests.util import IdTestCase
from musictree.voice import Voice


class TestGetPart(IdTestCase):
    def test_score_get_part(self):
        s = Score()
        p = s.add_child(Part('p1'))
        assert s.get_part(1) == p
        assert s.get_part(2) is None

    def test_part_get_part(self):
        p = Part('p1')
        with self.assertRaises(TypeError):
            p.get_part()

    def test_measure_get_part(self):
        m = Measure(1)
        with self.assertRaises(TypeError):
            m.get_part()

    def test_staff_get_part(self):
        st = Staff()
        with self.assertRaises(TypeError):
            st.get_part()

    def test_voice_get_part(self):
        v = Voice()
        with self.assertRaises(TypeError):
            v.get_part()

    def test_beat_get_part(self):
        b = Beat()
        with self.assertRaises(TypeError):
            b.get_part()

    def test_chord_get_part(self):
        ch = Chord()
        with self.assertRaises(TypeError):
            ch.get_part()


class TestGetMeasure(IdTestCase):
    def test_score_get_measure(self):
        s = Score()
        p = s.add_child(Part('p1'))
        m = p.add_child(Measure(1))
        assert p.get_measure(1) == m
        assert s.get_part(1).get_measure(1) == m
        assert s.get_measure(1, 1) == m
        assert s.get_measure(1, 2) is None
        assert s.get_measure(2, 2) is None

    def test_part_get_measure(self):
        p = Part('p1')
        m = p.add_child(Measure(1))
        assert p.get_measure(1) == m
        assert p.get_measure(2) is None

    def test_measure_get_measure(self):
        m = Measure(1)
        with self.assertRaises(TypeError):
            m.get_measure()

    def test_staff_get_measure(self):
        st = Staff()
        with self.assertRaises(TypeError):
            st.get_measure()

    def test_voice_get_measure(self):
        v = Voice()
        with self.assertRaises(TypeError):
            v.get_measure()

    def test_beat_get_measure(self):
        b = Beat()
        with self.assertRaises(TypeError):
            b.get_measure()

    def test_chord_get_measure(self):
        ch = Chord()
        with self.assertRaises(TypeError):
            ch.get_measure()


class TestGetStaff(IdTestCase):
    def test_score_get_staff(self):
        s = Score()
        p = s.add_child(Part('p1'))
        m = p.add_child(Measure(1))
        st = m.add_child(Staff())
        assert s.get_staff(1, 1, 1) == st
        assert s.get_staff(1, 2, 1) is None
        assert s.get_staff(2, 2, 1) is None

    def test_part_get_staff(self):
        p = Part('p1')
        m = p.add_child(Measure(1))
        st = m.add_child(Staff())
        assert p.get_staff(1, 1) == st
        assert p.get_staff(2, 1) is None

    def test_measure_get_staff(self):
        m = Measure(1)
        st = m.add_child(Staff())
        assert m.get_staff(1) == st
        assert m.get_staff(2) is None

    def test_staff_get_staff(self):
        st = Staff()
        with self.assertRaises(TypeError):
            st.get_staff()

    def test_voice_get_staff(self):
        v = Voice()
        with self.assertRaises(TypeError):
            v.get_staff()

    def test_beat_get_staff(self):
        b = Beat()
        with self.assertRaises(TypeError):
            b.get_staff()

    def test_chord_get_staff(self):
        ch = Chord()
        with self.assertRaises(TypeError):
            ch.get_staff()


class TestGetVoice(IdTestCase):
    def test_score_get_voice(self):
        s = Score()
        p1 = s.add_child(Part('p1'))
        m1 = p1.add_child(Measure(1))
        st1 = m1.add_child(Staff())
        v1 = st1.add_child(Voice())
        assert s.get_voice(1, 1, 1, 1) == v1

        p2 = s.add_child(Part('p2'))
        m2 = p2.add_measure()
        st2 = m2.get_children()[0]
        assert m2.get_staff(1) == st2

    def test_part_get_voice(self):
        p = Part('p1')
        m = p.add_child(Measure(1))
        st = m.add_child(Staff())
        v = st.add_child(Voice())
        assert p.get_voice(1, 1, 1) == v

    def test_measure_get_voice(self):
        m = Measure(1)
        st = m.add_child(Staff())
        v = st.add_child(Voice())
        assert m.get_voice(1, 1) == v

    @patch('musictree.measure.Measure')
    def test_staff_get_voice(self, mock_measure):
        st = Staff()
        st._parent = mock_measure
        v = st.add_child(Voice())
        assert st.get_voice(1) == v
        assert st.get_voice(2) is None

    def test_voice_get_voice(self):
        v = Voice()
        with self.assertRaises(TypeError):
            v.get_voice()

    def test_beat_get_voice(self):
        b = Beat()
        with self.assertRaises(TypeError):
            b.get_voice()

    def test_chord_get_voice(self):
        ch = Chord()
        with self.assertRaises(TypeError):
            ch.get_voice()


class TestGetBeat(IdTestCase):
    def test_score_get_beat(self):
        s = Score()
        p = s.add_child(Part('p1'))
        m = p.add_child(Measure(1))
        st = m.add_child(Staff())
        v = st.add_child(Voice())
        b = v.add_child(Beat())
        assert s.get_beat(1, 1, 1, 1, 1) == b

    def test_part_get_beat(self):
        p = Part('p1')
        m = p.add_child(Measure(1))
        st = m.add_child(Staff())
        v = st.add_child(Voice())
        b = v.add_child(Beat())
        assert p.get_beat(1, 1, 1, 1) == b

    def test_measure_get_beat(self):
        m = Measure(1)
        st = m.add_child(Staff())
        v = st.add_child(Voice())
        b = v.add_child(Beat())
        assert m.get_beat(1, 1, 1) == b

    @patch('musictree.measure.Measure')
    def test_staff_get_beat(self, mock_measure):
        st = Staff()
        st._parent = mock_measure
        v = st.add_child(Voice())
        b = v.add_child(Beat())
        assert st.get_beat(1, 1) == b
        assert st.get_beat(2, 2) is None

    @patch('musictree.staff.Staff')
    def test_voice_get_beat(self, mock_staff):
        v = Voice()
        v._parent = mock_staff
        b = v.add_child(Beat())
        assert v.get_beat(1) == b

    def test_beat_get_beat(self):
        b = Beat()
        with self.assertRaises(TypeError):
            b.get_beat()

    def test_chord_get_beat(self):
        ch = Chord()
        with self.assertRaises(TypeError):
            ch.get_beat()


class TestGetChord(IdTestCase):
    def test_score_get_chord(self):
        s = Score()
        p = s.add_child(Part('p1'))
        m = p.add_child(Measure(1))
        st = m.add_child(Staff())
        v = st.add_child(Voice())
        b = v.add_child(Beat())
        ch = b.add_child(Chord(60, 1))[0]
        assert s.get_chord(1, 1, 1, 1, 1, 1) == ch

    def test_part_get_chord(self):
        p = Part('p1')
        m = p.add_child(Measure(1))
        st = m.add_child(Staff())
        v = st.add_child(Voice())
        b = v.add_child(Beat())
        ch = b.add_child(Chord(60, 1))[0]
        assert p.get_chord(1, 1, 1, 1, 1) == ch

    def test_measure_get_chord(self):
        m = Measure(1)
        st = m.add_child(Staff())
        v = st.add_child(Voice())
        b = v.add_child(Beat())
        ch = b.add_child(Chord(60, 1))[0]
        assert m.get_chord(1, 1, 1, 1) == ch

    @patch('musictree.measure.Measure')
    def test_staff_get_chord(self, mock_measure):
        st = Staff()
        st._parent = mock_measure
        v = st.add_child(Voice())
        b = v.add_child(Beat())
        ch = b.add_child(Chord(60, 1))[0]
        assert st.get_chord(1, 1, 1) == ch

    @patch('musictree.staff.Staff')
    def test_voice_get_chord(self, mock_staff):
        v = Voice()
        v._parent = mock_staff
        b = v.add_child(Beat())
        ch = b.add_child(Chord(60, 1))[0]
        assert v.get_chord(1, 1) == ch

    @patch('musictree.voice.Voice')
    def test_beat_get_chord(self, mock_voice):
        b = Beat()
        b._parent = mock_voice
        ch = b.add_child(Chord(60, 1))[0]
        assert b.get_chord(1) == ch

    def test_chord_get_chord(self):
        ch = Chord()
        with self.assertRaises(TypeError):
            ch.get_chord()


class TestGetBeats(IdTestCase):
    def test_score_get_beats(self):
        s = Score()
        p = s.add_child(Part('p1'))
        m = p.add_child(Measure(1))
        st = m.add_child(Staff())
        v = st.add_child(Voice())
        b1 = v.add_child(Beat())
        b2 = v.add_child(Beat())
        assert s.get_beats() == [b1, b2]

    def test_part_get_beats(self):
        p = Part('p1')
        m = p.add_child(Measure(1))
        st = m.add_child(Staff())
        v = st.add_child(Voice())
        b1 = v.add_child(Beat())
        b2 = v.add_child(Beat())
        assert p.get_beats() == [b1, b2]

    def test_measure_get_beats(self):
        m = Measure(1)
        st = m.add_child(Staff())
        v = st.add_child(Voice())
        b1 = v.add_child(Beat())
        b2 = v.add_child(Beat())
        assert m.get_beats() == [b1, b2]

    @patch('musictree.measure.Measure')
    def test_staff_get_beats(self, mock_measure):
        st = Staff()
        st._parent = mock_measure
        v = st.add_child(Voice())
        b1 = v.add_child(Beat())
        b2 = v.add_child(Beat())
        assert st.get_beats() == [b1, b2]

    @patch('musictree.staff.Staff')
    def test_voice_get_beats(self, mock_staff):
        v = Voice()
        v._parent = mock_staff
        b1 = v.add_child(Beat())
        b2 = v.add_child(Beat())
        assert v.get_beats() == [b1, b2]

    def test_beat_get_beats(self):
        b = Beat()
        with self.assertRaises(TypeError):
            b.get_beats()

    def test_chord_get_beats(self):
        ch = Chord()
        with self.assertRaises(TypeError):
            ch.get_beats()
