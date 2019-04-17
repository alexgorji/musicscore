from unittest import TestCase
from musicscore.musictree.treescore_timewise import TreeScoreTimewise
import os

path = os.path.abspath(__file__).split('.')[0]


class TestAddMeasure(TestCase):
    def setUp(self):
        self.score = TreeScoreTimewise()
        self.score.add_part('one')

    def test_adding_measure(self):
        self.score.add_measure().time = (3, 4)
        self.score.add_measure().time = (2, 4)
        self.score.add_measure().time = (2, 4)
        self.score.add_measure().time = (2, 4)
        self.score.get_measure(4).time.force_show = True
        self.score.add_measure().time = (3, 8)

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
          <beats>3</beats>
          <beat-type>4</beat-type>
        </time>
      </attributes>
      <note>
        <rest/>
        <duration>3</duration>
        <type>half</type>
        <dot/>
      </note>
    </part>
  </measure>
  <measure number="2">
    <part id="p1">
      <attributes>
        <divisions>1</divisions>
        <time>
          <beats>2</beats>
          <beat-type>4</beat-type>
        </time>
      </attributes>
      <note>
        <rest/>
        <duration>2</duration>
        <type>half</type>
      </note>
    </part>
  </measure>
  <measure number="3">
    <part id="p1">
      <attributes>
        <divisions>1</divisions>
      </attributes>
      <note>
        <rest/>
        <duration>2</duration>
        <type>half</type>
      </note>
    </part>
  </measure>
  <measure number="4">
    <part id="p1">
      <attributes>
        <divisions>1</divisions>
        <time>
          <beats>2</beats>
          <beat-type>4</beat-type>
        </time>
      </attributes>
      <note>
        <rest/>
        <duration>2</duration>
        <type>half</type>
      </note>
    </part>
  </measure>
  <measure number="5">
    <part id="p1">
      <attributes>
        <divisions>2</divisions>
        <time>
          <beats>3</beats>
          <beat-type>8</beat-type>
        </time>
      </attributes>
      <note>
        <rest/>
        <duration>3</duration>
        <type>quarter</type>
        <dot/>
      </note>
    </part>
  </measure>
</score-timewise>
'''
        self.assertEqual(self.score.to_string(), result)
        # self.score.write(path=path)
