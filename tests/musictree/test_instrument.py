from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treeinstruments import TreeInstrument, Violin, ViolaDamore
from musicscore.musictree.treescorepart import TreeScorePart
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

import os

from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__)


class Test(TestCase):
    def test_1(self):
        instrument = TreeInstrument(name='banjo', abbreviation='bjo', number=2)
        # score = TreeScoreTimewise()
        score_part = TreeScorePart(id='p1', instrument=instrument)
        # score.add_score_part()
        # violin = Violin(1)
        # score.add_score_part(TreeScorePart('p2', violin))
        # sf = SimpleFormat(durations=5 * [1, 2, 3, 4])
        # sf.to_stream_voice().add_to_score(score, 1, 1)
        # sf = SimpleFormat(durations=4 * [4, 3, 2])
        # sf.to_stream_voice().add_to_score(score, 1, 2)
        # xml_path = path.split('.')[0] + '.xml'
        # score.write(xml_path)
        # TestScore().assert_template(result_path=xml_path)

    def test_2(self):
        instrument = ViolaDamore()
        string = instrument.strings[3]
        # print(string.tuning)