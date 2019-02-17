from unittest import TestCase
from musicscore.musicxml.elements.xml_note import XMLDisplayStep

class TestDisplayStep(TestCase):
    def setUp(self):
        self.display_step = XMLDisplayStep(value='C')

    def test_display_step(self):
        result = '''<display-step>C</display-step>
'''
        self.assertEqual(self.display_step.to_string(), result)