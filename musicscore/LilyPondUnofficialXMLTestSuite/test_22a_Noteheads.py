"""Different note styles, using the <notehead> element. First, each note head style is printed with four quarter
notes, two with filled heads, two with unfilled heads, where first the stem is up and then the stem is down. After
that, each note head style is printed with a half note (should have an unfilled head by default). Finally,
the Aiken note head styles are tested, once with stem up and once with stem down.
"""

from pathlib import Path

from musicscore import Score, Chord, Time, A, B, C, D, E, F, G
from musicscore.tests.util import notehead_values, notehead_aikin_values, IdTestCase


class TestLily22a(IdTestCase):
    def test_lily_22a_Noteheads(self):
        score = Score('Time signatures')
        p = score.add_part('p1')

        def generate_chords(qd):
            for head in notehead_values:
                if qd == 1:
                    chords = [Chord(A(4), qd), Chord(C(5), qd), Chord(A(4), qd), Chord(C(5), qd)]
                elif qd == 2:
                    chords = [Chord(A(4), qd), Chord(A(4), qd)]
                else:
                    chords = [Chord(A(4), qd)]
                chords[0].add_lyric(head)
                for ch in chords:
                    for m in ch.midis:
                        m.notehead = head
                    p.add_chord(ch)

        def generate_chords_aikin():
            qd = 1
            for head in notehead_aikin_values:
                chords = [Chord(A(4), qd), Chord(C(5), qd), Chord(A(4), qd), Chord(C(5), qd)]
                chords[0].add_lyric(head)
                for ch in chords:
                    for m in ch.midis:
                        m.notehead = head
                    p.add_chord(ch)
            scale = [A(3), B(3), C(4), D(4), E(4), F(4), G(4), A(4)]
            heads = ['do', 're', 'mi', 'fa', 'so', 'la', 'ti', 'do']
            for i, head in enumerate(heads):
                ch = Chord(scale[i], 1)
                ch.add_lyric(head)
                ch.midis[0].notehead = head
                p.add_chord(ch)
            scale = [C(5), D(5), E(5), F(5), G(5), A(5), B(5), C(6)]
            for i, head in enumerate(heads):
                ch = Chord(scale[i], 1)
                ch.add_lyric(head)
                ch.midis[0].notehead = head
                p.add_chord(ch)

        generate_chords(1)
        generate_chords(2)
        p.add_measure(Time(2, 4))
        generate_chords(3)
        p.add_chord(Chord(0, 1))

        p.add_measure(Time(4, 4))
        generate_chords_aikin()

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
