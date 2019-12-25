from unittest import TestCase

from musicscore.musicxml.elements.note import Notations
from musicscore.musicxml.types.complextypes.notations import Fermata


class Test(TestCase):
    def test_1(self):
        fermata = Fermata()
        notations = Notations()
        notations.add_child(fermata)
        # print(notations.to_string())
        result = '''<notations>
  <fermata>normal</fermata>
</notations>
'''
        self.assertEqual(notations.to_string(), result)
