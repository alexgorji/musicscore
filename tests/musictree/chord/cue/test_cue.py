from pathlib import Path

from quicktions import Fraction

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechordflags3 import TreeChordFlag3
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicscore.musicxml.elements.note import Cue, Type
from musicxmlunittest import XMLTestCase

path = Path(__file__)


class CueTypeFlag(TreeChordFlag3):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def implement(self, chord):
        t = chord.get_children_by_type(Type)[0]
        t.size = 'cue'
        return [chord]


class TestCue(XMLTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_add_child(self):
        xml_path = path.parent.joinpath(path.stem + '_add_child.xml')
        sf = SimpleFormat(quarter_durations=16 * [Fraction(1, 8)])
        for chord in sf.chords[1:-1]:
            chord.add_child(Cue())
        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_add_flag(self):
        xml_path = path.parent.joinpath(path.stem + '_add_flag.xml')
        sf = SimpleFormat(quarter_durations=16 * [Fraction(1, 8)])
        for chord in sf.chords[1:-1]:
            chord.add_flag(CueTypeFlag())
        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)
