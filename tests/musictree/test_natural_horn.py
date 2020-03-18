import os
from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat, TreeChord, Midi
from musicscore.musictree.treeinstruments import NaturalHorn
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.horn = NaturalHorn()
        self.score = TreeScoreTimewise()

    def test_1(self):
        xml_path = path + '_test_1.xml'
        harmonics = SimpleFormat()
        for i in range(1, 17):
            partial_midi = Midi(round(self.horn.get_partial_midi_value(i) * 2) / 2)
            if i % 7 == 0:
                partial_midi.accidental.mode = 'flat'
            if i % 11 == 0:
                partial_midi.accidental.mode = 'sharp'
            if i % 13 == 0:
                partial_midi.accidental.mode = 'flat'
            chord = TreeChord(midis=partial_midi)

            chord.add_words(i)
            harmonics.add_chord(chord)

        harmonics.to_stream_voice().add_to_score(self.score, part_number=2)

        harmonics.transpose(self.horn.transposition)
        harmonics.to_stream_voice().add_to_score(self.score, part_number=1)

        self.score.accidental_mode = 'modern'
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)
