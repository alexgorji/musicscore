import os
from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treeclef import ALTO_CLEF
from musicscore.musictree.treeinstruments import TreeInstrument, Violin, Cello, Viola
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def test_1(self):
        instrument = TreeInstrument(name='banjo', abbreviation='bjo', number=2)
        instrument.standard_clef = ALTO_CLEF
        sf = SimpleFormat(quarter_durations=[1, 2, 3, 1, 2, 3, 1, 2, 3])
        score = TreeScoreTimewise()
        sf.to_stream_voice(2).add_to_score(score)
        sf.transpose(5)
        sf.to_stream_voice(1).add_to_score(score)
        score.get_score_parts()[0].instrument = instrument

        xml_path = path + '_test_1.xml'
        score.write(xml_path)
        TestScore().assert_template(result_path=xml_path)

    def test_2(self):
        sf = SimpleFormat(quarter_durations=[1, 2, 3, 1, 2, 3, 1, 2, 3], midis=9 * [60 - 5])
        score = TreeScoreTimewise()
        for part_number in range(1, 5):
            sf.to_stream_voice().add_to_score(score, part_number=part_number)

        score_parts = score.get_score_parts()
        score_parts[0].instrument = Violin(1)
        score_parts[1].instrument = Violin(1)
        score_parts[2].instrument = Viola()
        score_parts[3].instrument = Cello()
        xml_path = path + '_test_2.xml'
        score.write(xml_path)
        TestScore().assert_template(result_path=xml_path)
