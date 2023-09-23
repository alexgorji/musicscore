"""
Two properly nested part groups: One group (with a square bracket) goes from staff 2 to 4)
and another group (with a curly bracket) goes from staff 3 to 4.
"""
from pathlib import Path

from musicscore import Score, Chord
from musicscore.tests.util import IdTestCase
from musicxml.xmlelement.xmlelement import XMLPartList, XMLPartGroup, XMLGroupSymbol, XMLGroupBarline, XMLScorePart


class TestLily41d(IdTestCase):
    def test_lily_41d_StaffGroups(self):
        score = Score()
        parts = [score.add_part(f'p-{i}') for i in range(1, 6)]
        for p in parts:
            p.add_chord(Chord(0, 4))

        score.group_parts(1, 2, 4, symbol='square')
        score.group_parts(2, 3, 4, symbol='bracket')

        # new_xml_part_list = XMLPartList(xsd_check=False)
        #
        # for index, xml_score_part in enumerate(score.xml_part_list.get_children()):
        #     if index == 1:
        #         pg = new_xml_part_list.add_child(XMLPartGroup(number='1', type='start'))
        #         pg.add_child(XMLGroupSymbol('square'))
        #         pg.add_child(XMLGroupBarline('yes'))
        #     elif index == 2:
        #         pg = new_xml_part_list.add_child(XMLPartGroup(number='2', type='start'))
        #         pg.add_child(XMLGroupSymbol('bracket'))
        #         pg.add_child(XMLGroupBarline('yes'))
        #
        #     new_xml_part_list.add_child(xml_score_part)
        #
        #     if index == 3:
        #         new_xml_part_list.add_child(XMLPartGroup(number='1', type='stop'))
        #         new_xml_part_list.add_child(XMLPartGroup(number='2', type='stop'))
        # score.xml_part_list = new_xml_part_list
        path = Path(__file__).with_suffix('.xml')
        score.export_xml(path)
