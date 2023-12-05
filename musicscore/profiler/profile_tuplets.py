import cProfile
from contextlib import redirect_stdout
from pathlib import Path

from musicscore.chord import Chord
from musicscore.part import Part
from musicscore.score import Score
from musicscore.tests.util_subdivisions import generate_all_quintuplets_manually, generate_all_sextuplets_manually, \
    generate_all_septuplets_manually, generate_all_triplets_manually


def p():
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

    """
    ... and exports the xml
    """
    xml_path = Path(__file__).with_suffix('.xml')
    s.export_xml(xml_path)


# with open(str(Path(__file__))+'xsd_tree_only_once.txt', '+w') as f:
with open(Path(__file__).with_suffix('.txt'), '+w') as f:
    with redirect_stdout(f):
        cProfile.run('p()', sort="tottime")
