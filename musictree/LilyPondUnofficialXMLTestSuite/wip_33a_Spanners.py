"""Several spanners defined in MusicXML: tuplet, slur (solid, dashed), tie, wedge (cresc, dim), tr + wavy-line,
single-note trill spanner, octave-shift (8va,15mb), bracket (solid down/down, dashed down/down, solid none/down,
dashed none/up, solid none/none), dashes, glissando (wavy), bend-alter, slide (solid), grouping, two-note tremolo,
hammer-on, pull-off, pedal (down, change, up)."""
from pathlib import Path

from musictree import Score, Time, Chord
from musictree.tests.util import IdTestCase


class TestLily33a(IdTestCase):
    def test_lily_33a_Spanners(self):
        score = Score()
        part = score.add_part('p1')

        t = Time(3, 4)
        t.actual_signatures = [1, 2, 1, 4]
        part.add_measure(t)
        part.add_measure(Time(3, 4))

        [part.add_chord(Chord(72, 2/3)) for _ in range(3)]
        part.add_chord(Chord(0, 1))

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
