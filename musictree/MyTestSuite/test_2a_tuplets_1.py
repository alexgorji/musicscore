from pathlib import Path

from musictree.chord import Chord
from musictree.part import Part
from musictree.score import Score
from musictree.tests.util import IdTestCase, generate_all_quintuplets, generate_all_sextuplets, generate_all_triplets, \
    generate_all_septuplets


class TestHelloTuplets1(IdTestCase):
    def test_generate_all_quintuplets(self):
        assert len(generate_all_quintuplets()) == 15
        for x in generate_all_quintuplets():
            assert sum(x) == 1

    def test_generate_all_sextuplets(self):
        # print([[f.as_integer_ratio() for f in x] for x in generate_all_sextuplets()])
        assert len(generate_all_sextuplets()) == 27
        for x in generate_all_sextuplets():
            assert sum(x) == 1

    def test_export_hello_world_tuplets_1(self):
        """
        Write all possible tuplet combinations up until SEXTUPLETS
        """
        """
        Tester creates a timewise score
        """
        s = Score()
        """
        He adds a measure with one part to it
        """
        p = s.add_child(Part('P1', name='Music'))
        """
        He adds a 1/4 measure
        """
        p.add_measure(time=(1, 4))
        """
        All possible combinations are:
        """
        triplets = generate_all_triplets()
        tuplets = triplets + generate_all_quintuplets() + generate_all_sextuplets() + generate_all_septuplets()
        for tuplet_list in tuplets:
            for tuplet in tuplet_list:
                p.add_chord(Chord(60, tuplet))
        # for tuplet in tuplets[6]:
        #     p.add_chord(Chord(60, tuplet))
        """
        ... and exports the xml
        """
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)
