from unittest.mock import patch, Mock

from musicscore.accidental import Accidental
from musicscore.beat import Beat
from musicscore.chord import Chord
from musicscore.measure import Measure
from musicscore.midi import Midi
from musicscore.musictree import MusicTree
from musicscore.note import Note
from musicscore.part import Part
from musicscore.score import Score
from musicscore.staff import Staff
from musicscore.tests.util import IdTestCase
from musicscore.voice import Voice


class TestMusicTree(IdTestCase):
    @patch.object(Chord, 'get_voice_number')
    @patch.object(Chord, 'get_staff_number')
    def test_add_child_type(self, mock_get_voice_number, mock_get_staff_number):
        mock_get_voice_number.return_value = 1
        mock_get_staff_number.return_value = None
        s = Score()
        p = Part('P1')
        m = Measure(1)
        st = Staff()
        v = Voice()
        b = Beat()
        c = Chord(60, 1)
        mi = c.add_midi(Midi(60))
        n = Note(midi=mi)
        acc = Accidental()
        assert p == s.add_child(p)
        assert m == p.add_child(m)
        assert st == m.add_child(st)
        assert v == st.add_child(v)
        assert b == v.add_child(b)
        assert c == b.add_child(c)[0]
        assert n == c._add_child(n)
        assert mi == n.add_child(mi)
        assert acc == mi.add_child(acc)

        objects = [s, m, st, v, b, n, mi]
        for parent in objects:
            with self.assertRaises(TypeError):
                parent.add_child(s)
        for parent in objects:
            if parent != s:
                with self.assertRaises(TypeError):
                    parent.add_child(p)
        for parent in objects:
            if parent != p:
                with self.assertRaises(TypeError):
                    parent.add_child(m)

        for child in objects:
            with self.assertRaises(NotImplementedError):
                acc.add_child(child)

    def test_check_args_kwargs(self):
        with self.assertRaises(ValueError):
            MusicTree()._check_args_kwargs(args=[1, 2, 3], kwargs={'part_number': 2}, class_name='Score')
        kwargs = MusicTree()._check_args_kwargs(args=[1, 2, 3], kwargs={}, class_name='Score', get_class_name='Staff')
        assert kwargs == {'part_number': 1, 'measure_number': 2, 'staff_number': 3}
        kwargs = MusicTree()._check_args_kwargs(args=[], kwargs={'part_number': 1, 'measure_number': 2, 'staff_number': 3},
                                                class_name='Score', get_class_name='Staff')
        assert kwargs == {'part_number': 1, 'measure_number': 2, 'staff_number': 3}
        with self.assertRaises(ValueError):
            MusicTree()._check_args_kwargs(args=[], kwargs={'part_number': 1, 'measure_number': 2, 'beat_number': 3}, class_name='Score')

        kwargs = MusicTree()._check_args_kwargs(args=[1, 2, 3], kwargs={}, class_name='Measure', get_class_name='Beat')
        assert kwargs == {'staff_number': 1, 'voice_number': 2, 'beat_number': 3}
        with self.assertRaises(ValueError):
            MusicTree()._check_args_kwargs(args=[1, 2, 3], kwargs={}, class_name='Measure', get_class_name='Voice')

    def test_get_type_errors(self):
        p = Part('p3')
        m = Measure(1)
        s = Staff()
        v = Voice()
        b = Beat()
        c = Chord(60, 1)
        for object_ in [p, m, s, v, b, c]:
            with self.assertRaises(TypeError):
                object_.get_part()

        for object_ in [m, s, v, b, c]:
            with self.assertRaises(TypeError):
                object_.get_measure()

        for object_ in [s, v, b, c]:
            with self.assertRaises(TypeError):
                object_.get_staff()

        for object_ in [v, b, c]:
            with self.assertRaises(TypeError):
                object_.get_voice()

        for object_ in [b, c]:
            with self.assertRaises(TypeError):
                object_.get_beat()

        for object_ in [c]:
            with self.assertRaises(TypeError):
                object_.get_chord()

    def test_score_get_part(self):
        score = Score()
        assert score.get_part(1) is None
        p1 = score.add_child(Part('p1'))
        assert score.get_part(part_number=1) == p1
        assert score.get_part(part_number=2) is None
        p2 = score.add_child(Part('p2'))
        assert score.get_part(part_number=2) == p2
        assert score.get_part(part_number=3) is None

        with self.assertRaises(ValueError):
            score.get_part(1, 2)
        with self.assertRaises(ValueError):
            score.get_part(staff_number=2)

    def test_part_get_measure(self):
        p = Part('p1')
        assert p.get_measure(1) is None
        m1 = p.add_measure()
        assert p.get_measure(1) == m1
        assert p.get_measure(2) is None
        m2 = p.add_measure()
        assert p.get_measure(1) == m1
        assert p.get_measure(2) == m2
        assert p.get_measure(3) is None

        with self.assertRaises(ValueError):
            p.get_measure(1, 2)

        with self.assertRaises(ValueError):
            p.get_measure(staff_number=2)

    def test_measure_get_staff(self):
        m = Measure(1)
        assert m.get_staff(1) is None
        st1 = m.add_staff()
        assert m.get_staff(1) == st1
        assert m.get_staff(2) is None
        st2 = m.add_staff()
        assert m.get_staff(1) == st1
        assert m.get_staff(2) == st2
        assert m.get_staff(3) is None

        with self.assertRaises(ValueError):
            m.get_staff(1, 2)

        with self.assertRaises(ValueError):
            m.get_staff(voice_number=2)

    @patch('musicscore.measure.Measure')
    def test_staff_get_voice(self, mock_measure):
        st = Staff()
        st._parent = mock_measure
        assert st.get_voice(1) is None
        v1 = st.add_voice()
        assert st.get_voice(1) == v1
        assert st.get_voice(2) is None
        v2 = st.add_voice()
        assert st.get_voice(1) == v1
        assert st.get_voice(2) == v2
        assert st.get_voice(3) is None

        with self.assertRaises(ValueError):
            st.get_voice(1, 2)

        with self.assertRaises(ValueError):
            st.get_voice(staff_number=2)

    def test_voice_get_beat(self):
        v = Voice()
        v._parent = Mock()
        assert v.get_beat(1) is None
        b1 = v.add_beat()
        assert v.get_beat(1) == b1
        assert v.get_beat(2) is None
        b2 = v.add_beat()
        assert v.get_beat(1) == b1
        assert v.get_beat(2) == b2
        assert v.get_beat(3) is None

        with self.assertRaises(ValueError):
            v.get_beat(1, 2)

        with self.assertRaises(ValueError):
            v.get_beat(voice_number=2)

    def test_beat_get_chord(self):
        b = Beat()
        b.get_possible_subdivisions = Mock(return_value=None)
        b._parent = Mock()
        assert b.get_chord(1) is None
        ch1 = b._add_chord(Chord(midis=60, quarter_duration=0.5))[0]
        assert b.get_chord(1) == ch1
        assert b.get_chord(2) is None
        ch2 = b._add_chord(Chord(midis=60, quarter_duration=0.5))[0]
        assert b.get_chord(1) == ch1
        assert b.get_chord(2) == ch2
        assert b.get_chord(3) is None

        with self.assertRaises(ValueError):
            b.get_chord(1, 2)

        with self.assertRaises(ValueError):
            b.get_chord(beat_number=2)
