'''
	<xs:group name="music-data">
		<xs:annotation>
			<xs:documentation>The music-data group contains the basic musical data that is either associated with a part or a measure, depending on whether the partwise or timewise hierarchy is used.</xs:documentation>
		</xs:annotation>
		<xs:sequence>
			<xs:choice minOccurs="0" maxOccurs="unbounded">
				<xs:element name="note" type="note"/>
				<xs:element name="backup" type="backup"/>
				<xs:element name="forward" type="forward"/>
				<xs:element name="direction" type="direction"/>
				<xs:element name="attributes" type="attributes"/>
				<xs:element name="harmony" type="harmony"/>
				<xs:element name="figured-bass" type="figured-bass"/>
				<xs:element name="print" type="print"/>
				<xs:element name="sound" type="sound"/>
				<xs:element name="barline" type="barline"/>
				<xs:element name="grouping" type="grouping"/>
				<xs:element name="link" type="link"/>
				<xs:element name="bookmark" type="bookmark"/>
			</xs:choice>
		</xs:sequence>
	</xs:group>
'''

from musicscore.musicxml.elements.xml_element import XMLElementGroup, XMLElement
from musicscore.dtd.dtd import Group, Sequence, Choice, Element
from musicscore.dtd.note import Note


class Backup(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='backup', *args, **kwargs)


class Forward(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='forward', *args, **kwargs)


class Direction(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='direction', *args, **kwargs)


class Attributes(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='attributes', *args, **kwargs)


class Sound(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='sound', *args, **kwargs)


class Barline(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='barline', *args, **kwargs)


class Link(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='link', *args, **kwargs)


class Bookmark(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='bookmark', *args, **kwargs)


class MusicData(XMLElementGroup):
    """"""

    _DTD = Sequence(
        Choice(
            Element(Note),
            Element(Backup),
            Element(Forward),
            Element(Direction),
            Element(Attributes),
            Element(Sound),
            Element(Barline),
            Element(Link),
            Element(Bookmark),
            min_occurrence=0,
            max_occurrence=None
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def reset_children(self):
        self.clear_children()
        self._DTD._possibility_index = 0

    def add_child(self, child):
        self._DTD.check_child_type(self, child)
        self._DTD.check_child_max_occurrence(self, child)
        self._children.append(child)
        return child

    def sort_children(self):
        self._DTD.sort_children(self)

    def close(self):
        self._DTD.close(self)