from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicxmlunittest import XMLTestCase


class Test(XMLTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf_1 = SimpleFormat(quarter_durations=[1, 0.25, 2.25])
        # sf_2 = SimpleFormat(quarter_durations=[0.25, 2.25, 1])
        sf_1.to_stream_voice().add_to_score(self.score, part_number=1, staff_number=1)
        # sf_2.to_stream_voice().add_to_score(self.score, part_number=1, staff_number=2)
        self.score.finish()
        xml_notes = self.score.get_measure(1).get_part(1).get_staff(1).xml_notes
        print([xml_note.notes[0].quarter_duration for xml_note in xml_notes])