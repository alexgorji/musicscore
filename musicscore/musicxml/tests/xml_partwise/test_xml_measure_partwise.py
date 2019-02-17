from unittest import TestCase
from musicscore.musicxml.elements.xml_partwise import XMLMeasurePartwise
from musicscore.musicxml.elements.xml_attributes import XMLAttributes, XMLTime, XMLClef, XMLDivisions
from musicscore.musicxml.elements.xml_note import XMLNote, XMLPitch


class TestMeasurePartwise(TestCase):
    def setUp(self):
        self.measure = XMLMeasurePartwise(number=1)

    def test_meaure_partwise(self):
        attributes = self.measure.add_child(XMLAttributes())
        attributes.add_child(XMLTime(3, 4))
        attributes.add_child(XMLClef('G', 2))
        attributes.add_child(XMLDivisions(2))
        result = '''<measure number="1">
  <attributes>
    <divisions>2</divisions>
    <time>
      <beats>3</beats>
      <beat-type>4</beat-type>
    </time>
    <clef>
      <sign>G</sign>
      <line>2</line>
    </clef>
  </attributes>
</measure>
'''
        self.assertEqual(self.measure.to_string(), result)

    def test_measure_music_data(self):
        self.measure.test_mode = True
        note = self.measure.add_music_data(XMLNote(XMLPitch(), 10))
        for child in note.get_children():
            child.include_in_test = False
        # attributes = self.measure.add_child(XMLAttributes())
        self.measure.add_xml_attribute(XMLTime(3, 4))
        self.measure.add_xml_attribute(XMLDivisions(3))
        with self.assertRaises(TypeError):
            self.measure.add_xml_attribute(None)
        note = self.measure.add_music_data(XMLNote(XMLPitch(), 10))
        for child in note.get_children():
            child.include_in_test = False
        result = '''<measure number="1">
  <note/>
  <attributes>
    <divisions/>
    <time>
      <beats/>
      <beat-type/>
    </time>
  </attributes>
  <note/>
</measure>
'''
        self.assertEqual(self.measure.to_string(), result)
