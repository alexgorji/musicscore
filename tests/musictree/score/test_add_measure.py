import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicxmlunittest import XMLTestCase

path = str(os.path.abspath(__file__).split('.')[0])


class Test(XMLTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        simple_format = SimpleFormat(quarter_durations=4)
        simple_format.to_stream_voice().add_to_score(self.score)
        self.score.add_measure()
        m2 = self.score.get_measure(2)
        self.score.finish()
        actual = m2.to_string()
        expected = """<measure number="2">
  <part id="p1">
    <attributes>
      <divisions>1</divisions>
    </attributes>
    <note>
      <rest/>
      <duration>4</duration>
      <voice>1</voice>
      <type>whole</type>
    </note>
  </part>
</measure>
"""
        self.assertEqual(expected, actual)
