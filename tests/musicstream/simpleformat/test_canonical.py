import os

from quicktions import Fraction

from musicscore.basic_functions import dToX
from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.midi import E
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicxmlunittest import XMLTestCase

path = os.path.abspath(__file__).split('.')[0]


def _generate_simple_format():
    unit = Fraction(1, 2)
    quarter_durations = [x * unit for x in range(1, 8)]
    intervals = list(range(1, 7))
    midis = dToX(intervals, first_element=60)
    output = SimpleFormat(quarter_durations=quarter_durations, midis=midis)
    return output


class Test(XMLTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()
        self.sf = _generate_simple_format()

    def test_1(self):
        xml_path = path + '_test_1.xml'
        self.sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        xml_path = path + '_test_2.xml'
        self.sf.to_stream_voice().add_to_score(self.score)
        self.sf.transpose(1)
        self.sf.to_stream_voice().add_to_score(self.score, staff_number=2)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_3(self):
        xml_path = path + '_test_3.xml'
        self.sf.to_stream_voice().add_to_score(self.score)
        self.sf.retrograde()
        self.sf.to_stream_voice().add_to_score(self.score, staff_number=2)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_4(self):
        xml_path = path + '_test_4.xml'
        self.sf.to_stream_voice().add_to_score(self.score)
        self.sf.mirror()
        self.sf.to_stream_voice().add_to_score(self.score, staff_number=2)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_5(self):
        xml_path = path + '_test_5.xml'
        self.sf.to_stream_voice().add_to_score(self.score)
        self.sf.mirror(pivot=58)
        self.sf.auto_clef()
        self.sf.to_stream_voice().add_to_score(self.score, staff_number=2)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_6(self):
        xml_path = path + '_test_6.xml'
        self.sf.to_stream_voice().add_to_score(self.score)
        self.sf.mirror(pivot=E(5))
        self.sf.to_stream_voice().add_to_score(self.score, staff_number=2)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_7(self):
        xml_path = path + '_test_7.xml'
        self.sf.retrograde()
        self.sf.to_stream_voice().add_to_score(self.score)
        self.sf.mirror(pivot=E(5))
        self.sf.to_stream_voice().add_to_score(self.score, staff_number=2)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_8(self):
        xml_path = path + '_test_8.xml'
        self.sf.to_stream_voice().add_to_score(self.score)
        self.sf.multiply_quarter_durations(factor=2)
        self.sf.to_stream_voice().add_to_score(self.score, staff_number=2)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)
