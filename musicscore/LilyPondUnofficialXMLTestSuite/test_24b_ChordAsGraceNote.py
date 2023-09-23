"""
Chords as grace notes.
"""
from pathlib import Path

from musicscore import Score, Chord, C, A, D, F, B
from musicscore.tests.util import IdTestCase
from musicxml.xmlelement.xmlelement import XMLSlur


class TestLily24b(IdTestCase):
    def test_lily_24b_ChordAsGraceNote(self):
        score = Score()
        part = score.add_part('p1')

        chords = [Chord(C(5), 1), Chord(C(5), 1), Chord([C(5), A(4)], 1)]
        gch = chords[1].add_grace_chord([D(5), F(5)])
        gch.add_x(XMLSlur(type='start'))
        chords[1].add_x(XMLSlur(type='stop'))

        gch = chords[2].add_grace_chord([B(4), D(5)])
        gch.add_x(XMLSlur(type='start', orientation='under'))
        chords[2].add_x(XMLSlur(type='stop'))

        for ch in chords:
            part.add_chord(ch)

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
