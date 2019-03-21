from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract, BeamValue
from musicscore.musicxml.attributes.color import Color
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.types.complex_type import ComplexType


class Number(AttributeAbstract):
    def __init__(self, number=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('number', number, 'BeamLevel')


class Repeater(AttributeAbstract):
    def __init__(self, repeater=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('repeater', repeater, 'YesNo')


class Fan(AttributeAbstract):
    def __init__(self, fan=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('fan', fan, 'Fan')


class TypeBeam(ComplexType, BeamValue, Number, Repeater, Fan, Color, OptionalUniqueId):
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

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='beam', value=value, *args, **kwargs)
