from unittest import TestCase
from musicscore.musicxml.elements.fullnote import DisplayStep, DisplayOctave, Rest


class TestRest(TestCase):
    def setUp(self):
        self.rest = Rest()

    def test_test(self):
        result = '''<rest/>
'''

        self.assertEqual(self.rest.to_string(), result)

        self.rest.add_child(DisplayStep('C'))
        result = '''<rest>
  <display-step>C</display-step>
</rest>
'''
        self.assertEqual(self.rest.to_string(), result)

        self.rest.display_step.value = 'D'
        self.rest.add_child(DisplayOctave(7))
        result = '''<rest>
  <display-step>D</display-step>
  <display-octave>7</display-octave>
</rest>
'''
        self.assertEqual(self.rest.to_string(), result)

