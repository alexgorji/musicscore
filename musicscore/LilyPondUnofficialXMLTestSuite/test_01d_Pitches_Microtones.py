from pathlib import Path

from musicscore import Score, C, D, E, F, Chord, Midi
from musicscore.tests.util import IdTestCase

"""
Some microtones: c flat-and-a-half, d half-flat, e half-sharp, f sharp-and-a half. Once in the
lower and once in the upper region of the staff.
"""


class TestLily01d(IdTestCase):
    def test_lily_01d_Pitches_Microtones(self):
        score = Score('Microtones')
        p = score.add_part('microtones')
        midis = [Midi(60 - 3 / 2), Midi(60 + 3 / 2), Midi(64 + 1 / 2), Midi(65 + 3 / 2)]
        midis[0].accidental.mode = 'force-flat'
        midis[1].accidental.mode = 'force-flat'
        midis += [C(5, 'three-quarters-flat'), D(5, 'quarter-flat'), E(5, 'quarter-sharp'),
                  F(5, 'three-quarters-sharp')]

        for midi in midis:
            p.add_chord(Chord(midi, 1))

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
