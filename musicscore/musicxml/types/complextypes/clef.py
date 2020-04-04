from musicscore.dtd.dtd import Sequence, Element
from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract, TypeStaffLine
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.printobject import PrintObject
from musicscore.musicxml.attributes.printstyle import PrintStyle
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeClefSign, Integer, TypeStaffNumber, TypeYesNo, TypeSymbolSize


class Sign(XMLElement, TypeClefSign):
    """
    The sign element represents the clef symbol.
    """
    _TAG = 'sign'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class Line(XMLElement, TypeStaffLine):
    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='line', value=value, *args, **kwargs)


class ClefOctaveChange(XMLElement, Integer):
    """
    The clef-octave-change element is used for transposing clefs. A treble clef for tenors would have a value of -1.
    """
    _TAG = 'clef-octave-change'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


'''
        <xs:attribute name="number" type="staff-number"/>
        <xs:attribute name="additional" type="yes-no"/>
        <xs:attribute name="size" type="symbol-size"/>
        <xs:attribute name="after-barline" type="yes-no"/>
        <xs:attributeGroup ref="print-style"/>
        <xs:attributeGroup ref="print-object"/>
        <xs:attributeGroup ref="optional-unique-id"/>
'''


class AfterBarline(AttributeAbstract):
    """"""

    def __init__(self, after_barline=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('after-barline', after_barline, "TypeYesNo")

class Additional(AttributeAbstract):
    """"""

    def __init__(self, additional=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('additional', additional, "TypeYesNo")
        TypeYesNo

class Size(AttributeAbstract):
    """"""

    def __init__(self, size=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('size', size, 'TypeSymbolSize')
        TypeSymbolSize


class ComplexTypeClef(ComplexType, PrintStyle, PrintObject, OptionalUniqueId, Additional, Size, AfterBarline):
    """
    Clefs are represented by a combination of sign, line, and clef-octave-change elements. The optional number attribute
    refers to staff numbers within the part. A value of 1 is assumed if not present. Sometimes clefs are added to the
    staff in non-standard line positions, either to indicate cue passages, or when there are multiple clefs present
    simultaneously on one staff. In this situation, the additional attribute is set to "yes" and the line value is
    ignored. The size attribute is used for clefs where the additional attribute is "yes". It is typically used to
    indicate cue clefs.

    Sometimes clefs at the start of a measure need to appear after the barline rather than before, as for cues or for
    use after a repeated section. The after-barline attribute is set to "yes" in this situation. The attribute is
    ignored for mid-measure clefs.

    Clefs appear at the start of each system unless the print-object attribute has been set to "no" or the additional
    attribute has been set to "yes".
    """

    '''
            <xs:attribute name="number" type="staff-number"/>
        <xs:attribute name="additional" type="yes-no"/>
        <xs:attribute name="size" type="symbol-size"/>
        <xs:attribute name="after-barline" type="yes-no"/>
        <xs:attributeGroup ref="print-style"/>
        <xs:attributeGroup ref="print-object"/>
        <xs:attributeGroup ref="optional-unique-id"/>'''
    _DTD = Sequence(
        Element(Sign),
        Element(Line, min_occurrence=0),
        Element(ClefOctaveChange, min_occurrence=0)
    )

    def __init__(self, tag, number=None, *args, **kwargs):
        super().__init__(tag=tag, *args, ** kwargs)
        self.number = number

    @property
    def number(self):
        try:
            return self.get_attribute('number')
        except KeyError:
            return None

    @number.setter
    def number(self, value):
        if value is None:
            self.remove_attribute('number')
        else:
            TypeStaffNumber(value)
            self._ATTRIBUTES.insert(0, 'number')
            self.set_attribute('number', value)
