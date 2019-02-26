from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.elements.xml_music_data import XMLMusicData
from musicscore.musicxml.types.simple_type import PositiveDevisions, ClefSign, StaffLine, PositiveInteger
from musicscore.musicxml.attributes.print_object import PrintObject


class XMLDivisions(XMLElement, PositiveDevisions):
    """
    Musical notation duration is commonly represented as fractions.
    The divisions element indicates how many divisions per quarter note are used to indicate a note's duration.
    For example, if duration = 1 and divisions = 2, this is an eighth note duration.
    Duration and divisions are used directly for generating sound output, so they must be chosen to take tuplets into
    account. Using a divisions element lets us use just one number to represent a duration for each note in the score,
    while retaining the full power of a fractional representation.
    If maximum compatibility with Standard MIDI 1.0 files is important, do not have the divisions value exceed 16383.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='divisions', value=value, *args, **kwargs)


class XMLTime(XMLElement, PrintObject):
    """
    Time signatures are represented by the beats element for the numerator and the beat-type element for the denominator.
    """

    class XMLBeats(XMLElement, PositiveInteger):
        """
        The beats element indicates the number of beats, as found in the numerator of a time signature.
        """

        def __init__(self, value, *args, **kwargs):
            super().__init__(tag='beats', value=value, *args, **kwargs)

    class XMLBeatType(XMLElement, PositiveInteger):
        """
        The beat-type element indicates the beat unit, as found in the denominator of a time signature.
        """

        def __init__(self, value, *args, **kwargs):
            super().__init__(tag='beat-type', value=value, *args, **kwargs)

    _CHILDREN_TYPES = [XMLBeats, XMLBeatType]
    _CHILDREN_ORDERED = True

    def __init__(self, beats, beat_type, *args, **kwargs):
        super().__init__(tag='time', *args, **kwargs)
        self._beats = None
        self._beat_type = None
        self.beats = beats
        self.beat_type = beat_type

    @property
    def beats(self):
        return self._beats

    @beats.setter
    def beats(self, value):
        self._set_child(self.XMLBeats, 'beats', value)

    @property
    def beat_type(self):
        return self._beat_type

    @beat_type.setter
    def beat_type(self, value):
        self._set_child(self.XMLBeatType, 'beat-type', value)


class XMLClef(XMLElement):
    """
    Clefs are represented by a combination of sign, line, and clef-octave-change elements.
    The optional number attribute refers to staff numbers within the part.
    A value of 1 is assumed if not present.
    Sometimes clefs are added to the staff in non-standard line positions, either to indicate cue passages,
    or when there are multiple clefs present simultaneously on one staff. In this situation,
    the additional attribute is set to "yes" and the line value is ignored.
    The size attribute is used for clefs where the additional attribute is "yes".
    It is typically used to indicate cue clefs.

    Sometimes clefs at the start of a measure need to appear after the barline rather than before,
    as for cues or for use after a repeated section.
    The after-barline attribute is set to "yes" in this situation. The attribute is ignored for mid-measure clefs.

    Clefs appear at the start of each system unless the print-object attribute has been set to "no" or
    the additional attribute has been set to "yes"
    """

    class XMLSign(XMLElement, ClefSign):
        def __init__(self, value, *args, **kwargs):
            super().__init__(tag='sign', value=value, *args, **kwargs)

    class XMLLine(XMLElement, StaffLine):
        def __init__(self, value, *args, **kwargs):
            super().__init__(tag='line', value=value, *args, **kwargs)

    _CHILDREN_TYPES = [XMLSign, XMLLine]
    _CHILDREN_ORDERED = True

    def __init__(self, sign, line):
        super().__init__(tag='clef')
        self._sign = None
        self._line = None
        self.sign = sign
        self.line = line

    @property
    def sign(self):
        return self._sign

    @sign.setter
    def sign(self, value):
        self._set_child(self.XMLSign, 'sign', value)

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, value):
        self._set_child(self.XMLLine, 'line', value)


class XMLAttributes(XMLElement):
    """
    The attributes element contains musical information that typically changes on measure boundaries.
    This includes key and time signatures, clefs, transpositions, and staving.
    When attributes are changed mid-measure, it affects the music in score order, not in MusicXML document order.
    <!ELEMENT attributes (%editorial;, divisions?, key*, time*, staves?, part-symbol?, instruments?,
    clef*, staff-details*, transpose*, directive*, measure-style*)>
    """
    _CHILDREN_TYPES = [XMLDivisions, XMLTime, XMLClef]
    _CHILDREN_ORDERED = True

    def __init__(self):
        super().__init__(tag='attributes')
