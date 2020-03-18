from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechordflags1 import PercussionFlag1, XFlag1
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        xml_path = path + '_test_1.xml'
        durations = [2, 2]
        sf = SimpleFormat(quarter_durations=durations)
        chords = sf.chords
        chords[0].add_tie('start')
        chords[1].add_tie('stop')
        chords[1].is_adjoinable = False
        # sf.to_stream_voice().add_to_score(self.score, part_number=1)
        sf._chords = []
        new_chords = chords[0].split(1, 1)

        new_chords.append(chords[1])
        for ch in new_chords:
            # ch.is_adjoinable = False
            sf.add_chord(ch)
        v = sf.to_stream_voice()
        # print([ch.quarter_duration for ch in v.chords])
        # print([ch.is_tied_to_next for ch in v.chords])
        # print([ch.is_adjoinable for ch in v.chords])

        sf.to_stream_voice().add_to_score(self.score, part_number=1)

        self.score.write(xml_path)
        # TestScore().assert_template(xml_path)

    def test_2(self):
        xml_path = path + '_test_2.xml'
        durations = [5]
        sf = SimpleFormat(quarter_durations=durations)

        chords = sf.chords
        sf._chords = []
        new_chords = chords[0].split(4, 1)
        new_chords[0].is_adjoinable = False
        for ch in new_chords:
            sf.add_chord(ch)

        chords = sf.chords
        sf._chords = []
        new_chords = chords[0].split(1, 3)
        new_chords[0].is_adjoinable = False
        new_chords.append(chords[-1])
        for ch in new_chords:
            sf.add_chord(ch)

        chords = sf.chords
        sf._chords = []
        sf.add_chord(chords[0])
        new_chords = chords[1].split(1, 2)
        new_chords[0].is_adjoinable = False
        new_chords.append(chords[-1])
        for ch in new_chords:
            sf.add_chord(ch)

        chords = sf.chords
        sf._chords = []
        sf.add_chord(chords[0])
        sf.add_chord(chords[1])
        new_chords = chords[2].split(1, 1)
        new_chords[0].is_adjoinable = False
        new_chords.append(chords[-1])
        for ch in new_chords:
            sf.add_chord(ch)

        sf.to_stream_voice().add_to_score(self.score, part_number=1)

        self.score.write(xml_path)
        # TestScore().assert_template(xml_path)
