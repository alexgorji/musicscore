"""
A clef change in the middle of a measure, using either an implicit measure or simply placing
the attributes in the middle of the measure.
"""
from pathlib import Path

from musicscore import Score, Chord, Clef, TrebleClef
from musicscore.tests.util import IdTestCase


class TestLily46c(IdTestCase):
    def test_lily_46c_Midmeasure_Clef(self):
        score = Score()
        part = score.add_part('p1')
        part.add_chord(Chord(0, 4))
        [part.add_chord(Chord(72, 1)) for _ in range(8)]
        ch = part.get_measure(2).get_chords()[2]
        ch.clef = Clef(sign='C', line=2)
        ch = part.get_measure(3).get_chords()[2]
        ch.clef = TrebleClef()

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
