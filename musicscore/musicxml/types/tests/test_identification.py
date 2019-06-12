from unittest import TestCase

from musicscore.musicxml.types.complextypes.encoding import Supports
from musicscore.musicxml.types.complextypes.identification import Encoding
from musicscore.musicxml.types.complextypes.scorepart import Identification


class Test(TestCase):
    def test_1(self):
        identification = Identification()
        encoding = identification.add_child(Encoding())
        supports = encoding.add_child(Supports(type_='yes', element='print', value_='yes'))
        supports.attribute = 'new-page'

        result = '''<identification>
  <encoding>
    <supports attribute="new-page" element="print" type="yes" value="yes"/>
  </encoding>
</identification>
'''
        self.assertEqual(identification.to_string(), result)
