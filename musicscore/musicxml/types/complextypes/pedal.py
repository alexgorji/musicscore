"""
<xs:complexType name="pedal">
        <xs:attribute name="type" type="pedal-type" use="required"/>
        <xs:attribute name="number" type="number-level"/>
        <xs:attribute name="line" type="yes-no"/>
        <xs:attribute name="sign" type="yes-no"/>
        <xs:attribute name="abbreviated" type="yes-no"/>
        <xs:attributeGroup ref="print-style-align"/>
        <xs:attributeGroup ref="optional-unique-id"/>
    </xs:complexType>
"""
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.printstyle import PrintStyleAlign
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeNumberLevel, TypeYesNo, TypePedalType


class ComplexTypePedal(ComplexType, PrintStyleAlign, OptionalUniqueId):
    """The pedal type represents piano pedal marks. In MusicXML 3.1 this includes sostenuto as well as damper pedal
    marks. The line attribute is yes if pedal lines are used. The sign attribute is yes if Ped, Sost, and * signs are
    used. For MusicXML 2.0 compatibility, the sign attribute is yes by default if the line attribute is no, and is no
    by default if the line attribute is yes. If the sign attribute is set to yes and the type is start or sostenuto,
    the abbreviated attribute is yes if the short P and S signs are used, and no if the full Ped and Sost signs are
    used. It is no by default. Otherwise the abbreviated attribute is ignored.

    The change and continue types are used when the line attribute is yes. The change type indicates a pedal lift and
    retake indicated with an inverted V marking. The continue type allows more precise formatting across system breaks
    and for more complex pedaling lines. The alignment attributes are ignored if the line attribute is yes."""

    def __init__(self, tag, type, line='no', *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.line = line
        self.type = type

    @property
    def type(self):
        return self.get_attribute('type')

    @type.setter
    def type(self, value):
        if value is None:
            self.remove_attribute('type')
        else:
            TypePedalType(value)
            self._ATTRIBUTES.insert(0, 'type')
            self.set_attribute('type', value)

    @property
    def number(self):
        return self.get_attribute('number')

    @number.setter
    def number(self, value):
        if value is None:
            self.remove_attribute('number')
        else:
            TypeNumberLevel(value)
            self._ATTRIBUTES.insert(0, 'number')
            self.set_attribute('number', value)

    @property
    def line(self):
        return self.get_attribute('line')

    @line.setter
    def line(self, value):
        if value is None:
            self.remove_attribute('line')
        else:
            TypeYesNo(value)
            self._ATTRIBUTES.insert(0, 'line')
            self.set_attribute('line', value)

    @property
    def sign(self):
        return self.get_attribute('sign')

    @sign.setter
    def sign(self, value):
        if value is None:
            self.remove_attribute('sign')
        else:
            TypeYesNo(value)
            self._ATTRIBUTES.insert(0, 'sign')
            self.set_attribute('sign', value)

    @property
    def abbreviated(self):
        return self.get_attribute('abbreviated')

    @abbreviated.setter
    def abbreviated(self, value):
        if value is None:
            self.remove_attribute('abbreviated')
        else:
            TypeYesNo(value)
            self._ATTRIBUTES.insert(0, 'abbreviated')
            self.set_attribute('abbreviated', value)
