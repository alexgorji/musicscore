from unittest import TestCase
import os, random

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(quarter_durations=[4, 4, 3, 2, 3, 4, 5, 6, 1, 2])
        self.score.set_time_signatures(quarter_durations=sf.quarter_duration)

        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)

        result_path = path + '_test_1'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_2(self):
        sf = SimpleFormat(quarter_durations=[4, 4, 3, 2, 3, 4, 5, 6, 1, 2])
        self.score.set_time_signatures(times={1: (3, 4), 5: (2, 4)})

        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)

        result_path = path + '_test_2'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_3(self):
        sf = SimpleFormat(quarter_durations=[4, 4, 3, 2, 3, 4, 5, 6, 1, 2])
        self.score.set_time_signatures(quarter_durations=[8, 3, 5, 4, 11, 3])

        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)

        result_path = path + '_test_3'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_4(self):
        sf = SimpleFormat(quarter_durations=[4, 4, 3, 2, 3, 4, 5, 6, 1, 2])
        self.score.set_time_signatures(quarter_durations=[8, 3, 5, 4, 11, 3], times={1: (3, 4)})

        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)

        result_path = path + '_test_4'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_sixteenth_time_signatures(self):
        quarter_durations = [3 * 0.5, 4, 3 * 0.25]
        sf = SimpleFormat(quarter_durations=[3 * 0.5, 4, 3 * 0.25])
        self.score.set_time_signatures(quarter_durations=quarter_durations)

        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)

        result_path = path + '_sixteenth'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_sixteenth_time_signatures_maxdivision_five(self):
        quarter_durations = random_value_generator(value_sum=10, value_min=0.1, value_max=2.5, grid=0.1, seed=10)
        # time_signature_durations = random_value_generator(value_sum=10, value_min=0.25, value_max=2.5, grid=0.25, seed=20)
        # print(time_signature_durations)
        sf = SimpleFormat(quarter_durations=quarter_durations)
        # self.score.set_time_signatures(quarter_durations=time_signature_durations)
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)

        result_path = path + '_sixteenth_max_division'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)


def random_value_generator(value_sum, value_min, value_max, grid, seed=None):
    if seed:
        random.seed(seed)

    min_grid = round(value_min / grid)
    max_grid = round(value_max / grid)

    output = []
    while sum(output) < value_sum:
        new_value = round(random.randrange(min_grid, max_grid) * grid, 5)
        output.append(new_value)

    while sum(output) > value_sum:
        max_value = max(output)
        replacement_value = round(max_value - (sum(output) - value_sum), 5)
        if replacement_value < value_min:
            replacement_value = value_min
        output[output.index(max_value)] = replacement_value

    return output
