from pathlib import Path

from musictree.chord import Chord
from musictree.part import Part
from musictree.score import Score
from musictree.tests.util import IdTestCase, generate_all_quintuplets, generate_all_sextuplets, generate_all_triplets, \
    generate_all_septuplets


class TestTuplets1(IdTestCase):
    def test_generate_all_quintuplets(self):
        assert len(generate_all_quintuplets()) == 15
        for x in generate_all_quintuplets():
            assert sum(x) == 1

    def test_generate_all_sextuplets(self):
        assert len(generate_all_sextuplets()) == 27
        for x in generate_all_sextuplets():
            assert sum(x) == 1

    def test_tuplets_1(self):
        """
        Write all possible tuplet combinations up until SEXTUPLETS
        """

        s = Score()

        p = s.add_child(Part('P1', name='Music'))

        p.add_measure(time=(1, 4))

        tuplets = generate_all_triplets() + generate_all_quintuplets() + generate_all_sextuplets() + generate_all_septuplets()

        for tuplet_list in tuplets:
            for tuplet in tuplet_list:
                p.add_chord(Chord(60, tuplet))

        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)
