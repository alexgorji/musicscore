"""
Two voices share one staff. Each voice is assigned some lyrics.
"""

from pathlib import Path

from musicscore import Score, A, Chord, Lyrics, C, E, D, B, G
from musicscore.chord import Rest
from musicscore.tests.util import IdTestCase
from musicscore.util import slur_chords
from musicxml import XMLFermata, XMLAccent


class TestLily42a(IdTestCase):
    def test_lily_42a_MultiVoice_TwoVoicesOnStaff_Lyrics(self):
        score = Score()
        part = score.add_part('p1')
        v1 = [Chord(E(5), 2), Chord(D(5), 1), Chord(B(4), 1), Rest(1), Chord(D(5), 1), Chord(B(3), 1.5),
              Chord(C(5), 0.5), Rest(4)]
        v2 = [Chord(C(5), 2), Chord(B(4), 1), Chord(G(4), 1), Rest(1), Chord(B(4), 1), Chord(G(3), 1.5),
              Chord(A(4), 0.5), Rest(4)]
        for ch in [v1[0], v2[0]]:
            ch.add_x(XMLFermata())
            ch.add_x(XMLAccent())
        v1[1].add_dynamics('mf')
        slur_chords(v1[-3:-1])
        slur_chords(v2[-3:-1])
        [part.add_chord(ch, voice_number=1) for ch in v1]
        [part.add_chord(ch, voice_number=2) for ch in v2]
        Lyrics(['This', 'is', 'the', None, 'lyrics', 'of', 'Voice1', None], show_number=True,
               default_y=-110).add_to_chords(v1)
        Lyrics(['This', 'is', 'the', None, 'lyrics', 'of', 'Voice2', None], show_number=True,
               default_y=-130).add_to_chords(v2)
        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
