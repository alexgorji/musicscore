from pathlib import Path

from musicscore.chord import Chord
from musicscore.clef import TrebleClef
from musicscore.part import Part
from musicscore.score import Score
from musicscore.tests.util import IdTestCase


class TestHelloRests(IdTestCase):
    def test_export_hello_world(self):
        """
        Hallo World, Variation III: Pitches and rests: 1, 2, ..., 15 beats (quarters) first in 4/4 measures, than in 5/4 and 6/4 measures.
        Each note / rest shows its duration as lyrics.
        """
        """
        Tester creates a timewise score
        """
        s = Score()
        """
        He adds a part
        """
        p = s.add_child(Part('P1', name='Music'))
        """
        He adds a long list of chords with ascending arithmatic progression a1=1 an=15 d=1:
          measures in 4/4 time
          measures in 5/4 time
          measures in 6/4 time
          as pitches and as rests
        """
        for time in [(4, 4), (5, 4), (6, 4)]:
            m = p.add_measure(time=time)
            if time == (4, 4):
                st = m.add_staff()
                st.clef = TrebleClef()
            for qd in list(range(1, 16)):
                ch = Chord(midis=60, quarter_duration=qd)
                ch.add_lyric(qd)
                p.add_chord(chord=ch, staff_number=1)
                ch = Chord(midis=0, quarter_duration=qd)
                ch.add_lyric(qd)
                p.add_chord(chord=ch, staff_number=2)

        """
        ... and exports the xml
        """
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)
