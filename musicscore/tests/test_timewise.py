from musicscore.musicxml.tests.xml_test import XMLTest
from musicscore.timewise import Timwise, Note, Measure, Part
from musicscore.musicxml.elements.xml_note import XMLPitch
from musicscore.midi import Midi
import os
path = os.path.abspath(__file__).split('.')[0]


class TestTimewise(XMLTest):

    def setUp(self):
        self.timewise = Timwise()

    def test_add_part(self):
        self.timewise.add_part()
        self.timewise.add_part(print_object='yes', name='oboe')
        result = '''<score-timewise>
  <part-list>
    <score-part id="p1">
      <part-name print-object="no">none</part-name>
    </score-part>
    <score-part id="p2">
      <part-name print-object="yes">oboe</part-name>
    </score-part>
  </part-list>
</score-timewise>
'''
        self.assertEqual(self.timewise.to_string(), result)

    def test_add_measure_part(self):
        self.timewise.add_measure()
        self.timewise.add_part()
        self.timewise.add_part()
        self.timewise.add_measure()
        note = Note(XMLPitch('D'), quarter_duration=1.5)
        self.timewise.add_note(measure_number=1, part_number=2, note=note)
        note = Note(XMLPitch('E', alter=-1, octave=5), quarter_duration=2)
        self.timewise.add_note(measure_number=1, part_number=2, note=note)

        self.timewise.finish()
        self.timewise.write(path)
        self.assert_template(path)

    def test_add_note(self):
        self.timewise.add_measure()
        self.timewise.add_part()
        self.timewise.add_measure()
        note = Note(XMLPitch(), quarter_duration=2)
        with self.assertRaises(IndexError):
            self.timewise.add_note(3, 1, note)
        with self.assertRaises(IndexError):
            self.timewise.add_note(1, 3, note)

    def test_add_midi(self):
        self.timewise.add_part()
        self.timewise.add_measure()
        self.timewise.add_midi(1, 1, Midi(70))
        result = '''<score-timewise>
  <part-list>
    <score-part id="p1">
      <part-name print-object="no">none</part-name>
    </score-part>
  </part-list>
  <measure number="1">
    <part id="p1">
      <attributes>
        <divisions>1</divisions>
      </attributes>
      <note>
        <pitch>
          <step>B</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
      </note>
    </part>
  </measure>
</score-timewise>
'''
        self.assertEqual(self.timewise.to_string(), result)





