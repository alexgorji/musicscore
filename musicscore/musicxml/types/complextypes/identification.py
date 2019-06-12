'''
    <xs:complexType name="identification">
        <xs:sequence>
            <xs:element name="creator" type="typed-text" minOccurs="0" maxOccurs="unbounded">
            </xs:element>
            <xs:element name="rights" type="typed-text" minOccurs="0" maxOccurs="unbounded">
            </xs:element>
            <xs:element name="encoding" type="encoding" minOccurs="0"/>
            <xs:element name="source" type="xs:string" minOccurs="0">
            </xs:element>
            <xs:element name="relation" type="typed-text" minOccurs="0" maxOccurs="unbounded">
                <xs:annotation>
                    <xs:documentation>
                    </xs:documentation>
                </xs:annotation>
            </xs:element>
            <xs:element name="miscellaneous" type="miscellaneous" minOccurs="0"/>
        </xs:sequence>
    </xs:complexType>
'''
from musicscore.dtd.dtd import Sequence, Element
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.complextypes.encoding import ComplexTypeEncoding
from musicscore.musicxml.types.complextypes.typedtext import ComplexTypeTypedText
from musicscore.musicxml.types.simple_type import String


class Rights(ComplexTypeTypedText):
    """The rights element is borrowed from Dublin Core. It contains copyright and other intellectual property notices.
    Words, music, and derivatives can have different types, so multiple rights tags with different type attributes are
    supported. Standard type values are music, words, and arrangement, but other types may be used. The type attribute
    is only needed when there are multiple rights elements."""
    _TAG = 'rights'

    def __init__(self, type=None, *args, **kwargs):
        super().__init__(tag=self._TAG, type=type, *args, **kwargs)


class Creator(ComplexTypeTypedText):
    """
    The creator element is borrowed from Dublin Core. It is used for the creators of the score. The type attribute is
    used to distinguish different creative contributions. Thus, there can be multiple creators within an identification.
    Standard type values are composer, lyricist, and arranger. Other type values may be used for different types of
    creative roles. The type attribute should usually be used even if there is just a single creator element. The
    MusicXML format does not use the creator / contributor distinction from Dublin Core.
    """
    _TAG = 'creator'

    def __init__(self, type=None, *args, **kwargs):
        super().__init__(tag=self._TAG, type=type, *args, **kwargs)


class Relation(ComplexTypeTypedText):
    """
    A related resource for the music that is encoded. This is similar to the Dublin Core relation element.
    Standard type values are music, words, and arrangement, but other types may be used.
    """
    _TAG = 'relation'

    def __init__(self, type=None, *args, **kwargs):
        super().__init__(tag=self._TAG, type=type, *args, **kwargs)


class Encoding(ComplexTypeEncoding):
    _TAG = 'encoding'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Source(XMLElement, String):
    """
    The source for the music that is encoded. This is similar to the Dublin Core source element.
    """
    _TAG = 'source'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class Miscellaneus(XMLElement):
    """
    <xs:element name="miscellaneus" type="miscellaneus"/>
    """
    _TAG = 'miscellaneus'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)
        raise NotImplementedError(self._TAG)


class ComplexTypeIdentification(ComplexType):
    """
    Identification contains basic metadata about the score. It includes the information in MuseData headers
    that may apply at a score-wide, movement-wide, or part-wide level. The creator, rights,
    source, and relation elements are based on Dublin Core.
    """
    _DTD = Sequence(
        Element(Creator,
                min_occurrence=0,
                max_occurrence=None),
        Element(Rights,
                min_occurrence=0,
                max_occurrence=None),
        Element(Encoding,
                min_occurrence=0),
        Element(Source,
                min_occurrence=0),
        Element(Relation,
                min_occurrence=0,
                max_occurrence=None),
        Element(Miscellaneus,
                min_occurrence=0)
    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
