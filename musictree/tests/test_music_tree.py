from unittest.mock import patch

from musictree.accidental import Accidental
from musictree.beat import Beat
from musictree.chord import Chord
from musictree.measure import Measure
from musictree.midi import Midi
from musictree.note import Note
from musictree.part import Part
from musictree.score import Score
from musictree.staff import Staff
from musictree.tests.util import IdTestCase
from musictree.voice import Voice


class TestMusicTree(IdTestCase):
    @patch.object(Chord, 'get_voice_number')
    def test_add_child_type(self, mock_chord_method):
        mock_chord_method.return_value = 1
        s = Score()
        p = Part('P1')
        m = Measure(1)
        st = Staff()
        v = Voice()
        b = Beat()
        c = Chord(60, 1)
        n = Note(parent_chord=c)
        mi = Midi(60)
        acc = Accidental()
        assert p == s.add_child(p)
        assert m == p.add_child(m)
        assert st == m.add_child(st)
        assert v == st.add_child(v)
        assert b == v.add_child(b)
        assert c == b.add_child(c)
        assert n == c.add_child(n)
        assert mi == n.add_child(mi)
        assert acc == mi.add_child(acc)

        objects = [s, m, st, v, b, c, n, mi]
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
