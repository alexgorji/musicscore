from unittest import TestCase
from musicscore.musicxml.elements.fullnote import DisplayStep, DisplayOctave, Rest


class TestRest(TestCase):
    def setUp(self):
        self.rest = Rest()

    def test_rest(self):
        result = '''<rest/>
'''

        self.assertEqual(self.rest.to_string(), result)

    def test_rest_2(self):
        self.rest.add_child(DisplayStep('C'))
        self.rest.add_child(DisplayOctave(4))
        result = '''<rest>
  <display-step>C</display-step>
  <display-octave>4</display-octave>
</rest>
'''
        self.assertEqual(self.rest.to_string(), result)

    def test_rest_3(self):
        self.rest.add_child(DisplayStep('C'))
        self.rest.display_step.value = 'D'
        self.rest.add_child(DisplayOctave(7))
        result = '''<rest>
  <display-step>D</display-step>
  <display-octave>7</display-octave>
</rest>
'''
        self.assertEqual(self.rest.to_string(), result)

