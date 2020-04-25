import os

from quicktions import Fraction

from musicscore.basic_functions import dToX
from musicscore.musicstream.streamvoice import SimpleFormat
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

        def _change_quarter_duration(chord, factor):
            chord.quarter_duration *= factor

        self.sf.change_chords(lambda chord: _change_quarter_duration(chord, 2))
        self.sf.to_stream_voice().add_to_score(self.score, staff_number=2)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        xml_path = path + '_test_2.xml'
        self.sf.to_stream_voice().add_to_score(self.score)

        def _change_quarter_duration(chord, factor):
            chord.quarter_duration *= factor

        self.sf.change_chords(lambda chord: _change_quarter_duration(chord, 2) if int(
            chord.quarter_duration) != chord.quarter_duration else None)
        self.sf.to_stream_voice().add_to_score(self.score, staff_number=2)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)
