from pathlib import Path

from musicscore.chord import Chord
from musicscore.part import Part
from musicscore.score import Score
from musicscore.tests.util import IdTestCase
from musicscore.tests.util_subdivisions import generate_all_quintuplets_manually, generate_all_sextuplets_manually, \
    generate_all_septuplets_manually, generate_all_triplets_manually


class TestHelloTuplets1(IdTestCase):
    def test_generate_all_quintuplets(self):
        assert len(generate_all_quintuplets_manually()) == 15
        for x in generate_all_quintuplets_manually():
            assert sum(x) == 1

    def test_generate_all_sextuplets(self):
        # print([[f.as_integer_ratio() for f in x] for x in generate_all_sextuplets_manually()])
        assert len(generate_all_sextuplets_manually()) == 27
        for x in generate_all_sextuplets_manually():
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
        triplets = generate_all_triplets_manually()
        tuplets = triplets + generate_all_quintuplets_manually() + generate_all_sextuplets_manually() + generate_all_septuplets_manually()
        for tuplet_list in tuplets:
            for tuplet in tuplet_list:
                p.add_chord(Chord(60, tuplet))
        # for tuplet in tuplets[6]:
        #     p._add_chord(Chord(60, tuplet))
        """
        ... and exports the xml
        """
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)
