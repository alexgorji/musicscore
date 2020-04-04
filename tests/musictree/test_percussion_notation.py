from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treebeat import TreeBeat
from musicscore.musictree.treechordflags1 import PizzFlag1, PercussionFlag1
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treepart import TreePart
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicscore.musicxml.elements.note import Type
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        # sf = SimpleFormat(durations=[4, 4, 2, 1, 1.5, 1.8, 0.2, 0.4, 0.5, 1])
        sf = SimpleFormat(quarter_durations=[4, 4])

        for chord in sf.chords:
            # chord.add_flag(PizzFlag())
            chord.add_flag(PercussionFlag1())
        v = sf.to_stream_voice()
        self.score.set_time_signatures([4, 3, 1])
        v.add_to_score(self.score)
        result_path = path + '_test_1'

        # self.score.fill_with_rest()
        # self.score.add_beats()
        # self.score.quantize()
        # for measure in self.score.get_children_by_type(TreeMeasure):
        #     for part in measure.get_children_by_type(TreePart):
        #         for beat in part.get_beats():
        #             new_chords = []
        #             for chord in beat.chords:
        #                 if chord.is_tied_to_previous:
        #                     chord.to_rest()
        #                     new_chords.append(chord)
        #
        #                 elif chord.position_in_beat == 0:
        #                     split = [chord]
        #                     if chord.quarter_duration == 1:
        #                         split = chord.split(1, 1)
        #                     elif chord.quarter_duration == 2:
        #                         split = chord.split(1, 3)
        #                     elif chord.quarter_duration == 3:
        #                         split = chord.split(1, 5)
        #                     elif chord.quarter_duration == 4:
        #                         split = chord.split(1, 7)
        #                     elif chord.quarter_duration == 6:
        #                         split = chord.split(1, 11)
        #                     else:
        #                         pass
        #                     try:
        #                         split[1].to_rest()
        #                     except IndexError:
        #                         pass
        #                     new_chords.extend(split)
        #                 else:
        #                     new_chords.append(chord)
        #             beat._chords = new_chords

        self.score.write(path=result_path)
        # TestScore().assert_template(result_path=result_path)
