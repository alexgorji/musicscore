from musicscore.dtd.dtd import Sequence, Choice, Element, GroupReference
from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract, BeamValue
from musicscore.musicxml.attributes.color import Color
from musicscore.musicxml.attributes.justify import Justify
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.placement import Placement
from musicscore.musicxml.attributes.position import Position
from musicscore.musicxml.attributes.print_object import PrintObject
from musicscore.musicxml.attributes.time_only import TimeOnly
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complex_type import ComplexType


class Number(AttributeAbstract):
    def __init__(self, number=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('number', number, 'Token')


class Name(AttributeAbstract):
    def __init__(self, name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('name', name, 'Token')


class Sylabic(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='sylabic', *args, **kwargs)
        raise NotImplementedError()


class Text(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='text', *args, **kwargs)
        raise NotImplementedError()


class Elision(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='elision', *args, **kwargs)
        raise NotImplementedError()


class Extend(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='extend', *args, **kwargs)
        raise NotImplementedError()


class Laughing(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='laughing', *args, **kwargs)
        raise NotImplementedError()


class Humming(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='humming', *args, **kwargs)
        raise NotImplementedError()


class EndParagraph(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='end-paragraph', *args, **kwargs)
        raise NotImplementedError()


class TypeLyric(ComplexType, Number, Name, Justify, Position, Placement, Color, PrintObject, TimeOnly,
                OptionalUniqueId):
    """The lyric type represents text underlays for lyrics, based on Humdrum with support for other formats. Two text
    elements that are not separated by an elision element are part of the same syllable, but may have different text
    formatting. The MusicXML XSD is more strict than the DTD in enforcing this by disallowing a second syllabic element
    unless preceded by an elision element. The lyric number indicates multiple lines, though a name can be used as well
    (as in Finale's verse / chorus / section specification).

    Justification is center by default; placement is below by default. The print-object attribute can override a note's
    print-lyric attribute in cases where only some lyrics on a note are printed, as when lyrics for later verses are
    printed in a block of text rather than with each note. The time-only attribute precisely specifies which lyrics are
    to be sung which time through a repeated section.
		<xs:sequence>
			<xs:choice>
				<xs:sequence>
					<xs:element name="syllabic" type="syllabic" minOccurs="0"/>
					<xs:element name="text" type="text-element-data"/>
					<xs:sequence minOccurs="0" maxOccurs="unbounded">
						<xs:sequence minOccurs="0">
							<xs:element name="elision" type="elision"/>
							<xs:element name="syllabic" type="syllabic" minOccurs="0"/>
						</xs:sequence>
						<xs:element name="text" type="text-element-data"/>
					</xs:sequence>
					<xs:element name="extend" type="extend" minOccurs="0"/>
				</xs:sequence>
				<xs:element name="extend" type="extend"/>
				<xs:element name="laughing" type="empty">
				<xs:element name="humming" type="empty">
				</xs:element>
			</xs:choice>
			<xs:element name="end-line" type="empty" minOccurs="0">
			<xs:element name="end-paragraph" type="empty" minOccurs="0">
			<xs:group ref="editorial"/>
		</xs:sequence>
    """
    _DTD = Sequence(
        Choice(
            Sequence(
                Element(Sylabic, min_occurrence=0),
                Element(Text),
                Sequence(
                    Sequence(
                        Element(Elision),
                        Element(Sylabic, min_occurrence=0),
                        min_occurrence=0
                    ),
                    Element(Text),
                    min_occurrence=0,
                    max_occurrence=None
                ),
                Element(Extend, min_occurrence=0)
            ),
            Element(Extend),
            Element(Laughing),
            Element(Humming)
        ),
        Element(EndParagraph, min_occurrence=0),
        GroupReference(Editorial)

    )


def __init__(self, value, *args, **kwargs):
    super().__init__(tag='beam', value=value, *args, **kwargs)
