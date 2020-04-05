import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicxmlunittest import XMLTestCase

path = str(os.path.abspath(__file__).split('.')[0])


class Test(XMLTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        simple_format = SimpleFormat(quarter_durations=[1, 2, 3])
        simple_format.to_stream_voice().add_to_score(self.score)
        measure_1_chords = self.score.get_measure(1).get_part(1).get_staff(1).get_voice(1).chords
        measure_2_chords = self.score.get_measure(2).get_part(1).get_staff(1).get_voice(1).chords
        for chord in measure_1_chords + measure_2_chords:
            if chord.next_in_score:
                chord.add_words(chord.next_in_score.quarter_duration)
        xml_path = path + '_test_1.xml'
        self.score.write(xml_path)
