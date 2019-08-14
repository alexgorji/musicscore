"""
   <xs:complexType name="tremolo">
        <xs:simpleContent>
            <xs:extension base="tremolo-marks">
                <xs:attribute name="type" type="tremolo-type" default="single"/>
            </xs:extension>
        </xs:simpleContent>
    </xs:complexType>
"""
from musicscore.musicxml.attributes.accidental import Smulf
from musicscore.musicxml.attributes.placement import Placement
from musicscore.musicxml.attributes.printstyle import PrintStyle
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeTremoloType, TypeTremoloMarks


class ComplexTypeTremolo(ComplexType, TypeTremoloMarks, PrintStyle, Placement, Smulf):
    """
    The tremolo ornament can be used to indicate single-note, double-note, or unmeasured tremolos. Single-note tremolos
    use the single type, double-note tremolos use the start and stop types, and unmeasured tremolos use the unmeasured
    type. The default is "single" for compatibility with Version 1.1. The text of the element indicates the number of
    tremolo marks and is an integer from 0 to 8. Note that the number of attached beams is not included in this value,
    but is represented separately using the beam element. The value should be 0 for unmeasured tremolos.

    When using double-note tremolos, the duration of each note in the tremolo should correspond to half of the notated
    type value. A time-modification element should also be added with an actual-notes value of 2 and a normal-notes
    value of 1. If used within a tuplet, this 2/1 ratio should be multiplied by the existing tuplet ratio.

    The smufl attribute specifies the glyph to use from the SMuFL tremolos range for an unmeasured tremolo. It is
    ignored for other tremolo types. The SMuFL buzzRoll glyph is used by default if the attribute is missing.

    Using repeater beams for indicating tremolos is deprecated as of MusicXML 3.0.
    """

    def __init__(self, tag, type='single', *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.type = type

    @property
    def type(self):
        return self.get_attribute('type')

    @type.setter
    def type(self, value):
        if value is None:
            self.remove_attribute('type')
        else:
            TypeTremoloType(value)
            self._ATTRIBUTES.insert(0, 'type')
            self.set_attribute('type', value)
