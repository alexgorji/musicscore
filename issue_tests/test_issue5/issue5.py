import os
from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.simple_format = SimpleFormat(quarter_durations=[4])
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = self.simple_format
        sf.chords[0].add_dynamics('ff')
        sf.chords[0].remove_dynamics()
        self.assertIsNone(sf.chords[0].get_dynamics())

    def test_2(self):
        sf = self.simple_format
        sf.chords[0].add_words('word')
        sf.chords[0].add_dynamics('ff')
        sf.chords[0].remove_dynamics()
        sf.chords[0].add_dynamics('p')
        sf.to_stream_voice().add_to_score(self.score, part_number=1)
        xml_path = path + '_test_2.xml'
        self.score.write(xml_path)
