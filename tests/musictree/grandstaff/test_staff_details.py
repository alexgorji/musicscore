import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicscore.musicxml.types.complextypes.attributes import StaffDetails
from musicscore.musicxml.types.complextypes.staffdetails import StaffLines, StaffSize
from musicxmlunittest import XMLTestCase

path = str(os.path.abspath(__file__).split('.')[0])


class Test(XMLTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf_1 = SimpleFormat(quarter_durations=[2, 2], midis=[0, 71])
        sf_1.to_stream_voice().add_to_score(self.score, staff_number=1)

        sf_2 = SimpleFormat(quarter_durations=[2, 2], midis=[71, 0])
        sf_2.to_stream_voice().add_to_score(self.score, staff_number=2)

        first_staff = self.score.get_measure(1).get_part(1)
        staff_details = first_staff.attributes.add_child(StaffDetails())
        staff_details.add_child(StaffLines(1))
        xml_path = path + '_test_1.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        sf_1 = SimpleFormat(quarter_durations=[2, 2], midis=[0, 71])
        sf_1.to_stream_voice().add_to_score(self.score, staff_number=1)

        sf_2 = SimpleFormat(quarter_durations=[2, 2], midis=[71, 0])
        sf_2.to_stream_voice().add_to_score(self.score, staff_number=2)

        first_staff = self.score.get_measure(1).get_part(1)
        staff_details = first_staff.attributes.add_child(StaffDetails())
        staff_details.add_child(StaffSize(65))
        xml_path = path + '_test_2.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_3(self):
        sf_1 = SimpleFormat(quarter_durations=[2, 2], midis=[0, 71])
        sf_1.to_stream_voice().add_to_score(self.score, staff_number=1)

        sf_2 = SimpleFormat(quarter_durations=[2, 2], midis=[71, 0])
        sf_2.to_stream_voice().add_to_score(self.score, staff_number=2)

        first_staff = self.score.get_measure(1).get_part(1)
        staff_details = first_staff.attributes.add_child(StaffDetails(number=1))
        staff_details.add_child(StaffLines(1))
        staff_details = first_staff.attributes.add_child(StaffDetails(number=1))
        staff_details.add_child(StaffSize(65))

        xml_path = path + '_test_3.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)
