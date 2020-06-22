from pathlib import Path

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicxmlunittest import XMLTestCase

path = Path(__file__)


class Test(XMLTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_single_syllabic(self):
        xml_path = path.parent.joinpath(path.stem + '_single_syllabic.xml')
        sf = SimpleFormat(quarter_durations=4)
        sf.chords[0].add_lyric('one', syllabic='single')
        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_multi_syllabic(self):
        xml_path = path.parent.joinpath(path.stem + '_multi_syllabic.xml')
        sf = SimpleFormat(quarter_durations=[1, 1, 1, 1])
        sf.chords[0].add_lyric('non', syllabic='begin')
        sf.chords[1].add_lyric('syl', syllabic='middle')
        sf.chords[2].add_lyric('la', syllabic='middle')
        sf.chords[3].add_lyric('bic', syllabic='end')
        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_extend(self):
        xml_path = path.parent.joinpath(path.stem + '_extend.xml')
        sf = SimpleFormat(quarter_durations=[1, 1, 1, 1])
        sf.chords[0].add_lyric('one', syllabic='single', extend='start')
        # sf.chords[1].add_lyric(extend='continue')
        sf.chords[3].add_lyric('two', syllabic='single')
        sf.to_stream_voice().add_to_score(self.score)
        self.score.finish()
        partwise = self.score.to_partwise()
        partwise.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_melismatic(self):
        xml_path = path.parent.joinpath(path.stem + '_melismatic.xml')
        sf = SimpleFormat(quarter_durations=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1])
        sf.chords[0].add_lyric('mar', syllabic='begin')
        sf.chords[3].add_lyric('a', syllabic='middle')
        sf.chords[-1].add_lyric('thon', syllabic='end')
        sf.to_stream_voice().add_to_score(self.score)
        self.score.finish()
        partwise = self.score.to_partwise()
        partwise.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_simple(self):
        xml_path = path.parent.joinpath(path.stem + '_simple.xml')
        sf = SimpleFormat(quarter_durations=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1])
        sf.chords[0].add_lyric(1)
        sf.chords[3].add_lyric(2)
        sf.chords[-1].add_lyric(3)
        sf.to_stream_voice().add_to_score(self.score)
        self.score.finish()
        partwise = self.score.to_partwise()
        partwise.write(xml_path)
        self.assertCompareFiles(xml_path)

