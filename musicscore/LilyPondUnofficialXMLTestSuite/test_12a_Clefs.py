"""
Various clefs: G, C, F, percussion, TAB and none; some are also possible with transposition and on other staff lines than their default (e.g. soprano/alto/tenor/baritone C clefs); Each measure shows a different clef (measure 17 has the " none" clef), only measure 18 has the same treble clef as measure 1.
"""
from pathlib import Path

from musicscore import AltoClef, TenorClef, BassClef, TrebleClef, Score, Chord
from musicscore.clef import PercussionClef, Clef
from musicscore.tests.util import IdTestCase

clefs = [TrebleClef(), AltoClef(), TenorClef(), BassClef(), PercussionClef(), TrebleClef(octave_change=-1),
         BassClef(octave_change=-1), Clef(sign='G', line=1), Clef(sign='F', line=3), Clef(sign='C', line=5),
         Clef(sign='C', line=2), Clef(sign='C', line=1), PercussionClef(), TrebleClef(octave_change=1),
         BassClef(octave_change=1), Clef(sign='TAB'), Clef('none'), TrebleClef()]


class TestLily12a(IdTestCase):
    def test_lily_12a_Clefs(self):
        score = Score()
        part = score.add_part('p1')
        for c in clefs:
            ch = Chord(60, 4)
            part.add_chord(ch)
            part.get_current_measure().get_staff(1).clef = c

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
