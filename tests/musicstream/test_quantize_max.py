import itertools
import os
import random
from unittest import TestCase

from quicktions import Fraction

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(quarter_durations=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
        for index, chord in enumerate(sf.chords):
            chord.add_lyric(index + 1)
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score, part_number=2)

        sf = SimpleFormat(quarter_durations=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)

        self.score.fill_with_rest()
        self.score.preliminary_adjoin_rests()
        self.score.add_beats()

        for measure in self.score.get_children_by_type(TreeMeasure):
            part = measure.get_part(2)
            for beat in part.get_beats():
                beat.max_division = 7

        result_path = path + '_test_1'
        # with self.assertWarns(UserWarning):
        #     self.score.write(path=result_path)
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_2(self):
        self.score.add_measure(TreeMeasure(time=(3, 4)))
        sf = SimpleFormat(quarter_durations=[0.5, 0.6, 0.7, 0.8])
        for index, chord in enumerate(sf.chords):
            chord.add_lyric(index + 1)
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)

        sf = SimpleFormat(quarter_durations=[0.5, 0.6, 0.7, 0.8])
        for index, chord in enumerate(sf.chords):
            chord.add_lyric(index + 1)
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score, part_number=2)

        self.score.fill_with_rest()
        self.score.preliminary_adjoin_rests()
        self.score.add_beats()

        for measure in self.score.get_children_by_type(TreeMeasure):
            part = measure.get_part(2)
            for beat in part.get_beats():
                beat.max_division = 7

        self.score.quantize()

        result_path = path + '_test_2'
        # with self.assertWarns(UserWarning):
        #     self.score.write(path=result_path)
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_3(self):

        random.seed(3)
        durations = []
        while sum(durations) <= 16:
            duration = random.randrange(0, 2) + (random.random() / 2.)
            durations.append(Fraction(duration).limit_denominator(100))

        def add_to_score(part=1):
            sf = SimpleFormat(quarter_durations=durations)
            dynamics = itertools.cycle(['pppp', 'ppp', 'pp', 'p', 'mp', 'mf', 'f', 'ff', 'fff'])

            for index, chord in enumerate(sf.chords):
                chord.add_lyric(index + 1)
                d = chord.add_dynamics(dynamics.__next__())
                d.relative_y = -20
                d.halign = 'center'
            v = sf.to_stream_voice(1)
            v.add_to_score(self.score, part)

        add_to_score(1)
        add_to_score(2)
        add_to_score(3)
        add_to_score(4)
        add_to_score(5)
        add_to_score(6)
        add_to_score(7)
        add_to_score(8)

        self.score.get_score_parts()[0].max_division = 8
        self.score.get_score_parts()[1].max_division = 7
        self.score.get_score_parts()[2].max_division = 6
        self.score.get_score_parts()[3].max_division = 5
        self.score.get_score_parts()[4].max_division = 4
        self.score.get_score_parts()[5].max_division = 3
        self.score.get_score_parts()[6].max_division = 2
        self.score.get_score_parts()[7].max_division = 1
        result_path = path + '_test_3'

        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_4(self):
        sf = SimpleFormat(
            quarter_durations=[Fraction(3, 10), Fraction(3, 10), Fraction(3, 10), Fraction(3, 10), Fraction(3, 10),
                               Fraction(3, 2), Fraction(1, 2), Fraction(1, 3)])
        xml_path = path + '_test_4.xml'
        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        TestScore().assert_template(result_path=xml_path)

    def test_5(self):
        self.score.set_time_signatures(
            [Fraction(3, 2)])
        sf = SimpleFormat(quarter_durations=[0.666, 0.333, 0.5])
        xml_path = path + '_test_5.xml'
        sf.to_stream_voice().add_to_score(self.score)
        self.score.get_score_parts()[0].max_division = 1
        self.score.write(xml_path)
        # TestScore().assert_template(result_path=xml_path)

    # def test_4(self):
    #
    #     random.seed(1)
    #     durations = []
    #     while sum(durations) <= 16:
    #         duration = random.randrange(0, 2) + (random.random() / 2.)
    #         durations.append(Fraction(duration).limit_denominator(100))
    #
    #     def add_to_score(part=1):
    #         sf = SimpleFormat(durations=durations)
    #         for index, chord in enumerate(sf.chords):
    #             chord.add_lyric(index + 1)
    #         v = sf.to_voice(1)
    #         v.add_to_score(self.score, 1, part)
    #
    #     add_to_score(1)
    #
    #     def print_last_chord_ties():
    #         chord = self.score.get_measure(3).get_part(1).get_voice(1).get_beats()[-1].chords[-1]
    #         try:
    #             print(chord.get_children_by_type(Lyric)[0].get_children_by_type(Text)[0].value)
    #         except:
    #             pass
    #         print(chord.tie_types)
    #
    #     self.score.get_score_parts()[0].max_division = 2
    #     # self.score.fill_with_rest()
    #     # self.score.add_beats()
    #     # print_last_chord_ties()
    #     # self.score.quantize()
    #     # print_last_chord_ties()
    #     # self.score.split_not_notatable()
    #     # print_last_chord_ties()
    #     # self.score.update_tuplets()
    #     # self.score.substitute_sextoles()
    #     # self.score.update_types()
    #     # self.score.update_dots()
    #     # self.score.group_beams()
    #     # print_last_chord_ties()
    #     # self.score.chord_to_notes()
    #     # print(self.score.get_measure(3).get_part(1).notes[-1].get_children())
    #     # self.score.update_divisions()
    #     #
    #     # self.score.update_accidentals(mode='normal')
    #     #
    #     # self.score.update_durations()
    #     # print(self.score.get_measure(3).get_part(1).notes[-1].get_children())
    #     # self.score.close_dtd()
    #     # print(self.score.get_measure(3).get_part(1).notes[-1].get_children())
    #
    #     result_path = path + '_test_4'
    #     self.score.write(path=result_path)
