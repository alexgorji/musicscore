from pathlib import Path

from musicscore import Score, G, A, B, C, D, E, F, Chord, Midi
from musicscore.tests.util import IdTestCase

"""
All pitches from G to c”” in ascending steps; First without accidentals, then with a sharp and then with a flat 
accidental. Double alterations and cautionary accidentals are tested at the end.
"""


class TestLily01a(IdTestCase):
    def test_lily_01a_Pitches_Pitches(self):

        score = Score('Pitches and accidentals')
        p = score.add_part('pitches')
        scale_1 = [G(2), A(2), B(2), C(3), D(3), E(3), F(3), G(3), A(3), B(3), C(4), D(4), E(4), F(4), G(4), A(4), B(4),
                   C(5),
                   D(5), E(5), F(5), G(5), A(5), B(5), C(6), D(6), E(6), F(6), G(6), A(6), B(6), C(7)]
        # with sharps
        scale_2 = [midi.__deepcopy__() for midi in scale_1]
        for midi in scale_2:
            midi.transpose(1)
            if midi.value % 12 in [0, 5]:
                # B# and E#
                midi.accidental.mode = 'force-sharp'
            else:
                midi.accidental.mode = 'sharp'
        # with flats
        scale_3 = [midi.__deepcopy__() for midi in scale_1]
        for midi in scale_3:
            midi.transpose(-1)
            if midi.value % 12 in [11, 4]:
                # C-flat and F-flat
                midi.accidental.mode = 'force-flat'
            else:
                midi.accidental.mode = 'flat'
        # Double alterations and cautionary accidentals.
        cs = [Midi(74), Midi(70), Midi(73), Midi(73), Midi(73), Midi(73)]
        cs[0].accidental.mode = 'force-sharp'
        cs[1].accidental.mode = 'force-flat'
        for midi in scale_1 + scale_2 + scale_3 + cs:
            p.add_chord(Chord(midis=midi, quarter_duration=1))
        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
