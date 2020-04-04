from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(quarter_durations=[0.5, 1.5, 0.3, 1.7])
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)

        result_path = path + '_test_1'
        self.score.fill_with_rest()
        self.score.preliminary_adjoin_rests()
        self.score.add_beats()
        self.score.quantize()
        self.score.split_not_notatable()
        for chord in self.score.get_measure(1).get_part(1).get_staff(1).get_voice(1).chords:
            chord.add_lyric(round(float(chord.offset), 2))
        # with self.assertWarns(UserWarning):
        #     self.score.write(path=result_path)
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)
