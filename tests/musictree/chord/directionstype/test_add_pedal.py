from pathlib import Path

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicxmlunittest import XMLTestCase

path = Path(__file__)


class TestAddPedal(XMLTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_imply(self):
        xml_path = path.parent.joinpath(path.stem + '_imply.xml')
        sf = SimpleFormat(quarter_durations=[1, 1, 1, 1])
        sf.chords[0].add_pedal('start')
        sf.chords[2].add_pedal('stop')
        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)
