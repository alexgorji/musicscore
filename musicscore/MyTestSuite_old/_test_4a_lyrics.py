from pathlib import Path

from musicxml.xmlelement.xmlelement import XMLLyric

from musicscore.chord import Chord
from musicscore.part import Part
from musicscore.score import Score
from musicscore.tests.util import IdTestCase


class TestHelloLyrics(IdTestCase):
    def test_export_hello_world_lyrics(self):
        """
        Tester creates a timewise score
        """
        s = Score()
        """
        He adds a part
        """
        p = s.add_child(Part('P1', name='Music'))
        """
        He adds some chords with lyrics
        """
        for i in range(6):
            ch = Chord(60 + i, 3)
            ch.add_lyric(ch.midis[0].accidental.sign)
            p.add_chord(ch)
        """
        ... and exports the xml
        """
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)
