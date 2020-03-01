from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

import os
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(quarter_durations=[1, 1, 1, 1])
        for index, ch in enumerate(sf.chords):
            ch.add_words(str(index + 1))

        sf.chords[0].add_tie('start')
        sf.chords[1].add_tie('stop')
        sf.chords[0].is_adjoinable = False

        sf.chords[1].add_tie('start')
        sf.chords[2].add_tie('stop')
        sf.chords[1].is_adjoinable = False

        sf.chords[2].add_tie('start')
        sf.chords[3].add_tie('stop')
        sf.chords[2].is_adjoinable = False

        sf.chords[1].remove_tie('start')
        sf.chords[2].remove_tie('stop')

        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_1.xml'
        self.score.write(xml_path)

        TestScore().assert_template(xml_path)

    def test_2(self):
        sf = SimpleFormat(quarter_durations=[5], midis=[(60, 65, 69)])
        chords = sf.chords[0].split(1, 1, 1, 1, 1)
        for ch in chords:
            ch.is_adjoinable = False
        sf._chords = []
        for ch in chords:
            sf.add_chord(ch)
        sf.chords[2].remove_tie('start')
        sf.chords[3].remove_tie('stop')
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_2.xml'
        self.score.write(xml_path)

        TestScore().assert_template(xml_path)

    def test_3(self):
        sf = SimpleFormat(quarter_durations=[5], midis=[(60, 65, 69)])
        chords = sf.chords[0].split(1, 1, 1, 1, 1)
        for ch in chords:
            ch.is_adjoinable = False
        sf._chords = []
        for ch in chords:
            sf.add_chord(ch)
        sf.chords[2].remove_tie('start')
        sf.chords[2].add_slur(type='start', line_type='dashed')
        sf.chords[3].remove_tie('stop')
        sf.chords[3].add_slur(type='stop')
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_3.xml'
        self.score.write(xml_path)

        TestScore().assert_template(xml_path)

    def test_4(self):
        sf = SimpleFormat(quarter_durations=[5], midis=[(60, 65, 69)])
        chords = sf.chords[0].split(1, 1, 1, 1, 1)
        sf._chords = []

        for ch in chords:
            sf.add_chord(ch)
        sf.chords[2].remove_tie('start')
        sf.chords[2].add_slur(type='start', line_type='dashed')
        sf.chords[3].remove_tie('stop')
        sf.chords[3].add_slur(type='stop')
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_4.xml'
        self.score.write(xml_path)

        TestScore().assert_template(xml_path)

    def test_5(self):
        sf = SimpleFormat(quarter_durations=[2])
        chords = sf.chords[0].split(1, 1)
        sf._chords = []
        for ch in chords:
            sf.add_chord(ch)
        sf.chords[0].remove_tie('start')
        sf.chords[0].add_slur(type='start', line_type='dashed')
        sf.chords[1].remove_tie('stop')
        sf.chords[1].add_slur(type='stop')
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_5.xml'
        self.score.write(xml_path)

        # TestScore().assert_template(xml_path)
