from musicscore.dtd.dtd import Sequence, Element
from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract
from musicscore.musicxml.attributes.printobject import PrintObject
from musicscore.musicxml.attributes.printspacing import PrintSpacing
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeStaffType, NonNegativeInteger, NonNegativeDecimal, \
    TypeStaffNumber, TypeShowFrets

"""
    <xs:complexType name="staff-details">
        <xs:sequence>
            <xs:element name="staff-type" type="staff-type" minOccurs="0"/>
            <xs:element name="staff-lines" type="xs:nonNegativeInteger" minOccurs="0">
            </xs:element>
            <xs:element name="staff-tuning" type="staff-tuning" minOccurs="0" maxOccurs="unbounded"/>
            <xs:element name="capo" type="xs:nonNegativeInteger" minOccurs="0">
                <xs:annotation>
                    <xs:documentation>
                    </xs:documentation>
                </xs:annotation>
            </xs:element>
            <xs:element name="staff-size" type="non-negative-decimal" minOccurs="0">
                <xs:annotation>
                    <xs:documentation>
                    </xs:documentation>
                </xs:annotation>
            </xs:element>
        </xs:sequence>
        <xs:attribute name="number" type="staff-number"/>
        <xs:attribute name="show-frets" type="show-frets"/>
        <xs:attributeGroup ref="print-object"/>
        <xs:attributeGroup ref="print-spacing"/>
    </xs:complexType>
"""


class StaffType(XMLElement, TypeStaffType):
    """
    """
    _TAG = 'staff-type'

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class StaffLines(XMLElement, NonNegativeInteger):
    """
    The staff-lines element specifies the number of lines for a non 5-line staff.
    """
    _TAG = 'staff-lines'

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class StaffTuning(XMLElement):
    """
    """
    _TAG = 'staff-tuning'

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)
        raise NotImplementedError()


class Capo(XMLElement, NonNegativeInteger):
    """
    The capo element indicates at which fret a capo should be placed on a fretted instrument. This changes the open
    tuning of the strings specified by staff-tuning by the specified number of half-steps.
    """
    _TAG = 'capo'

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class StaffSize(XMLElement, NonNegativeDecimal):
    """
    The staff-size element indicates how large a staff space is on this staff, expressed as a percentage of the work's
    default scaling. Values less than 100 make the staff space smaller while values over 100 make the staff space
    larger. A staff-type of cue, ossia, or editorial implies a staff-size of less than 100, but the exact value is
    implementation-dependent unless specified here. Staff size affects staff height only, not the relationship of the
    staff to the left and right margins.
    """
    _TAG = 'staff-size'

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class ShowFrets(AttributeAbstract):

    def __init__(self, show_frets=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('show-frets', show_frets, 'TypeShowFrets')
        TypeShowFrets


class ComplexTypeStaffDetails(ComplexType, ShowFrets, PrintObject, PrintSpacing):
    """ The staff-details element is used to indicate different types of staves. The optional number
    attribute specifies the staff number from top to bottom on the system, as with clef. The print-object
    attribute is used to indicate when a staff is not printed in a part, usually in large scores where empty
    parts are omitted. It is yes by default. If print-spacing is yes while print-object is no, the score is
    printed in cutaway format where vertical space is left for the empty part.
    """
    _DTD = Sequence(
        Element(StaffType, min_occurrence=0),
        Element(StaffLines, min_occurrence=0),
        Element(StaffTuning, min_occurrence=0, max_occurrence=None),
        Element(Capo, min_occurrence=0),
        Element(StaffSize, min_occurrence=0),

    )

    def __init__(self, tag, number=1, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.number = number

    @property
    def number(self):
        return self.get_attribute('number')

    @number.setter
    def number(self, value):
        if value is None:
            self.remove_attribute('number')
        else:
            TypeStaffNumber(value)
            self._ATTRIBUTES.insert(0, 'number')
            self.set_attribute('number', value)
