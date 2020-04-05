import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicxmlunittest import XMLTestCase
from tests.score_templates.xml_test_score import TestScore

path = str(os.path.abspath(__file__).split('.')[0])


class Test(XMLTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat()
        sf.add_chord(TreeChord())
        sf.add_chord(TreeChord(quarter_duration=0))
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)
        chord = self.score.get_measure(1).get_part(1).get_staff(1).get_voice(1).chords[1]
        self.score.fill_with_rest()
        self.score.preliminary_adjoin_rests()
        self.score.add_beats()
        chord.remove_from_score()

        xml_path = path + '_test_1.xml'
        self.score.write(path=xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        sf = SimpleFormat()
        chord_1 = sf.add_chord(TreeChord())
        chord_2 = sf.add_chord(TreeChord(quarter_duration=0))
        chord_1.add_tie('start')
        chord_2.add_tie('stop')

        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)
        chord = self.score.get_measure(1).get_part(1).get_staff(1).get_voice(1).chords[1]
        self.score.fill_with_rest()
        self.score.preliminary_adjoin_rests()
        self.score.add_beats()
        chord.remove_from_score()

        xml_path = path + '_test_2.xml'
        self.score.write(path=xml_path)
        self.assertCompareFiles(xml_path)
