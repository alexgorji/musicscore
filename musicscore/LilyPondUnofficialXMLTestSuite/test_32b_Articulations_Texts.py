"""
Text markup: different font sizes, weights and colors.
Bold, Medium
Bold, Large
Bold, Small
Normal, Medium
Normal, Large
Normal, Small
Normal, Small, Colored, Below
"""
from pathlib import Path

from musicscore import Score, Time, Chord, G, F
from musicscore.tests.util import IdTestCase


class TestLily32b(IdTestCase):
    def test_lily_32b_Articulations_Texts(self):
        score = Score()
        part = score.add_part('p1')
        t = Time(4, 4)
        t.actual_signatures = [1, 8]
        m = part.add_measure(t)
        m.implicit = 'yes'
        m.number = 0
        part.add_measure(Time(4, 4))
        part.add_chord(Chord(F(4), 0.5))
        part.add_chord(Chord(G(4), 4))
        part.add_chord(Chord(F(4), 4))

        chords = part.get_chords()
        chords[0].add_words('Bold, Medium', placement='below', font_weight='bold', font_size=14)
        chords[1].add_words('Bold, Large', placement='below', font_weight='bold', font_size=18, relative_y=-30)
        chords[2].add_words('Bold, Small', placement='below', font_weight='bold', font_size=10)
        chords[0].add_words('Normal, Medium', font_size=18)
        chords[1].add_words('Normal, Large', font_size=14, relative_y=30)
        chords[2].add_words('Normal, Small', font_size=10)
        chords[2].add_words('Normal, Small, Colored, Below', placement='below', font_size=10, color='#FF0000',
                            relative_y=-30)

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
