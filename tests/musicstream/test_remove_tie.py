import os
from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()
        self.score.add_measure(TreeMeasure(time=(1, 4)))

    def test_1(self):
        sf = SimpleFormat(quarter_durations=[1, 0, 1])
        sf.chords[0].add_tie('start')
        sf.chords[1].add_tie('stop')
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)
        self.score.fill_with_rest()
        self.score.preliminary_adjoin_rests()
        self.score.add_beats()
        self.score.quantize()

        chord = self.score.get_measure(2).get_part(1).get_staff(1).get_voice(1).chords[0]
        chord.remove_from_score()

        result_path = path + '_test_1'
        # with self.assertWarns(UserWarning):
        #     self.score.write(path=result_path)
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)