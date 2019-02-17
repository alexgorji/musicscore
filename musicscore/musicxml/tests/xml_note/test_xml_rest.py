from unittest import TestCase
from musicscore.musicxml.elements.xml_note import XMLRest, XMLNote


class TestRest(TestCase):
    def setUp(self):
        self.rest = XMLRest()

    def test_test(self):
        result = '''<rest/>
'''
        self.assertEqual(self.rest.to_string(), result)

        self.rest.display_step = 'C'
        result = '''<rest>
  <display-step>C</display-step>
</rest>
'''
        self.assertEqual(self.rest.to_string(), result)

        self.rest.display_step = None
        result = '''<rest/>
'''
        self.assertEqual(self.rest.to_string(), result)

        self.rest.display_step = 'D'
        self.rest.display_octave = 7
        result = '''<rest>
  <display-step>D</display-step>
  <display-octave>7</display-octave>
</rest>
'''
        self.assertEqual(self.rest.to_string(), result)

    def test_rest_note(self):
        note = XMLNote(event=self.rest, duration=2)
        result = '''<note>
  <rest/>
  <duration>2</duration>
</note>
'''
        self.assertEqual(note.to_string(), result)
