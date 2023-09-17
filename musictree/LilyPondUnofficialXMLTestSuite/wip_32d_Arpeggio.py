"""
Different Arpeggio directions (normal, up, down, non-arpeggiate)
"""
from pathlib import Path

from musictree import Score, Chord, C, E, G
from musictree.tests.util import IdTestCase
from musicxml import XMLArpeggiate


class TestLily32d(IdTestCase):
    def test_lily_32d_Arpeggio(self):
        score = Score()
        part = score.add_part('p1')

        chords = [Chord([C(4), E(5), G(5)], 1) for _ in range(8)]

        for i, ch in enumerate(chords):
            if i == 0:
                ch.add_arpeggio()

        [part.add_chord(ch) for ch in chords]

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
