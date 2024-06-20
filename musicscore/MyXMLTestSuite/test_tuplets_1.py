from pathlib import Path

from quicktions import Fraction

from musicscore.chord import Chord
from musicscore.part import Part
from musicscore.score import Score
from musicscore.tests.util import IdTestCase, create_test_xml_paths
from musicscore.tests.util_subdivisions import generate_all_subdivision_patterns

path = Path(__file__)


class TestTuplets1(IdTestCase):
    def test_tuplets_1(self):
        """
        Write all possible tuplet combinations up until septuplets
        """

        s = Score()

        p = s.add_child(Part('P1', name='Music'))

        p.add_measure(time=(1, 4))

        rhythmic_patterns = []
        for subdivision in range(1, 8):
            rhythmic_patterns.extend(generate_all_subdivision_patterns(subdivision, True))

        for rhythmic_pattern in rhythmic_patterns:
            subdivision = sum(rhythmic_pattern)
            for x in rhythmic_pattern:
                ch = Chord(60, Fraction(x, subdivision))
                ch.add_lyric(x)
                p.add_chord(ch)
        xml_path = create_test_xml_paths(path, 'upto_7')[0]
        s.export_xml(xml_path)

    def test_tuplets_8(self):
        """
        Write all possible tuplet combinations of 32nd
        """

        s = Score()

        p = s.add_child(Part('P1', name='Music'))

        p.add_measure(time=(1, 4))

        subdivision = 8
        rhythmic_patterns = generate_all_subdivision_patterns(subdivision, True)
        for x in [d for rp in rhythmic_patterns for d in rp]:
            ch = Chord(60, Fraction(x, subdivision))
            ch.add_lyric(x)
            p.add_chord(ch)
        xml_path = create_test_xml_paths(path, '8')[0]
        s.export_xml(xml_path)

    def test_tuplets_9(self):
        """
        Write all possible tuplet combinations of nonuplets
        """

        s = Score()

        p = s.add_child(Part('P1', name='Music'))

        p.add_measure(time=(1, 4))

        subdivision = 9
        rhythmic_patterns = generate_all_subdivision_patterns(subdivision, True)
        for x in [d for rp in rhythmic_patterns for d in rp]:
            ch = Chord(60, Fraction(x, subdivision))
            ch.add_lyric(x)
            p.add_chord(ch)
        xml_path = create_test_xml_paths(path, '9')[0]
        s.export_xml(xml_path)
