import difflib
from pathlib import Path
from unittest import TestCase

import xmldiff
from xmldiff.main import diff_trees

from musictree.chord import Chord
from musictree.measure import Measure
from musictree.part import Part
from musictree.score import Score
from musictree.tests.util import diff_xml

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
        <voice>1</voice>
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
        s = Score()
        """
        He adds a measure with one part to it (default Measure has a 4/4 time signature)
        """
        p = s.add_child(Part('P1', name='Music'))
        m = p.add_child(Measure(number=1))
        """
        He adds a Chord with midi 60 to the measure
        """
        m.add_chord(Chord(60, 4))
        s.update_xml_notes()
        assert s.to_string() == expected
        """
        ... and exports the xml (3.1 is default)
        """
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)
        assert diff_xml(xml_path) == []
