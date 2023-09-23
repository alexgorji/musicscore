from pathlib import Path

from musicscore import Score, C, D, Chord, Time
from musicscore.tests.util import IdTestCase

"""Accidentals can be cautionary or editorial. Each measure has a normal accidental, an editorial, a cautionary and 
an editorial and cautionary accidental."""


class TestLily01e(IdTestCase):
    def test_lily_01e_Pitches_ParenthesizedAccidentals(self):
        score = Score('cautionary accidentals')
        p = score.add_part('cautionary')
        p.add_measure(Time(5, 4))
        midis = [C(4, 'bb') for _ in range(5)] + \
                [C(4, 'three-quarters-flat') for _ in range(5)] + \
                [C(4, 'b') for _ in range(5)] + \
                [C(4, 'quarter-flat') for _ in range(5)] + \
                [C(4, 'natural') for _ in range(5)] + \
                [C(4, 'quarter-sharp') for _ in range(5)] + \
                [C(4, '#') for _ in range(5)] + \
                [C(4, 'three-quarters-sharp') for _ in range(5)] + \
                [C(4, '##') for _ in range(5)]
        for index, midi in enumerate(midis):
            if (index + 1) % 5 == 0:
                midi.accidental.bracket = 'yes'
                ch = Chord(midi, 1)
                ch.add_lyric('bracket')
            elif (index + 1) % 5 == 1:
                ch = Chord(midi, 1)
            elif (index + 1) % 5 == 2:
                midi.accidental.parentheses = 'yes'
                ch = Chord(midi, 1)
                ch.add_lyric('parentheses')
            elif (index + 1) % 5 == 3:
                midi.accidental.cautionary = 'yes'
                ch = Chord(midi, 1)
                ch.add_lyric('cautionary')
            else:
                midi.accidental.editorial = 'yes'
                ch = Chord(midi, 1)
                ch.add_lyric('editorial')
            p.add_chord(ch)

        xml_file = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_file)
