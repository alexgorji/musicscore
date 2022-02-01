from pathlib import Path
from unittest import TestCase

from musictree.chord import Chord
from musictree.measure import Measure
from musictree.part import Part
from musictree.score import Score

expected = """<score-partwise version="4.0">
  <part-list>
    <score-part id="P1">
      <part-name>Music</part-name>
    </score-part>
  </part-list>
  <part id="P1">
    <measure number="1">
      <attributes>
        <divisions>1</divisions>
        <key>
          <fifths>0</fifths>
        </key>
        <time>
          <beats>4</beats>
          <beat-type>4</beat-type>
        </time>
        <clef>
          <sign>G</sign>
          <line>2</line>
        </clef>
      </attributes>
      <note>
        <pitch>
          <step>C</step>
          <octave>4</octave>
        </pitch>
        <duration>4</duration>
        <type>whole</type>
      </note>
    </measure>
  </part>
</score-partwise>
"""


class TestAcceptance(TestCase):
    def test_export_hello_world(self):
        """
        Hello World as musicxml means having a C4 pitch as a whole in a 4/4 measure with treble clef.
        """
        """
        Tester creates a timewise score
        """
        score = Score()
        """
        He adds a measure with one part to it (default Measure has a 4/4 time signature)
        """
        p = score.add_child(Part('p1'))
        m = p.add_child(Measure(number=1))
        """
        He adds a Chord with midi 60 to the measure
        """
        m.add_chord(Chord(60, 4))
        print(score.to_string())
        assert score.to_string() == expected
        # """
        # ... and exports the xml (3.1 is default)
        # """
        # xml_path = Path(__file__).with_suffix('.muscixml')
        # score.export_xml(xml_path)
