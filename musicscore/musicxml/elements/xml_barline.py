from musicscore.musicxml.attributes.barline import BarlineAttributes
from musicscore.musicxml.types.simple_type import BarStyleType
from musicscore.musicxml.elements.xml_element import XMLElement2


class XMLBarStyle(XMLElement2, BarStyleType):

    """Bar-style contains style information. Choices are regular, dotted, dashed, heavy, light-light, light-heavy,
    heavy-light, heavy-heavy, tick (a short stroke through the top line), short (a partial barline between the 2nd
    and 4th lines), and none.
    <!ELEMENT bar-style (#PCDATA)>
    <!ATTLIST bar-style
        %color;
    >
    """

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag='bar-style', value=value, *args, **kwargs)





class XMLBarline(XMLElement2, BarlineAttributes):
    """
         <xs:complexType name="barline">
         <xs:annotation>
             <xs:documentation>If a barline is other than a normal single barline, it should be represented by a barline type that describes it. This includes information about repeats and multiple endings, as well as line style. Barline data is on the same level as the other musical data in a score - a child of a measure in a partwise score, or a part in a timewise score. This allows for barlines within measures, as in dotted barlines that subdivide measures in complex meters. The two fermata elements allow for fermatas on both sides of the barline (the lower one inverted).

 Barlines have a location attribute to make it easier to process barlines independently of the other musical data in a score. It is often easier to set up measures separately from entering notes. The location attribute must match where the barline element occurs within the rest of the musical data in the score. If location is left, it should be the first element in the measure, aside from the print, bookmark, and link elements. If location is right, it should be the last element, again with the possible exception of the print, bookmark, and link elements. If no location is specified, the right barline is the default. The segno, coda, and divisions attributes work the same way as in the sound element. They are used for playback when barline elements contain segno or coda child elements.</xs:documentation>
         </xs:annotation>
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
     """
    # _ATTRIBUTES = BarlineAttributes._ATTRIBUTES
    # _CHILDREN_TYPES = [XMLBarStyle]
    # _CHILDREN_ORDERED = True

    def __init__(self, *args, **kwargs):
        super().__init__(tag='barline', *args, **kwargs)
