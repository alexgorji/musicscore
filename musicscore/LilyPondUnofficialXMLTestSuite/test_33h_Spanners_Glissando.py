"""
All different types of glissando defined in MusicXML
"""
from pathlib import Path

from musicscore import Score, G, Chord, F
from musicscore.tests.util import IdTestCase
from musicxml import XMLGlissando, XMLSlide

types = ['normal glissando', 'solid (+text)', 'dashed', 'dotted', 'wavy', 'normal slide', 'solid (+text)', 'dashed',
         'dotted', 'wavy']


class TestLily33h(IdTestCase):
    def test_lily_33h_Spanners_Glissando(self):
        score = Score()
        part = score.add_part('p1')
        line_types = [None, 'solid', 'dashed', 'dotted', 'wavy']
        for i, t in enumerate(types):
            chords = [Chord(G(4), 1), Chord(F(5), 1)]
            texts = t.split(' ')
            chords[0].add_lyric(texts[0])
            if len(texts) > 1:
                chords[1].add_lyric(texts[1])

            if i < 5:
                chords[0].add_x(XMLGlissando(type='start', line_type=line_types[i]))
                chords[1].add_x(XMLGlissando(type='stop'))
            else:
                chords[0].add_x(XMLSlide(type='start', line_type=line_types[i-5]))
                chords[1].add_x(XMLSlide(type='stop'))
            [part.add_chord(ch) for ch in chords]

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
