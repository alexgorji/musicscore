from pathlib import Path

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicscore.musicxml.types.complextypes.defaults import WordFont, LyricFont
from musicxmlunittest import XMLTestCase

path = Path(__file__)


class TestScoreDefaults(XMLTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_word_font(self):
        sf = SimpleFormat(quarter_durations=[1, 1])
        sf.chords[0].add_words('some very nice words')
        sf.to_stream_voice(1).add_to_score(self.score)
        xml_path = path.parent.joinpath(path.stem + '_word_font.xml')
        self.score.defaults.add_child(WordFont(font_family='Open Sans'))

        self.score.add_title('test title')
        self.score.add_subtitle('test subtitle')
        self.score.write(path=xml_path)
        self.assertCompareFiles(xml_path)

    def test_lyric_font(self):
        sf = SimpleFormat(quarter_durations=[1, 1])
        sf.chords[0].add_lyric('some very nice words')
        sf.to_stream_voice(1).add_to_score(self.score)
        xml_path = path.parent.joinpath(path.stem + '_lyric_font.xml')
        self.score.defaults.add_child(LyricFont(font_family='Open Sans'))

        self.score.add_title('test title')
        self.score.add_subtitle('test subtitle')
        self.score.write(path=xml_path)
        self.assertCompareFiles(xml_path)
