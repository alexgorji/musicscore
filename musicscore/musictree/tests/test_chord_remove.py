import warnings
from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treescore_timewise import TreeScoreTimewise


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat()
        sf.add_chord(TreeChord())
        sf.add_chord(TreeChord(quarter_duration=0))
        v = sf.to_voice(1)
        v.add_to_score(self.score, 1, 1)
        chord = self.score.get_measure(1).get_part(1).get_voice(1).chords[1]
        self.score.fill_with_rest()
        self.score.add_beats()
        chord.remove_from_score()

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
          <step>B</step>
          <octave>4</octave>
        </pitch>
        <duration>1</duration>
        <voice>1</voice>
        <type>quarter</type>
      </note>
      <note>
        <rest/>
        <duration>3</duration>
        <voice>1</voice>
        <type>half</type>
        <dot/>
      </note>
    </part>
  </measure>
</score-timewise>
'''

        with self.assertWarns(UserWarning):
            self.assertEqual(self.score.to_string(), result)

    def test_2(self):
        sf = SimpleFormat()
        chord_1 = sf.add_chord(TreeChord())
        chord_2 = sf.add_chord(TreeChord(quarter_duration=0))
        chord_1.add_tie('start')
        chord_2.add_tie('stop')

        v = sf.to_voice(1)
        v.add_to_score(self.score, 1, 1)
        chord = self.score.get_measure(1).get_part(1).get_voice(1).chords[1]
        self.score.fill_with_rest()
        self.score.add_beats()
        chord.remove_from_score()

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
          <step>B</step>
          <octave>4</octave>
        </pitch>
        <duration>1</duration>
        <voice>1</voice>
        <type>quarter</type>
      </note>
      <note>
        <rest/>
        <duration>3</duration>
        <voice>1</voice>
        <type>half</type>
        <dot/>
      </note>
    </part>
  </measure>
</score-timewise>
'''
        with self.assertWarns(UserWarning):
            self.assertEqual(self.score.to_string(), result)

