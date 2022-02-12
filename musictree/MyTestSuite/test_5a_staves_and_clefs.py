from pathlib import Path

from musictree.chord import Chord
from musictree.measure import Measure
from musictree.part import Part
from musictree.score import Score
from musictree.staff import Staff
from musictree.tests.util import IdTestCase


class TestHelloPianoStaves(IdTestCase):
    def test_export_hello_world_piano_staves(self):
        """
        Tester creates a timewise score
        """
        s = Score()
        """
        He adds a part
        """
        p = s.add_child(Part('P1', name='Music'))
        """
        He adds some chords for two staves with each two voices
        """
        p.add_chord(Chord(60, 4), staff=1, voice=1)
        p.add_chord(Chord(61, 4), staff=1, voice=2)
        p.add_chord(Chord(48, 4), staff=2, voice=1)
        p.add_chord(Chord(49, 4), staff=2, voice=2)

        s.update_xml_notes()
        """
        ... and exports the xml
        """
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)
