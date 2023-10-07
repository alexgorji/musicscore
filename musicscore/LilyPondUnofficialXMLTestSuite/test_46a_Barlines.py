"""
Different types of (non-repeat) barlines: default (no setting), regular, dotted, dashed, heavy, light-light, light-heavy,
heavy-light, heavy-heavy, tick, short, none.
"""
from pathlib import Path

from musicscore import Score, Chord
from musicscore.tests.util import IdTestCase
from musicxml.xmlelement.xmlelement import XMLWords


class TestLily46a(IdTestCase):
    def test_lily_46a_Barlines(self):
        score = Score()
        p = score.add_part('p1')
        p.add_chord(Chord(0, 4))

        barline_styles = ['regular', 'dotted', 'dashed', 'heavy', 'light-light', 'light-heavy',
                          'heavy-light', 'heavy-heavy', 'tick', 'short', 'none']

        for bs in barline_styles:
            ch = Chord(0, 4)
            ch.add_x(XMLWords(bs), placement='below')
            p.add_chord(ch)
            p.get_current_measure().set_barline(style=bs)

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
