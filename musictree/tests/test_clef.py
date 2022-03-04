from unittest import TestCase

from musictree.clef import Clef, TrebleClef, BassClef, TenorClef, AltoClef


class TestClef(TestCase):
    def test_default_clef(self):
        c = Clef()
        expected = """<clef>
  <sign>G</sign>
  <line>2</line>
</clef>
"""
        assert c.to_string() == expected

    def test_clef_copy(self):
        c = Clef('F', 2, show=False, octave_change=-1)
        copied = c.__copy__()
        assert copied != c
        assert copied.xml_object != c.xml_object
        assert copied.sign == c.sign
        assert copied.line == c.line
        assert copied.show == c.show
        assert copied.octave_change == c.octave_change

    def test_global_clefs(self):
        c = TrebleClef()
        assert c.sign == 'G'
        assert c.line == 2
        c = BassClef()
        assert c.sign == 'F'
        assert c.line == 4
        c = TenorClef()
        assert c.sign == 'C'
        assert c.line == 4
        c = AltoClef()
        assert c.sign == 'C'
        assert c.line == 3
        c = TrebleClef(octave_change=1)
        expected = """<clef>
  <sign>G</sign>
  <line>2</line>
  <clef-octave-change>1</clef-octave-change>
</clef>
"""
        assert c.to_string() == expected
