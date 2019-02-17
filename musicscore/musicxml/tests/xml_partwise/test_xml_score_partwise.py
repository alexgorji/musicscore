from unittest import TestCase
from musicscore.musicxml.elements.xml_partwise import XMLScorePartwise, XMLPartPartwise, XMLMeasurePartwise
from musicscore.musicxml.elements.xml_score_header import XMLScorePart
from musicscore.musicxml.elements.xml_note import XMLNote, XMLPitch
from musicscore.musicxml.elements.xml_attributes import XMLTime, XMLClef, XMLDivisions, XMLAttributes


class TestXMLScorePartwise(TestCase):
    def setUp(self):
        self.score = XMLScorePartwise()
        part_id = 'P1'
        self.score.add_score_part(XMLScorePart(id=part_id))
        part = self.score.add_child(XMLPartPartwise(id=part_id))
        measure = part.add_child(XMLMeasurePartwise(number=1))
        attributes = measure.add_child(XMLAttributes())
        attributes.add_child(XMLTime(4, 4))
        attributes.add_child(XMLClef('G', 2))
        attributes.add_child(XMLDivisions(1))
        measure.add_child(XMLNote(event=XMLPitch(), duration=4))

    def test_xml_score(self):
        self.score.test_mode = True
        result = '''<score-partwise>
  <part-list>
    <score-part>
      <part-name/>
    </score-part>
  </part-list>
  <part>
    <measure>
      <attributes>
        <divisions/>
        <time>
          <beats/>
          <beat-type/>
        </time>
        <clef>
          <sign/>
          <line/>
        </clef>
      </attributes>
      <note>
        <pitch>
          <step/>
          <octave/>
        </pitch>
        <duration/>
      </note>
    </measure>
  </part>
</score-partwise>
'''
        self.assertEqual(self.score.to_string(), result)
        # self.score.test_mode = False
        # print(self.score.to_string())



