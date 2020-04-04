from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicscore.musicxml.elements.note import Tie


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        simpleformat = SimpleFormat(quarter_durations=4)
        voice = simpleformat.to_stream_voice(2)
        self.score.add_part()
        self.score.add_measure()
        p = self.score.get_measure(1).get_part(1)
        remaining_chords = voice.add_to_part(p)
        result = '''<part id="p1">
  <attributes>
    <divisions>1</divisions>
  </attributes>
  <note>
    <pitch>
      <step>B</step>
      <octave>4</octave>
    </pitch>
    <duration>4</duration>
    <voice>2</voice>
    <type>whole</type>
  </note>
  <backup>
    <duration>4</duration>
  </backup>
  <note>
    <rest/>
    <duration>4</duration>
    <voice>1</voice>
    <type>whole</type>
  </note>
</part>
'''
        self.assertEqual(p.to_string(), result)
        self.assertEqual(remaining_chords, None)

    def test_2(self):
        simpleformat = SimpleFormat(quarter_durations=7)
        voice = simpleformat.to_stream_voice(2)
        self.score.add_part()
        self.score.add_measure()
        p = self.score.get_measure(1).get_part(1)
        remaining_chords = voice.add_to_part(p)
        result = '''<part id="p1">
  <attributes>
    <divisions>1</divisions>
  </attributes>
  <note>
    <pitch>
      <step>B</step>
      <octave>4</octave>
    </pitch>
    <duration>4</duration>
    <tie type="start"/>
    <voice>2</voice>
    <type>whole</type>
    <notations>
      <tied number="1" type="start"/>
    </notations>
  </note>
  <backup>
    <duration>4</duration>
  </backup>
  <note>
    <rest/>
    <duration>4</duration>
    <voice>1</voice>
    <type>whole</type>
  </note>
</part>
'''
        self.assertEqual(p.to_string(), result)
        chord = remaining_chords[0]
        self.assertEqual(chord.quarter_duration, 3)
        self.assertEqual(chord.get_children_by_type(Tie)[0].type, 'stop')

    def test_3(self):
        simpleformat = SimpleFormat(quarter_durations=3)
        voice = simpleformat.to_stream_voice(2)
        self.score.add_part()
        self.score.add_measure()
        p = self.score.get_measure(1).get_part(1)
        remaining_chords = voice.add_to_part(p)
        result = '''<part id="p1">
  <attributes>
    <divisions>1</divisions>
  </attributes>
  <note>
    <pitch>
      <step>B</step>
      <octave>4</octave>
    </pitch>
    <duration>3</duration>
    <voice>2</voice>
    <type>half</type>
    <dot/>
  </note>
  <note>
    <rest/>
    <duration>1</duration>
    <voice>2</voice>
    <type>quarter</type>
  </note>
  <backup>
    <duration>4</duration>
  </backup>
  <note>
    <rest/>
    <duration>4</duration>
    <voice>1</voice>
    <type>whole</type>
  </note>
</part>
'''
        self.assertEqual(p.to_string(), result)

    def test_4(self):
        simpleformat = SimpleFormat(quarter_durations=7, midis=0)
        voice = simpleformat.to_stream_voice(2)
        self.score.add_part()
        self.score.add_measure()
        p = self.score.get_measure(1).get_part(1)
        remaining_chords = voice.add_to_part(p)
        result = '''<part id="p1">
  <attributes>
    <divisions>1</divisions>
  </attributes>
  <note>
    <rest/>
    <duration>4</duration>
    <voice>2</voice>
    <type>whole</type>
  </note>
  <backup>
    <duration>4</duration>
  </backup>
  <note>
    <rest/>
    <duration>4</duration>
    <voice>1</voice>
    <type>whole</type>
  </note>
</part>
'''
        self.assertEqual(p.to_string(), result)
        self.assertEqual(remaining_chords[0].midis[0].value, 0)
        self.assertEqual(remaining_chords[0].get_children_by_type(Tie), [])

    def test_5(self):
        simpleformat = SimpleFormat(quarter_durations=3, midis=0)
        voice = simpleformat.to_stream_voice(2)
        self.score.add_part()
        self.score.add_measure()
        p = self.score.get_measure(1).get_part(1)
        voice.add_to_part(p)
        result = '''<part id="p1">
  <attributes>
    <divisions>1</divisions>
  </attributes>
  <note>
    <rest/>
    <duration>4</duration>
    <voice>2</voice>
    <type>whole</type>
  </note>
  <backup>
    <duration>4</duration>
  </backup>
  <note>
    <rest/>
    <duration>4</duration>
    <voice>1</voice>
    <type>whole</type>
  </note>
</part>
'''
        self.assertEqual(p.to_string(), result)
