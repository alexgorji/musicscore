import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicxmlunittest import XMLTestCase

path = str(os.path.abspath(__file__).split('.')[0])


class TestGetBeats(XMLTestCase):
    def setUp(self):
        self.score = TreeScoreTimewise()

    def test_1(self):
        score = self.score
        result_path = path + '_test_1'
        sf = SimpleFormat(quarter_durations=[1.5, 2, 3.5])
        sf.to_stream_voice().add_to_score(score)

        score.finish_til_flag_1()
        score.finish_from_flag_1_to_2()
        score.finish_from_flag_2_to_3()

        beat_number = 1
        for measure in score.get_children_by_type(TreeMeasure):
            for beat in measure.get_beats():
                for chord in beat.chords:
                    chord.add_words(beat_number)
                    beat_number += 1
                print(beat.chords)
        self.score.write(path=result_path)
