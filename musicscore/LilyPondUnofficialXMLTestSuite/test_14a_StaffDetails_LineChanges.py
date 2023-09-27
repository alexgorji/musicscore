"""The number of staff lines can be modified by using the staff-lines child of the staff-details attribute. This can
happen globally (the first staff has one line globally) or during the part at the beginning of a measure and even
inside a measure (the second part has 5 lines initially, 4 at the beginning of the second measure, and 3 starting in
the middle of the third measure)."""

from pathlib import Path

from musicscore import Score, Chord, G
from musicscore.tests.util import IdTestCase
from musicxml import XMLStaffDetails

"""
finale changes staff number of lines only ones. The next changes have no effect.
"""


class TestLily14a(IdTestCase):
    def test_lily_14a_StaffDetails_LineChanges(self):
        score = Score()
        p1 = score.add_part('p1')
        p2 = score.add_part('p2')
        p1.name = 'Part 1'
        p2.name = 'Part 2'

        [p1.add_chord(Chord(G(4), 4)) for _ in range(4)]
        [p2.add_chord(Chord(G(4), 2)) for _ in range(8)]

        sd = p1.get_measure(1).xml_attributes.xml_staff_details = XMLStaffDetails()
        sd.xml_staff_lines = 1

        sd = p2.get_measure(1).xml_attributes.xml_staff_details = XMLStaffDetails()
        sd.xml_staff_lines = 4

        sd = p2.get_measure(2).xml_attributes.xml_staff_details = XMLStaffDetails()
        sd.xml_staff_lines = 3

        sd = p2.get_measure(3).xml_attributes.xml_staff_details = XMLStaffDetails()
        sd.xml_staff_lines = 2
        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
