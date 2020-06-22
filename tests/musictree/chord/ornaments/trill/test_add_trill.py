from pathlib import Path

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicxmlunittest import XMLTestCase

path = Path(__file__)


class TestAddTrill(XMLTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_add_trill(self):
        xml_path = path.parent.joinpath(path.stem + '_add_trill.xml')
        sf = SimpleFormat(quarter_durations=4)
        sf.chords[0].add_trill_mark()
        sf.chords[0].add_wavy_line(type='start')
        sf.chords[0].add_wavy_line(type='stop', relative_x=20)
        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)
