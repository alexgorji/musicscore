from unittest import TestCase

from musicscore.musictree.midi import Midi
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treenote import TreeNote
from musicscore.musictree.treepart import TreePart
from musicscore.musictree.treescore_timewise import TreeScoreTimewise
import os

path = os.path.abspath(__file__).split('.')[0]


class TestTreeTimewise(TestCase):
    def setUp(self):
        self.score = TreeScoreTimewise()
        self.score.add_measure()
        self.score.add_part('one')

    def test_score(self):
        result = '''<score-timewise version="3.0">
  <part-list>
    <score-part id="p1">
      <part-name print-object="no">one</part-name>
    </score-part>
  </part-list>
  <measure number="1">
    <part id="p1">
      <attributes>
        <divisions>1</divisions>
      </attributes>
    </part>
  </measure>
</score-timewise>
'''
        self.assertEqual(self.score.to_string(), result)

    def test_add_note(self):
        self.score.add_note(1, 1, TreeNote())
        self.score.add_note(1, 1, TreeNote())
        self.score.add_note(1, 1, TreeNote(event=Midi(61).get_pitch_rest(), quarter_duration=2))
        self.score.finish()
        result = '''<score-timewise version="3.0">
  <part-list>
    <score-part id="p1">
      <part-name print-object="no">one</part-name>
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
        <rest/>
        <duration>1</duration>
        <type>quarter</type>
      </note>
      <note>
        <rest/>
        <duration>1</duration>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>C</step>
          <alter>1</alter>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>half</type>
        <accidental>sharp</accidental>
      </note>
    </part>
  </measure>
</score-timewise>
'''
        self.assertEqual(self.score.to_string(), result)
        self.score.write(path=path)

    def test_quantize_beats(self):
        self.score.add_note(1, 1, TreeNote(quarter_duration=1, event=Midi(60).get_pitch_rest()))
        self.score.add_note(1, 1, TreeNote(quarter_duration=1.2, event=Midi(60).get_pitch_rest()))
        self.score.add_note(1, 1, TreeNote(quarter_duration=0.3, event=Midi(60).get_pitch_rest()))
        self.score.add_note(1, 1, TreeNote(quarter_duration=0.2, event=Midi(60).get_pitch_rest()))
        self.score.add_note(1, 1, TreeNote(quarter_duration=1.3, event=Midi(60).get_pitch_rest()))
        self.score.finish()
        result = '''<score-timewise version="3.0">
  <part-list>
    <score-part id="p1">
      <part-name print-object="no">one</part-name>
    </score-part>
  </part-list>
  <measure number="1">
    <part id="p1">
      <attributes>
        <divisions>6</divisions>
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
        <duration>6</duration>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>C</step>
          <octave>4</octave>
        </pitch>
        <duration>6</duration>
        <tie/>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>C</step>
          <octave>4</octave>
        </pitch>
        <duration>1</duration>
        <type>16th</type>
        <beam number="1">begin</beam>
      </note>
      <note>
        <pitch>
          <step>C</step>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
        <beam number="1">continue</beam>
      </note>
      <note>
        <pitch>
          <step>C</step>
          <octave>4</octave>
        </pitch>
        <duration>1</duration>
        <type>16th</type>
        <beam number="1">continue</beam>
      </note>
      <note>
        <pitch>
          <step>C</step>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <tie/>
        <type>eighth</type>
        <beam number="1">end</beam>
      </note>
      <note>
        <pitch>
          <step>C</step>
          <octave>4</octave>
        </pitch>
        <duration>6</duration>
        <type>quarter</type>
      </note>
    </part>
  </measure>
</score-timewise>
'''
        self.assertEqual(self.score.to_string(), result)
        self.score.write(path=path)
