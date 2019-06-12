"""
    <xs:complexType name="encoding">
        <xs:choice minOccurs="0" maxOccurs="unbounded">
            <xs:element name="software" type="xs:string"/>
            <xs:element name="encoding-description" type="xs:string"/>
            <xs:element name="supports" type="supports"/>
        </xs:choice>
    </xs:complexType>
"""
from musicscore.dtd.dtd import Choice, Element
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.complextypes.supports import ComplexTypeSupports


class EncodingDate(XMLElement):
    """
    <xs:element name="encoding-date" type="yyyy-mm-dd"/>
    """
    _TAG = 'encoding-date'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)
        raise NotImplementedError(self._TAG)


class Encoder(object):
    """
    <xs:element name="encoder" type="typed-text"/>
    """
    _TAG = 'encoder'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)
        raise NotImplementedError(self._TAG)


class Software(object):
    """
    <xs:element name="software" type="xs:string"/>
    """
    _TAG = 'software'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)
        raise NotImplementedError(self._TAG)


class EncodingDescription(object):
    """
    <xs:element name="encoding-description" type="xs:string"/>
    """
    _TAG = 'encoding-description'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)
        raise NotImplementedError(self._TAG)


class Supports(ComplexTypeSupports):
    """
    <xs:element name="supports" type="supports"/>
    """
    _TAG = 'supports'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class ComplexTypeEncoding(ComplexType):
    """
    The encoding element contains information about who did the digital encoding, when, with what software, and in what
     aspects. Standard type values for the encoder element are music, words, and arrangement, but other types may be
     used. The type attribute is only needed when there are multiple encoder element.
    """
    _DTD = Choice(
        Element(EncodingDate),
        Element(Encoder),
        Element(Software),
        Element(EncodingDescription),
        Element(Supports),
        min_occurrence=0,
        max_occurrence=None,
    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
