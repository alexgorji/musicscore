"""
Barlines can appear at mid-measure positions, without using an implicit measure!
"""
from musicxml import XMLBarline

"""
MuseScore supports mid-measure barlines
"""

from pathlib import Path

from musicscore import Score, Chord
from musicscore.tests.util import IdTestCase


class TestLily46b(IdTestCase):
    def test_lily_46b_MidmeasureBarlines(self):
        score = Score()
        p = score.add_part('p1')
        midis = [72, 69, 65, 72]
        chords = [Chord(m, 1) for m in midis]
        [p.add_chord(ch) for ch in chords]
        b = XMLBarline(location='middle')
        b.xml_bar_style = 'dashed'
        chords[1].add_xml_element_after_notes(b)
        score.finalize()

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
