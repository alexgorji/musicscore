from unittest import TestCase

from musicscore import Part
from musicscore.clef import Clef, TrebleClef, BassClef, TenorClef, AltoClef, PercussionClef
from musicscore.tests.util import IdTestCase


class TestClef(IdTestCase):
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
        c = PercussionClef()
        assert c.sign == 'percussion'
        assert c.line is None

        c = TrebleClef(octave_change=1)
        expected = """<clef>
  <sign>G</sign>
  <line>2</line>
  <clef-octave-change>1</clef-octave-change>
</clef>
"""
        assert c.to_string() == expected

    def test_staff_clef(self):
        clefs = [None, TrebleClef(), AltoClef(), TenorClef(), BassClef(), PercussionClef(),
                 TrebleClef(octave_change=-1),
                 Clef(sign='F', line=3)]

        part = Part('p1')
        for c in clefs:
            m = part.add_measure()
            m.get_staff(1).clef = c
        for m, c in zip(part.get_children(), clefs):
            if c:
                assert m.clefs == [c]
        part.finalize()
