from unittest import TestCase

from musictree.treechord import TreeChord


class TestTreeChord(TestCase):
    def test_default_midis(self):
        chord = TreeChord()
        assert chord.midis == [71]

    def test_midis_setter(self):
        chord = TreeChord()
        with self.assertRaises(TypeError):
            chord.midis = [60, 'bla']

    def test_add_midi(self):
        chord = TreeChord(midis=[80, 81])
        assert chord.midis == [80, 81]
        chord.add_midi(82)
        assert chord.midis == [80, 81, 82]
