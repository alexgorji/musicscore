"""
    <xs:complexType name="supports">
        <xs:attribute name="attribute" type="xs:NMTOKEN"/>
        <xs:attribute name="value" type="xs:token"/>
    </xs:complexType>
"""
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeYesNo, Token


class ComplexTypeSupports(ComplexType):
    """
    The supports type indicates if a MusicXML encoding supports a particular MusicXML element. This is recommended for
    elements like beam, stem, and accidental, where the absence of an element is ambiguous if you do not know if the
    encoding supports that element. For Version 2.0, the supports element is expanded to allow programs to indicate
    support for particular attributes or particular values. This lets applications communicate, for example, that all
    system and/or page breaks are contained in the MusicXML file.
    """

    def __init__(self, tag, type_, element, attribute=None, value_=None, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self._ATTRIBUTES = ['attribute', 'element', 'type', 'value']
        self.type_ = type_
        self.element = element
        self.attribute = attribute
        self.value_ = value_

    @property
    def type_(self):
        return self.get_attribute('type')

    @type_.setter
    def type_(self, value):
        if value is None:
            self.remove_attribute('type')
        else:
            TypeYesNo(value)
            self.set_attribute('type', value)

    @property
    def attribute(self):
        return self.get_attribute('attribute')

    @attribute.setter
    def attribute(self, value):
        if value is None:
            self.remove_attribute('attribute')
        else:
            Token(value)
            self.set_attribute('attribute', value)

    @property
    def element(self):
        return self.get_attribute('element')

    @element.setter
    def element(self, value):
        if value is None:
            self.remove_attribute('element')
        else:
            Token(value)
            self.set_attribute('element', value)

    @property
    def value_(self):
        return self.get_attribute('value')

    @value_.setter
    def value_(self, v):
        if v is None:
            self.remove_attribute('value')
        else:
            Token(v)
            self.set_attribute('value', v)
