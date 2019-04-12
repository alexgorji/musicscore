'''
	<xs:complexType name="notations">
		<xs:sequence>
			<xs:group ref="editorial"/>
			<xs:choice minOccurs="0" maxOccurs="unbounded">
				<xs:element name="tied" type="tied"/>
				<xs:element name="slur" type="slur"/>
				<xs:element name="tuplet" type="tuplet"/>
				<xs:element name="glissando" type="glissando"/>
				<xs:element name="slide" type="slide"/>
				<xs:element name="ornaments" type="ornaments"/>
				<xs:element name="technical" type="technical"/>
				<xs:element name="articulations" type="articulations"/>
				<xs:element name="dynamics" type="dynamics"/>
				<xs:element name="fermata" type="fermata"/>
				<xs:element name="arpeggiate" type="arpeggiate"/>
				<xs:element name="non-arpeggiate" type="non-arpeggiate"/>
				<xs:element name="accidental-mark" type="accidental-mark"/>
				<xs:element name="other-notation" type="other-notation"/>
			</xs:choice>
		</xs:sequence>
		<xs:attributeGroup ref="print-object"/>
		<xs:attributeGroup ref="optional-unique-id"/>
	</xs:complexType>
'''

from musicscore.dtd.dtd import Sequence, GroupReference, Choice, Element
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.printobject import PrintObject
from musicscore.musicxml.common.common import Editorial
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.complextypes.slur import ComplexTypeSlur
from musicscore.musicxml.types.simple_type import TypeTiedType


class Tied(XMLElement, TypeTiedType):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='tied', value=value, *args, **kwargs)


class Slur(ComplexTypeSlur):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='slur', value=value, *args, **kwargs)
        raise NotImplementedError()


class Tuplet(XMLElement):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='tuplet', value=value, *args, **kwargs)
        raise NotImplementedError()


class Glissando(XMLElement):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='glissando', value=value, *args, **kwargs)
        raise NotImplementedError()


class Slide(XMLElement):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='slide', value=value, *args, **kwargs)
        raise NotImplementedError()


class Ornaments(XMLElement):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='ornaments', value=value, *args, **kwargs)
        raise NotImplementedError()


class Technical(XMLElement):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='technical', value=value, *args, **kwargs)
        raise NotImplementedError()


class Articulations(XMLElement):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='articulations', value=value, *args, **kwargs)
        raise NotImplementedError()


class Dynamics(XMLElement):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='dynamics', value=value, *args, **kwargs)
        raise NotImplementedError()


class Fermata(XMLElement):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='fermata', value=value, *args, **kwargs)
        raise NotImplementedError()


class Arpeggiate(XMLElement):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='arpeggiate', value=value, *args, **kwargs)
        raise NotImplementedError()


class NonArpeggiate(XMLElement):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='non-arpeggiate', value=value, *args, **kwargs)
        raise NotImplementedError()


class AccidentalMark(XMLElement):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='accidental-mark', value=value, *args, **kwargs)
        raise NotImplementedError()


class OtherNotation(XMLElement):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='other-notation', value=value, *args, **kwargs)
        raise NotImplementedError()


class ComplexTypeNotations(ComplexType, PrintObject, OptionalUniqueId):
    """
    Notations refer to musical notations, not XML notations. Multiple notations are allowed in order to represent
    multiple editorial levels. The print-object attribute, added in Version 3.0, allows notations to represent details
    of performance technique, such as fingerings, without having them appear in the score.
    """
    _DTD = Sequence(
        GroupReference(Editorial),
        Choice(
            Element(Tied),
            Element(Slur),
            Element(Tuplet),
            Element(Glissando),
            Element(Slide),
            Element(Ornaments),
            Element(Technical),
            Element(Articulations),
            Element(Dynamics),
            Element(Fermata),
            Element(Arpeggiate),
            Element(NonArpeggiate),
            Element(AccidentalMark),
            Element(OtherNotation),
            min_occurrence=0,
            max_occurrence=None
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(tag='notations', *args, **kwargs)
