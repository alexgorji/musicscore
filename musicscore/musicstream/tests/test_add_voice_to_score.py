from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescore_timewise import TreeScoreTimewise
from musicscore.musicxml.elements.note import Lyric
from musicscore.musicxml.score_templates.xml_test_score import TestScore
from musicscore.musicxml.types.complextypes.lyric import Text

path = os.path.abspath(__file__).split('.')[0]

class Test(TestCase):

    def setUp(self) -> None:
        self.score = TreeScoreTimewise()


    def test_1(self):
        simpleformat = SimpleFormat(midis=list(range(60, 68)))
        voice = simpleformat.to_voice(2)
        self.score.add_part()
        self.score.add_measure()
        voice.add_to_score(self.score, 1)
        result = '''<score-timewise version="3.0">
  <part-list>
    <score-part id="p1">
      <part-name print-object="no">none</part-name>
    </score-part>
  </part-list>
  <measure number="1">
    <part id="p1">
      <attributes>
        <divisions>1</divisions>
        <time>
          <beats>4</beats>
          <beat-type>4</beat-type>
        </time>
      </attributes>
      <note>
        <pitch>
          <step>C</step>
          <octave>4</octave>
        </pitch>
        <duration>1</duration>
        <voice>2</voice>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>C</step>
          <alter>1</alter>
          <octave>4</octave>
        </pitch>
        <duration>1</duration>
        <voice>2</voice>
        <type>quarter</type>
        <accidental>sharp</accidental>
      </note>
      <note>
        <pitch>
          <step>D</step>
          <octave>4</octave>
        </pitch>
        <duration>1</duration>
        <voice>2</voice>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>E</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>1</duration>
        <voice>2</voice>
        <type>quarter</type>
        <accidental>flat</accidental>
      </note>
    </part>
  </measure>
  <measure number="2">
    <part id="p1">
      <attributes>
        <divisions>1</divisions>
      </attributes>
      <note>
        <pitch>
          <step>E</step>
          <alter>0</alter>
          <octave>4</octave>
        </pitch>
        <duration>1</duration>
        <voice>2</voice>
        <type>quarter</type>
        <accidental>natural</accidental>
      </note>
      <note>
        <pitch>
          <step>F</step>
          <octave>4</octave>
        </pitch>
        <duration>1</duration>
        <voice>2</voice>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>F</step>
          <alter>1</alter>
          <octave>4</octave>
        </pitch>
        <duration>1</duration>
        <voice>2</voice>
        <type>quarter</type>
        <accidental>sharp</accidental>
      </note>
      <note>
        <pitch>
          <step>G</step>
          <octave>4</octave>
        </pitch>
        <duration>1</duration>
        <voice>2</voice>
        <type>quarter</type>
      </note>
    </part>
  </measure>
</score-timewise>
'''
        self.assertEqual(self.score.to_string(), result)

    def test_2(self):
        simpleformat = SimpleFormat(midis=list(range(60, 68)), durations=[1.2]*8)
        voice = simpleformat.to_voice(2)
        self.score.add_part()
        self.score.add_measure()
        voice.add_to_score(self.score, 1)
        result_path = path + '_test_2'
        self.score.write(result_path)
        TestScore().assert_template(result_path=result_path)


    def test_3(self):
        sf = SimpleFormat(midis=[(60, 61, 67)], durations=7)
        voice = sf.to_voice(1)
        voice.add_to_score(self.score, 1)
        result_path = path + '_test_3'
        self.score.write(result_path)
        TestScore().assert_template(result_path=result_path)

    def test_4(self):
        midis = list(range(60, 80))
        sf = SimpleFormat(midis=midis)
        for chord in sf.chords:
            l = chord.add_child(Lyric())
            l.add_child(Text(str([m.value for m in chord.midis])))
        voice = sf.to_voice(1)
        voice.add_to_score(self.score, 1)
        p = path + '_test_4'
        self.score.write(p)
