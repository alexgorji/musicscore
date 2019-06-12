from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract, TypeBeamValue, TypeBeamLevel
from musicscore.musicxml.attributes.color import Color
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from unittest import TestCase


class Repeater(AttributeAbstract):
    def __init__(self, repeater=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('repeater', repeater, 'TypeYesNo')


class Fan(AttributeAbstract):
    def __init__(self, fan=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('fan', fan, 'TypeFan')


class ComplexTypeBeam(ComplexType, TypeBeamValue, Repeater, Fan, Color, OptionalUniqueId):
    """
    documentation>Beam values include begin, continue, end, forward hook, and backward hook. Up to eight concurrent
    beams are available to cover up to 1024th notes. Each beam in a note is represented with a separate beam element,
    starting with the eighth note beam using a number attribute of 1.

    Note that the beam number does not distinguish sets of beams that overlap, as it does for slur and other elements.
    Beaming groups are distinguished by being in different voices and/or the presence or absence of grace and cue
    elements.

    Beams that have a begin value can also have a fan attribute to indicate accelerandos and ritardandos using fanned
    beams. The fan attribute may also be used with a continue value if the fanning direction changes on that note. The
    value is "none" if not specified.

    The repeater attribute has been deprecated in MusicXML 3.0. Formerly used for tremolos, it needs to be specified
    with a "yes" value for each beam using it.
    """

    def __init__(self, value, number=1, *args, **kwargs):
        super().__init__(tag='beam', value=value, *args, **kwargs)
        self.number = number

    @property
    def number(self):
        return self.get_attribute('number')

    @number.setter
    def number(self, value):
        if value is None:
            self.remove_attribute('number')
        else:
            TypeBeamLevel(value)
            self._ATTRIBUTES.insert(0, 'number')
            self.set_attribute('number', value)


class Test(TestCase):

    def setUp(self):
        self.beam = ComplexTypeBeam('begin', number=2, repeater='yes', fan='accel', color='#800080', id='beam1')

    def test_beam(self):
        result = '''<beam number="2" repeater="yes" fan="accel" color="#800080" id="beam1">begin</beam>
'''
        self.assertEqual(self.beam.to_string(), result)

    def run(self):
        self.setUp()
        self.test_beam()
        print('beam tested')
        print()
