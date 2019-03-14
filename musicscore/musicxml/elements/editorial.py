"""
	<xs:group name="editorial">
		<xs:annotation>
			<xs:documentation>The editorial group specifies editorial information for a musical element.</xs:documentation>
		</xs:annotation>
		<xs:sequence>
			<xs:group ref="footnote" minOccurs="0"/>
			<xs:group ref="level" minOccurs="0"/>
		</xs:sequence>
	</xs:group>
"""
from musicscore.dtd.dtd import Group, Sequence, Element
from musicscore.musicxml.types.complex_type import TypeLevel

Footnote = Sequence(

)


class Level(TypeLevel):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='level', *args, **kwargs)


"""
The level element specifies editorial information for different MusicXML elements. It is defined within a group due to 
its multiple uses within the MusicXML schema.
"""
Level = Sequence(
    Element(Level)
)

"""
The editorial group specifies editorial information for a musical element.
"""
Editorial = Sequence(
    Group(Footnote, min_occurrence=0),
    Group(Level, min_occurrence=0)

)
