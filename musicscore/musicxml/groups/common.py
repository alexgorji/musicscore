from musicscore.dtd.dtd import Sequence, Element
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.formattedtext import ComplexTypeFormattedText
from musicscore.musicxml.types.complextypes.level import ComplexTypeLevel
from musicscore.musicxml.types.simple_type import String, PositiveInteger


class FootNote(ComplexTypeFormattedText):
    """
    The footnote element specifies editorial information that appears in footnotes in the printed score. It is defined
    within a group due to its multiple uses within the MusicXML schema.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='footnote', value=value, *args, **kwargs)


class Level(ComplexTypeLevel):
    """
    The level element specifies editorial information for different MusicXML elements. It is defined within a group due
    to its multiple uses within the MusicXML schema.
    """

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


"""
The editorial group specifies editorial information for a musical element.
"""
Editorial = Sequence(
    Element(FootNote, min_occurrence=0),
    Element(Level, min_occurrence=0)
)


class Voice(XMLElement, String):
    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag='voice', value=value, *args, **kwargs)


'''
The editorial-voice group supports the common combination of editorial and voice information for a musical element
'''
EditorialVoice = Sequence(
    Element(FootNote, min_occurrence=0),
    Element(Level, min_occurrence=0),
    Element(Voice, min_occurrence=0)

)

"""
The editorial-voice-direction group supports the common combination of editorial and voice information for a direction 
element. It is separate from the editorial-voice element because extensions and restrictions might be different for 
directions than for the note and forward elements.
"""

EditorialVoiceDirection = Sequence(
    Element(FootNote, min_occurrence=0),
    Element(Level, min_occurrence=0),
    Element(Voice, min_occurrence=0)
)

'''
	<xs:group name="staff">
		<xs:annotation>
			<xs:documentation>The staff element is defined within a group due to its use by both notes and direction elements.</xs:documentation>
		</xs:annotation>
		<xs:sequence>
			<xs:element name="staff" type="xs:positiveInteger">
				<xs:annotation>
					<xs:documentation></xs:documentation>
				</xs:annotation>
			</xs:element>
		</xs:sequence>
	</xs:group>
'''


class StaffElement(XMLElement, PositiveInteger):
    """
    Staff assignment is only needed for music notated on multiple staves. Used by both notes and directions.
    Staff valuesare numbers, with 1 referring to the top-most staff in a part.
    """
    _TAG = 'staff'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


Staff = Sequence(
    Element(StaffElement)
)
