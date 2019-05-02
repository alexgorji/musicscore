from musicscore.dtd.dtd import Sequence, Element, GroupReference
from musicscore.musicxml.groups.layout import Layout
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.complextypes.scaling import ComplexTypeScaling


class Scaling(ComplexTypeScaling):
    _TAG = 'scaling'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class ComplexTypeDefaults(ComplexType):
    """
    The defaults type specifies score-wide defaults for scaling, layout, and appearance.
    """

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)

    _DTD = Sequence(
        Element(Scaling, min_occurrence=0),
        GroupReference(Layout)
    )


'''
    <xs:complexType name="defaults">
        <xs:sequence>
            <xs:element name="scaling" type="scaling" minOccurs="0"/>
            <xs:group ref="layout"/>
            <xs:element name="appearance" type="appearance" minOccurs="0"/>
            <xs:element name="music-font" type="empty-font" minOccurs="0"/>
            <xs:element name="word-font" type="empty-font" minOccurs="0"/>
            <xs:element name="lyric-font" type="lyric-font" minOccurs="0" maxOccurs="unbounded"/>
            <xs:element name="lyric-language" type="lyric-language" minOccurs="0" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
'''
