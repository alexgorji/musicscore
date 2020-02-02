from musicscore.dtd.dtd import Sequence, GroupReference, Element
from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract
from musicscore.musicxml.attributes.barline import BarlineAttributes
from musicscore.musicxml.attributes.color import Color
from musicscore.musicxml.groups.common import Editorial
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.complextypes.segno import ComplexTypeSegno
from musicscore.musicxml.types.simple_type import TypeBarStyle, TypeBackwardForward
from musicscore.musicxml.elements.xml_element import XMLElement


class WavyLine(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='wavy-line', *args, **kwargs)
        raise NotImplementedError('WavyLine')


class Segno(ComplexTypeSegno):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='segno', *args, **kwargs)


class Coda(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='coda', *args, **kwargs)
        raise NotImplementedError()


class Fermata(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='fermata', *args, **kwargs)
        raise NotImplementedError('Fermata')


class Ending(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='ending', *args, **kwargs)
        raise NotImplementedError('Ending')


class Times(AttributeAbstract):

    def __init__(self, times=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('times', times, 'NonNegativeInteger')


class Winged(AttributeAbstract):

    def __init__(self, winged=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('winged', winged, 'TypeWinged')


class ComplexTypeRepeat(ComplexType, Times, Winged):
    """The repeat type represents repeat marks. The start of the repeat has a forward direction while the end of the
    repeat has a backward direction. Backward repeats that are not part of an ending can use the times attribute to
    indicate the number of times the repeated section is played.
    """

    def __init__(self, tag, direction, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.direction = direction

    @property
    def direction(self):
        return self.get_attribute('direction')

    @direction.setter
    def direction(self, value):
        if value is None:
            self.remove_attribute('direction')
        else:
            TypeBackwardForward(value)
            self._ATTRIBUTES.(0, 'direction')
            self.set_attribute('direction', value)


class Repeat(ComplexTypeRepeat):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='repeat', *args, **kwargs)


'''
	<xs:complexType name="barline">
		<xs:sequence>
			<xs:element name="bar-style" type="bar-style-color" minOccurs="0"/>
			<xs:group ref="editorial"/>
			<xs:element name="wavy-line" type="wavy-line" minOccurs="0"/>
			<xs:element name="segno" type="segno" minOccurs="0"/>
			<xs:element name="coda" type="coda" minOccurs="0"/>
			<xs:element name="fermata" type="fermata" minOccurs="0" maxOccurs="2"/>
			<xs:element name="ending" type="ending" minOccurs="0"/>
			<xs:element name="repeat" type="repeat" minOccurs="0"/>
		</xs:sequence>
		<xs:attribute name="location" type="right-left-middle" default="right"/>
		<xs:attribute name="segno" type="xs:token"/>
		<xs:attribute name="coda" type="xs:token"/>
		<xs:attribute name="divisions" type="divisions"/>
		<xs:attributeGroup ref="optional-unique-id"/>
	</xs:complexType>
'''


class ComplexTypeBarStyleColor(ComplexType, TypeBarStyle, Color):
    """
    The bar-style-color type contains barline style and color information.
    """

    def __init__(self, tag, value, *args, **kwargs):
        super().__init__(tag=tag, value=value, *args, **kwargs)


class BarStyle(ComplexTypeBarStyleColor):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='bar-style', *args, **kwargs)


class ComplexTypeBarline(ComplexType, BarlineAttributes):
    """
    If a barline is other than a normal single barline, it should be represented by a barline type that describes it.
    This includes information about repeats and multiple endings, as well as line style. Barline data is on the same
    level as the other musical data in a score - a child of a measure in a partwise score, or a part in a timewise
    score. This allows for barlines within measures, as in dotted barlines that subdivide measures in complex meters.
    The two fermata elements allow for fermatas on both sides of the barline (the lower one inverted).

    Barlines have a location attribute to make it easier to process barlines independently of the other musical data in
    a score. It is often easier to set up measures separately from entering notes. The location attribute must match
    where the barline element occurs within the rest of the musical data in the score. If location is left, it should be
    the first element in the measure, aside from the print, bookmark, and link elements. If location is right, it should
    be the last element, again with the possible exception of the print, bookmark, and link elements. If no location is
    specified, the right barline is the default. The segno, coda, and divisions attributes work the same way as in the
    sound element. They are used for playback when barline elements contain segno or coda child elements.
    """
    _DTD = Sequence(
        Element(BarStyle, min_occurrence=0),
        GroupReference(Editorial),
        Element(WavyLine, min_occurrence=0),
        Element(Segno, min_occurrence=0),
        Element(Coda, min_occurrence=0),
        Element(Fermata, min_occurrence=0, max_occurrence=2),
        Element(Ending, min_occurrence=0),
        Element(Repeat, min_occurrence=0)
    )

    def __init__(self, *args, **kwargs):
        super().__init__(tag='barline', *args, **kwargs)
