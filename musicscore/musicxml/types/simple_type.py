import re


class SimpleType(object):
    _PERMITTED = ()

    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if v is not None and v not in self._PERMITTED:
            raise ValueError('{}.value {} must be None or in {} '.format(self.__class__.__name__, v, self._PERMITTED))
        self._value = v
        self._text = v

    def __repr__(self):
        return str(self.value)


# ///////////////

class ExampleType(SimpleType):
    _PERMITTED = ('one', 'two', 'three')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class Decimal(SimpleType):
    """
    Decimal.value can be a float, int or None.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        if v is not None and not isinstance(v, float) and not isinstance(v, int):
            raise TypeError('value {} of {} must a be a float, int or None'.format(v, self.__class__.__name__))
        self._value = v


TypeDecimal = Decimal


class Integer(SimpleType):
    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        if not isinstance(v, int):
            raise TypeError('value {} must be an int not {}'.format(v, type(v).__name__))
        self._value = v


TypeInteger = Integer


class PositiveInteger(SimpleType):
    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        Integer(v)
        if v < 1:
            raise ValueError('value {} must a be positive.'.format(v))

        self._value = v


TypePositiveInteger = PositiveInteger


class NonNegativeInteger(SimpleType):
    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        Integer(v)
        if v < 0:
            raise ValueError('value {} must a be non negative.'.format(v))

        self._value = v


TypeNonNegativeInteger = NonNegativeInteger


class String(SimpleType):
    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        if not isinstance(v, str):
            raise TypeError('value {} must a be string'.format(v))
        self._value = v


TypeString = String


# todo xs:Token
class Token(String):
    """
    Der lexikalische und der Werteraum von xs:token sind die Menge aller Strings nach Whitespace-Ersetzung,
    d.h., nachdem jedes Vorkommen von #x9 (Tab), #xA (Linefeed) und #xD (Carriage Return) durch ein #x20 (Leerzeichen)
    ersetzt und dann Whitespace zusammengefaßt (d.h., unmittelbar aufeinanderfolgende Leerzeichen werden durch ein
    einzelnes ersetzt, und führende oder am Ende stehende Leerzeichen werden entfernt) wurde.

    Einfacher ausgedrückt, ist xs:token der geeignetste Datentyp für Strings, bei denen es nicht auf Whitespace ankommt.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


TypeToken = Token


# todo xs:ID
class ID(String):
    """

    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


# todo xs:IDREF
class IDREF(String):
    """

    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


# todo xs:anyURI
class AnyURI(String):
    """

    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


# ///////////////
# Simple types derived from barline.mod elements

class TypeBackwardForward(SimpleType):
    """The backward-forward type is used to specify repeat directions. The start of the repeat has a forward direction
    while the end of the repeat has a backward direction.
    """
    _PERMITTED = ["backward", "forward"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeBarStyle(SimpleType):
    """The bar-style type represents barline style information. Choices are regular, dotted, dashed, heavy, light-light,
    light-heavy, heavy-light, heavy-heavy, tick (a short stroke through the top line), short (a partial barline between
    the 2nd and 4th lines), and none.
    """
    _PERMITTED = ["regular", "dotted", "dashed", "heavy", "light-light", "light-heavy", "heavy-light", "heavy-heavy",
                  "tick", "short", "none"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeEndingNumber(Token):
    """
    The ending-number type is used to specify either a comma-separated list of positive integers without leading zeros,
    or a string of zero or more spaces. It is used for the number attribute of the ending element. The zero or more
    spaces version is used when software knows that an ending is present, but cannot determine the type of the ending
    """
    pattern = r'([ ]*)|([1-9][0-9]*(, ?[1-9][0-9]*)*)'
    p = re.compile(pattern)

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeRightLeftMiddle(SimpleType):
    """
    The right-left-middle type is used to specify barline location.
    """
    _PERMITTED = ["right", "left", "middle"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeStartStopDiscontinue(SimpleType):
    """
    The start-stop-discontinue type is used to specify ending types. Typically, the start type is associated with the
    left barline of the first measure in an ending. The stop and discontinue types are associated with the right barline
    of the last measure in an ending. Stop is used when the ending mark concludes with a downward jog, as is typical for
    first endings. Discontinue is used when there is no downward jog, as is typical for second endings that do not
    conclude a pieceThe right-left-middle type is used to specify barline location.
    """
    _PERMITTED = ["start", "stop", "discontinue"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeWinged(SimpleType):
    """
    The winged attribute indicates whether the repeat has winged extensions that appear above and below the barline.
    The straight and curved values represent single wings, while the double-straight and double-curved values represent
    double wings. The none value indicates no wings and is the default.
    """
    _PERMITTED = ["none", "straight", "curved", "double-straight", "double-curved"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


# ///////////////
# Simple types derived from common.mod entities and elements

class TypeAboveBelow(SimpleType):
    _PERMITTED = ('above', 'below')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeBeamLevel(PositiveInteger):
    """
    The MusicXML format supports six levels of beaming, up to 1024th notes. Unlike the number-level type, the beam-level
    type identifies concurrent beams in a beam group. It does not distinguish overlapping beams such as grace notes
    within regular notes, or beams used in different voices.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        PositiveInteger(v)
        if v < 1 or v > 8:
            raise ValueError(
                '{}.value {} must be between 1 and 8'.format(self.__class__.__name__, v))
        self._value = v


class TypeColor(Token):
    pattern = r'^#[\dA-F]{6}([\dA-F][\dA-F])?$'
    p = re.compile(pattern)

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        Token(v)
        m = self.p.match(v)
        if m is None:
            raise ValueError(
                '{}.value {} must match the following pattern: {}'.format(self.__class__.__name__,
                                                                          v, self.pattern))
        self._value = v


class TypeCommaSeparatedText(Token):
    pattern = r'^[^,]+(, ?[^,]+)*$'
    p = re.compile(pattern)

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        m = self.p.match(v)
        if m is None:
            raise ValueError(
                '{}.value {} must match the following pattern: {}'.format(self.__class__.__name__,
                                                                          v, self.pattern))
        self._value = v


class TypeDivisions(Integer):
    """
    The divisions type is used to express values in terms of the musical divisions defined by the divisions element.
    It is preferred that these be integer values both for MIDI interoperability and to avoid roundoff errors.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeEnclosureShape(SimpleType):
    """The enclosure-shape type describes the shape and presence / absence of an enclosure around text or symbols. A
    bracket enclosure is similar to a rectangle with the bottom line missing, as is common in jazz notation.
    """
    _PERMITTED = ["rectangle", "square", "oval", "circle", "bracket", "triangle", "diamond", "pentagon", "hexagon",
                  "heptagon", "octagon", "nonagon", "decagon", "none"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeFontWeight(SimpleType):
    _PERMITTED = ('normal', 'bold')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeFontSize(Decimal):

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeFontStyle(SimpleType):
    _PERMITTED = ('normal', 'italic')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeLeftCenterRight(SimpleType):
    """
    The left-center-right type is used to define horizontal alignment and text justification.
    """
    _PERMITTED = ('left', 'center', 'right')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeLineLength(SimpleType):
    """
    The line-length type distinguishes between different line lengths for doit, falloff, plop, and scoop articulations.
    """
    _PERMITTED = ('short', 'medium' 'long')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeLineType(SimpleType):
    """
    The line-type type distinguishes between solid, dashed, dotted, and wavy lines.
    """
    _PERMITTED = ('solid', 'dashed', 'dotted', 'wavy')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeLineShape(SimpleType):
    """
    The line-shape type distinguishes between straight and curved lines.
    """
    _PERMITTED = ('straight', 'curved')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeMidi16(PositiveInteger):
    """
    The midi-16 type is used to express MIDI 1.0 values that range from 1 to 16.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        PositiveInteger(v)
        if v <= 1 or v >= 16:
            raise ValueError(
                '{}.value {} must be between 1 and 16'.format(self.__class__.__name__, v))
        self._value = v


class TypeMidi128(PositiveInteger):
    """
    The midi-128 type is used to express MIDI 1.0 values that range from 1 to 128..
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        PositiveInteger(v)
        if v <= 1 or v >= 128:
            raise ValueError(
                '{}.value {} must be between 1 and 128'.format(self.__class__.__name__, v))
        self._value = v


class TypeMidi16384(PositiveInteger):
    """
    The midi-16384 type is used to express MIDI 1.0 values that range from 1 to 16384..
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        PositiveInteger(v)
        if v <= 1 or v >= 16384:
            raise ValueError(
                '{}.value {} must be between 1 and 16384'.format(self.__class__.__name__, v))
        self._value = v


class TypeMute(SimpleType):
    """
    The mute type represents muting for different instruments, including brass, winds, and strings. The on and off
    values are used for undifferentiated mutes. The remaining values represent specific mutes.

    """

    _PERMITTED = ["on", "off", "straight", "cup", "harmon-no-stem", "harmon-stem", "bucket", "plunger", "hat",
                  "solotone", "practice", "stop-mute", "stop-hand", "echo", "palm"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeNonNegativeDecimal(SimpleType):
    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        if not isinstance(v, float) and not isinstance(v, int):
            raise TypeError('value {} must a be a non negative float or int not {}'.format(v, type(v).__name__))
        if v < 0:
            raise ValueError('value {} must be non negative'.format(v))
        self._value = v


class TypeNumberLevel(PositiveInteger):
    """
    Slurs, tuplets, and many other features can be concurrent and overlapping within a single musical part. The
    number-level type distinguishes up to six concurrent objects of the same type. A reading program should be prepared
    to handle cases where the number-levels stop in an arbitrary order. Different numbers are needed when the features
    overlap in MusicXML document order. When a number-level value is optional, the value is 1 by default
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        if v < 1 or v > 6:
            raise ValueError(
                '{}.value {} must be between 1 and 6'.format(self.__class__.__name__, v))
        self._value = v


class TypeNumberOfLines(Integer):
    """
    The number-of-lines type is used to specify the number of lines in text decoration attributes.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        if v < 0 or v > 3:
            raise ValueError(
                '{}.value {} must be between 0 and 3'.format(self.__class__.__name__, v))
        self._value = v


class TypeNumberOrNormal(SimpleType):
    """
    The number-or-normal values can be either a decimal number or the string "normal". This is used by the line-height
    and letter-spacing attributes.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        if v is not 'normal':
            try:
                Decimal(v)
            except TypeError:
                raise ValueError(
                    '{}.value {} can be either a decimal number or the string "normal"'.format(self.__class__.__name__,
                                                                                               v))
        self._value = v


class OverUnder(SimpleType):
    _PERMITTED = ['over', 'under']

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypePercent(Decimal):
    """
    The percent type specifies a percentage from 0 to 100.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        if v > 100 or v < 0:
            raise ValueError(
                '{}.value {} must be a percentage from 0 to 100'.format(self.__class__.__name__, v))
        self._value = v


class TypePositiveDivisions(PositiveInteger):
    """
    The positive-divisions type restricts divisions values to positive numbers.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypePositiveDecimal(SimpleType):
    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        if not isinstance(v, float) and not isinstance(v, int):
            raise TypeError('value {} must a be a positive float or int'.format(v))
        if v <= 0:
            raise ValueError('value {} must be positive'.format(v))
        self._value = v


class TypeRotationDegrees(Decimal):
    """
    The rotation-degrees type specifies rotation, pan, and elevation values in degrees. Values range from -180 to 180.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        if v < -180 or v > 180:
            raise ValueError(
                '{}.value {} must be between -180 and 180'.format(self.__class__.__name__, v))
        self._value = v


class TypeSemiPitched(SimpleType):
    _PERMITTED = ["high", "medium-high", "medium", "medium-low", "low", "very-low"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeSmulfGlyphName(Token):
    """
    The smufl-glyph-name type is used for attributes that reference a specific Standard Music Font Layout (SMuFL)
    character. The value is a SMuFL canonical glyph name, not a code point. For instance, the value for a standard piano
    pedal mark would be keyboardPedalPed, not U+E650.
    <xs:restriction base="xs:NMTOKEN"/>
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)
        raise NotImplementedError()


class TypeSmuflCodaGlyphNameType(TypeSmulfGlyphName):
    """
    The smufl-coda-glyph-name type is used to reference a specific Standard Music Font Layout (SMuFL) coda character.
    The value is a SMuFL canonical glyph name that starts with coda.
    """

    # pattern = r"coda\c*"
    # p = re.compile(pattern)

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)
        NotImplementedError()

    # @SimpleType.value.setter
    # def value(self, v):
    #     Token(v)
    #     m = self.p.match(v)
    #     if m is None:
    #         raise ValueError(
    #             '{}.value {} must match the following pattern: {}'.format(self.__class__.__name__,
    #                                                                       v, self.pattern))
    #     self._value = v


class TypeTypeSmulfSegnoGlyphName(TypeSmulfGlyphName):
    """
    The smufl-segno-glyph-name type is used to reference a specific Standard Music Font Layout (SMuFL) segno character.
    The value is a SMuFL canonical glyph name that starts with segno.
    """

    # pattern = r'^segno\c*'
    # p = re.compile(pattern)

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)
        NotImplementedError()

    # @SimpleType.value.setter
    # def value(self, v):
    #     Token(v)
    #     m = self.p.match(v)
    #     if m is None:
    #         raise ValueError(
    #             '{}.value {} must match the following pattern: {}'.format(self.__class__.__name__,
    #                                                                       v, self.pattern))
    #     self._value = v


class TypeSmulfAccidentalGlyphName(TypeSmulfGlyphName):
    """
    The smufl-accidental-glyph-name type is used to reference a specific Standard Music Font Layout (SMuFL) accidental
    character. The value is a SMuFL canonical glyph name that starts with acc.
	<xs:restriction base="smufl-glyph-name">
		<xs:pattern value="acc\c+"/>
	</xs:restriction>
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)
        raise NotImplementedError()


class TypeSmulfLyricsGlyphName(TypeSmulfGlyphName):
    """
    The smufl-lyrics-glyph-name type is used to reference a specific Standard Music Font Layout (SMuFL) lyrics elision
    character. The value is a SMuFL canonical glyph name that starts with lyrics.
    <xs:restriction base="smufl-glyph-name">
        <xs:pattern value="lyrics\c+"/>
    </xs:restriction>
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)
        raise NotImplementedError()


class TypeStartStop(SimpleType):
    """
    The start-stop type is used for an attribute of musical elements that can either start or stop, such as tuplets.
    The values of start and stop refer to how an element appears in musical score order, not in MusicXML document order.
    An element with a stop attribute may precede the corresponding element with a start attribute within a MusicXML
    document. This is particularly common in multi-staff music. For example, the stopping point for a tuplet may appear
    in staff 1 before the starting point for the tuplet appears in staff 2 later in the document
    """
    _PERMITTED = ["start", "stop"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeStartStopContinue(SimpleType):
    """
    The start-stop-continue type is used for an attribute of musical elements that can either start or stop, but also
    need to refer to an intermediate point in the symbol, as for complex slurs or for formatting of symbols across
    system breaks.

    The values of start, stop, and continue refer to how an element appears in musical score order, not in MusicXML
    document order. An element with a stop attribute may precede the corresponding element with a start attribute within
    a MusicXML document. This is particularly common in multi-staff music. For example, the stopping point for a slur
    may appear in staff 1 before the starting point for the slur appears in staff 2 later in the document.
    """
    _PERMITTED = ["start", "stop", "continue"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeSymbolSize(SimpleType):
    """
    The symbol-size type is used to distinguish between full, cue sized, grace cue sized, and oversized symbols.
    """
    _PERMITTED = ["full", "cue", "grace-cue", "large"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeTenths(Decimal):
    """
    The tenths type is a number representing tenths of interline staff space (positive or negative).
    Both integer and decimal values are allowed, such as 5 for a half space and 2.5 for a quarter space.
    Interline space is measured from the middle of a staff line.
    Distances in a MusicXML file are measured in tenths of staff space.
    Tenths are then scaled to millimeters within the scaling element, used in the defaults element at the start of
    a musicxml. Individual staves can apply a scaling factor to adjust staff size.
    When a MusicXML element or attribute refers to tenths, it means the global tenths defined by the scaling element,
    not the local tenths as adjusted by the staff-size element.
    Tenths allows the value None.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeTextDirection(SimpleType):
    """The text-direction type is used to adjust and override the Unicode bidirectional text algorithm,
    similar to the W3C Internationalization Tag Set recommendation. Values are ltr (left-to-right embed), rtl (right-to-
    left embed), lro (left-to-right bidi-override), and rlo (right-to-left bidi-override). The default value is ltr.
    This type is typically used by applications that store text in left-to-right visual order rather than logical order.
    Such applications can use the lro value to better communicate with other applications that more fully support
    bidirectional text.
    """

    _PERMITTED = ["ltr", "rtl", "lro", "rlo"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeTiedType(SimpleType):
    """
	The tied-type type is used as an attribute of the tied element to specify where the visual representation of a tie
	begins and ends. A tied element which joins two notes of the same pitch can be specified with tied-type start on the
	first note and tied-type stop on the second note. To indicate a note should be undamped, use a single tied element
	with tied-type let-ring. For other ties that are visually attached to a single note, such as a tie leading into or
	out of a repeated section or coda, use two tied elements on the same note, one start and one stop.

	In start-stop cases, ties can add more elements using a continue type. This is typically used to specify the
	formatting of cross-system ties.
    """
    _PERMITTED = ["start", "stop", "continue", "let-ring"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeTimeOnly(Token):
    """
    The time-only type is used to indicate that a particular playback-related element only applies particular times
    through a repeated section. The value is a comma-separated list of positive integers arranged in ascending order,
    indicating which times through the repeated section that the element applies.
    """
    pattern = r'[1-9][0-9]*(, ?[1-9][0-9]*)*'
    p = re.compile(pattern)

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        m = self.p.match(v)
        if m is None:
            raise ValueError(
                '{}.value {} must match the following pattern: {}'.format(self.__class__.__name__,
                                                                          v, self.pattern))
        self._value = v


class TypeUpDown(SimpleType):
    """
    The up-down type is used for the direction of arrows and other pointed symbols like vertical accents, indicating
    which way the tip is pointing.
    """

    _PERMITTED = ["up", "down"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeValign(SimpleType):
    """
    The valign type is used to indicate vertical alignment to the top, middle, bottom, or baseline of the text.
    Defaults are implementation-dependent.
    """

    _PERMITTED = ["top", "middle", "bottom", "baseline"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeValignImage(SimpleType):
    """
    The valign-image type is used to indicate vertical alignment for images and graphics, so it does not include a
    baseline value. Defaults are implementation-dependent.
    """

    _PERMITTED = ["top", "middle", "bottom"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeYesNo(SimpleType):
    _PERMITTED = ('yes', 'no')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeYesNoNumber(SimpleType):
    """
    The yes-no-number type is used for attributes that can be either boolean or numeric values.
    """
    _PERMITTED = ('yes', 'no')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        if v is not None and v not in self._PERMITTED and not Decimal(v):
            raise ValueError(
                '{}.value {} must be yes no or decimal')
        self._value = v


class TypePositiveIntegerOrEmpty(SimpleType):
    """
    The positive-integer-or-empty values can be either a positive integer or an empty string.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        if v is not None and not TypePositiveInteger(v) and v != '':
            raise ValueError(
                '{}.value {}  can be either a positive integer or an empty string')
        self._value = v


class TypeTrillBeats(SimpleType):
    """
    The trill-beats type specifies the beats used in a trill-sound or bend-sound attribute group. It is a decimal value
    with a minimum value of 2.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        if v is not None:
            if not TypeDecimal(v):
                raise TypeError('{}.value {} must be of type Decimal not {}.'.format(self.__class__, v, v.__class__))
        if v < 2:
            raise ValueError('{}.value {} must be greater than or equal to 2.'.format(self.__class__, v))
        self._value = v


class TypeStartNote(SimpleType):
    """
    The start-note type describes the starting note of trills and mordents for playback, relative to the current note.
    """

    _PERMITTED = ["upper", "main", "below"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeTrillStep(SimpleType):
    """
    The trill-step type describes the alternating note of trills and mordents for playback, relative to the current note.
    """

    _PERMITTED = ["whole", "half", "unison"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeTwoNoteTurn(SimpleType):
    """
    The two-note-turn type describes the ending notes of trills and mordents for playback, relative to the current note.
    """

    _PERMITTED = ["whole", "half", "none"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeTremoloType(SimpleType):
    """
    The tremolo-type is used to distinguish multi-note, single-note, and unmeasured tremolos.
    """

    _PERMITTED = ["start", "stop", "single", "unmeasured"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeFermataShape(SimpleType):
    """
    The fermata-shape type represents the shape of the fermata sign. The empty value is equivalent to the normal value.
    """
    _PERMITTED = ["normal", "angled", "square", "double-angled", "double-square", "double-dot", "half-curve", "curlew",
                  ""]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeUprightInverted(SimpleType):
    """
    The upright-inverted type describes the appearance of a fermata element. The value is upright if not specified.
    """
    _PERMITTED = ["upright", "inverted"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


''''
	<!-- Simple types derived from common.mod entities and elements -->


	<xs:simpleType name="css-font-size">
		<xs:annotation>
			<xs:documentation>The css-font-size type includes the CSS font sizes used as an alternative to a numeric point size.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:token">
			<xs:enumeration value="xx-small"/>
			<xs:enumeration value="x-small"/>
			<xs:enumeration value="small"/>
			<xs:enumeration value="medium"/>
			<xs:enumeration value="large"/>
			<xs:enumeration value="x-large"/>
			<xs:enumeration value="xx-large"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="left-right">
		<xs:annotation>
			<xs:documentation>The left-right type is used to indicate whether one element appears to the left or the right of another element.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:token">
			<xs:enumeration value="left"/>
			<xs:enumeration value="right"/>
		</xs:restriction>
	</xs:simpleType>


	<xs:simpleType name="smufl-coda-glyph-name">
		<xs:annotation>
			<xs:documentation>The smufl-coda-glyph-name type is used to reference a specific Standard Music Font Layout (SMuFL) coda character. The value is a SMuFL canonical glyph name that starts with coda.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="smufl-glyph-name">
			<xs:pattern value="coda\c*"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="smufl-pictogram-glyph-name">
		<xs:annotation>
			<xs:documentation>The smufl-pictogram-glyph-name type is used to reference a specific Standard Music Font Layout (SMuFL) percussion pictogram character. The value is a SMuFL canonical glyph name that starts with pict.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="smufl-glyph-name">
			<xs:pattern value="pict\c+"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="smufl-segno-glyph-name">
		<xs:annotation>
			<xs:documentation>The smufl-segno-glyph-name type is used to reference a specific Standard Music Font Layout (SMuFL) segno character. The value is a SMuFL canonical glyph name that starts with segno.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="smufl-glyph-name">
			<xs:pattern value="segno\c*"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="start-stop-single">
		<xs:annotation>
			<xs:documentation>The start-stop-single type is used for an attribute of musical elements that can be used for either multi-note or single-note musical elements, as for groupings.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:token">
			<xs:enumeration value="start"/>
			<xs:enumeration value="stop"/>
			<xs:enumeration value="single"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="string-number">
		<xs:annotation>
			<xs:documentation>The string-number type indicates a string number. Strings are numbered from high to low, with 1 being the highest pitched full-length string.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:positiveInteger"/>
	</xs:simpleType>

	<xs:simpleType name="top-bottom">
		<xs:annotation>
			<xs:documentation>The top-bottom type is used to indicate the top or bottom part of a vertical shape like non-arpeggiate.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:token">
			<xs:enumeration value="top"/>
			<xs:enumeration value="bottom"/>
		</xs:restriction>
	</xs:simpleType>


	<xs:simpleType name="yyyy-mm-dd">
		<xs:annotation>
			<xs:documentation>Calendar dates are represented yyyy-mm-dd format, following ISO 8601. This is a W3C XML Schema date type, but without the optional timezone data.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:date">
			<xs:pattern value="[^:Z]*"/>
		</xs:restriction>
	</xs:simpleType>
'''


# ///////////////
# Simple types derived from attributes.mod entities and elements

class TypeCancelLocation(SimpleType):
    """
    The cancel-location type is used to indicate where a key signature cancellation appears relative to a new key
    signature: to the left, to the right, or before the barline and to the left. It is left by default. For mid-measure
    key elements, a cancel-location of before-barline should be treated like a cancel-location of left.
    """
    _PERMITTED = ['left', 'right', 'before-barline']

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeClefSign(SimpleType):
    """
    The clef-sign element represents the different clef symbols.

    The jianpu sign indicates that the music that follows should be in jianpu numbered notation, just as the TAB sign
    indicates that the music that follows should be in tablature notation.

    Unlike TAB, a jianpu sign does not correspond to a visual clef notation.
    """
    _PERMITTED = ('G', 'F', 'C', 'percussion', 'TAB', 'jianpu', 'none')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeFifths(Integer):
    """
    The fifths type represents the number of flats or sharps in a traditional key signature. Negative numbers are used
    for flats and positive numbers for sharps, reflecting the key's placement within the circle of fifths
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeMillimeters(Decimal):
    """The millimeters type is a number representing millimeters. This is used in the scaling element to provide a
    default scaling from tenths to physical units."""

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeMode(SimpleType):
    """
    The mode type is used to specify major/minor and other mode distinctions. Valid mode values include major, minor,
    dorian, phrygian, lydian, mixolydian, aeolian, ionian, locrian, and none
    """
    _PERMITTED = ['major', 'minor', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'ionian', 'locrian',
                  'none']

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeStaffLine(PositiveInteger):
    """
    The staff-line type indicates the line on a given staff.
    Staff lines are numbered from bottom to top, with 1 being the bottom line on a staff.
    Staff line values can be used to specify positions outside the staff,
    such as a C clef positioned in the middle of a grand staff.
    Standard values are 2 for the G sign (treble clef), 4 for the F sign (bass clef),
    3 for the C sign (alto clef) and 5 for TAB (on a 6-line staff).
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeStaffNumber(PositiveInteger):
    """
    The staff-number type indicates staff numbers within a multi-staff part. Staves are numbered from top to bottom,
    with 1 being the top staff on a part.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


'''
```DTD
	<!-- Simple types derived from attributes.mod entities and elements -->

	<xs:simpleType name="show-frets">
		<xs:annotation>
			<xs:documentation>The show-frets type indicates whether to show tablature frets as numbers (0, 1, 2) or letters (a, b, c). The default choice is numbers.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:token">
			<xs:enumeration value="numbers"/>
			<xs:enumeration value="letters"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="staff-type">
		<xs:annotation>
			<xs:documentation>The staff-type value can be ossia, cue, editorial, regular, or alternate. An alternate staff indicates one that shares the same musical data as the prior staff, but displayed differently (e.g., treble and bass clef, standard notation and tab).</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="ossia"/>
			<xs:enumeration value="cue"/>
			<xs:enumeration value="editorial"/>
			<xs:enumeration value="regular"/>
			<xs:enumeration value="alternate"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="time-relation">
		<xs:annotation>
			<xs:documentation>The time-relation type indicates the symbol used to represent the interchangeable aspect of dual time signatures.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="parentheses"/>
			<xs:enumeration value="bracket"/>
			<xs:enumeration value="equals"/>
			<xs:enumeration value="slash"/>
			<xs:enumeration value="space"/>
			<xs:enumeration value="hyphen"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="time-separator">
		<xs:annotation>
			<xs:documentation>The time-separator type indicates how to display the arrangement between the beats and beat-type values in a time signature. The default value is none. The horizontal, diagonal, and vertical values represent horizontal, diagonal lower-left to upper-right, and vertical lines respectively. For these values, the beats and beat-type values are arranged on either side of the separator line. The none value represents no separator with the beats and beat-type arranged vertically. The adjacent value represents no separator with the beats and beat-type arranged horizontally.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:token">
			<xs:enumeration value="none"/>
			<xs:enumeration value="horizontal"/>
			<xs:enumeration value="diagonal"/>
			<xs:enumeration value="vertical"/>
			<xs:enumeration value="adjacent"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="time-symbol">
		<xs:annotation>
			<xs:documentation>The time-symbol type indicates how to display a time signature. The normal value is the usual fractional display, and is the implied symbol type if none is specified. Other options are the common and cut time symbols, as well as a single number with an implied denominator. The note symbol indicates that the beat-type should be represented with the corresponding downstem note rather than a number. The dotted-note symbol indicates that the beat-type should be represented with a dotted downstem note that corresponds to three times the beat-type value, and a numerator that is one third the beats value.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:token">
			<xs:enumeration value="common"/>
			<xs:enumeration value="cut"/>
			<xs:enumeration value="single-number"/>
			<xs:enumeration value="note"/>
			<xs:enumeration value="dotted-note"/>
			<xs:enumeration value="normal"/>
		</xs:restriction>
	</xs:simpleType>

'''


# ///////////////
# Simple types derived from direction.mod elements

class TypeMarginType(SimpleType):
    """
    The margin-type type specifies whether margins apply to even page, odd pages, or both.
    """
    _PERMITTED = ('odd', 'even', 'both')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeWedgeType(SimpleType):
    """
    The wedge type is crescendo for the start of a wedge that is closed at the left side, diminuendo for the start of
    a wedge that is closed on the right side, and stop for the end of a wedge. The continue type is used for formatting
    wedges over a system break, or for other situations where a single wedge is divided into multiple segments.
    """
    _PERMITTED = ('crescendo', 'diminuendo', 'stop', 'continue')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeLineEnd(SimpleType):
    """
    The line-end type specifies if there is a jog up or down (or both), an arrow, or nothing at the start or end of a
    bracket.
    """
    _PERMITTED = ('up', 'down', 'both', 'arrow', 'none')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeLineWidthType(Token):
    """
    The line-width-type defines what type of line is being defined in a line-width element. Values include beam,
    bracket, dashes, enclosure, ending, extend, heavy barline, leger, light barline, octave shift, pedal, slur middle,
    slur tip, staff, stem, tie middle, tie tip, tuplet bracket, and wedge. This is left as a string so that other
    application-specific types can be defined, but it is made a separate type so that it can be redefined more strictly.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


'''
<!-- Simple types derived from direction.mod elements -->

   <xs:simpleType name="accordion-middle">
		<xs:annotation>
			<xs:documentation>The accordion-middle type may have values of 1, 2, or 3, corresponding to having 1 to 3 dots in the middle section of the accordion registration symbol. This type is not used if no dots are present.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:positiveInteger">
			<xs:minInclusive value="1"/>
			<xs:maxInclusive value="3"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="beater-value">
		<xs:annotation>
			<xs:documentation>The beater-value type represents pictograms for beaters, mallets, and sticks that do not have different materials represented in the pictogram. The finger and hammer values are in addition to Stone's list.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="bow"/>
			<xs:enumeration value="chime hammer"/>
			<xs:enumeration value="coin"/>
			<xs:enumeration value="drum stick"/>
			<xs:enumeration value="finger"/>
			<xs:enumeration value="fingernail"/>
			<xs:enumeration value="fist"/>
			<xs:enumeration value="guiro scraper"/>
			<xs:enumeration value="hammer"/>
			<xs:enumeration value="hand"/>
			<xs:enumeration value="jazz stick"/>
			<xs:enumeration value="knitting needle"/>
			<xs:enumeration value="metal hammer"/>
			<xs:enumeration value="slide brush on gong"/>
			<xs:enumeration value="snare stick"/>
			<xs:enumeration value="spoon mallet"/>
			<xs:enumeration value="superball"/>
			<xs:enumeration value="triangle beater"/>
			<xs:enumeration value="triangle beater plain"/>
			<xs:enumeration value="wire brush"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="degree-symbol-value">
		<xs:annotation>
			<xs:documentation>The degree-symbol-value type indicates indicates that a symbol should be used in specifying the degree.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:token">
			<xs:enumeration value="major"/>
			<xs:enumeration value="minor"/>
			<xs:enumeration value="augmented"/>
			<xs:enumeration value="diminished"/>
			<xs:enumeration value="half-diminished"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="degree-type-value">
		<xs:annotation>
			<xs:documentation>The degree-type-value type indicates whether the current degree element is an addition, alteration, or subtraction to the kind of the current chord in the harmony element.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="add"/>
			<xs:enumeration value="alter"/>
			<xs:enumeration value="subtract"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="effect">
		<xs:annotation>
			<xs:documentation>The effect type represents pictograms for sound effect percussion instruments. The cannon, lotus flute, and megaphone values are in addition to Stone's list.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="anvil"/>
			<xs:enumeration value="auto horn"/>
			<xs:enumeration value="bird whistle"/>
			<xs:enumeration value="cannon"/>
			<xs:enumeration value="duck call"/>
			<xs:enumeration value="gun shot"/>
			<xs:enumeration value="klaxon horn"/>
			<xs:enumeration value="lions roar"/>
			<xs:enumeration value="lotus flute"/>
			<xs:enumeration value="megaphone"/>
			<xs:enumeration value="police whistle"/>
			<xs:enumeration value="siren"/>
			<xs:enumeration value="slide whistle"/>
			<xs:enumeration value="thunder sheet"/>
			<xs:enumeration value="wind machine"/>
			<xs:enumeration value="wind whistle"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="glass-value">
		<xs:annotation>
			<xs:documentation>The glass-value type represents pictograms for glass percussion instruments.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="glass harmonica"/>
			<xs:enumeration value="glass harp"/>
			<xs:enumeration value="wind chimes"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="harmony-type">
		<xs:annotation>
			<xs:documentation>The harmony-type type differentiates different types of harmonies when alternate harmonies are possible. Explicit harmonies have all note present in the music; implied have some notes missing but implied; alternate represents alternate analyses.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:token">
			<xs:enumeration value="explicit"/>
			<xs:enumeration value="implied"/>
			<xs:enumeration value="alternate"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="kind-value">
		<xs:annotation>
			<xs:documentation>A kind-value indicates the type of chord. Degree elements can then add, subtract, or alter from these starting points. Values include:

Triads:
	major (major third, perfect fifth)
	minor (minor third, perfect fifth)
	augmented (major third, augmented fifth)
	diminished (minor third, diminished fifth)
Sevenths:
	dominant (major triad, minor seventh)
	major-seventh (major triad, major seventh)
	minor-seventh (minor triad, minor seventh)
	diminished-seventh (diminished triad, diminished seventh)
	augmented-seventh (augmented triad, minor seventh)
	half-diminished (diminished triad, minor seventh)
	major-minor (minor triad, major seventh)
Sixths:
	major-sixth (major triad, added sixth)
	minor-sixth (minor triad, added sixth)
Ninths:
	dominant-ninth (dominant-seventh, major ninth)
	major-ninth (major-seventh, major ninth)
	minor-ninth (minor-seventh, major ninth)
11ths (usually as the basis for alteration):
	dominant-11th (dominant-ninth, perfect 11th)
	major-11th (major-ninth, perfect 11th)
	minor-11th (minor-ninth, perfect 11th)
13ths (usually as the basis for alteration):
	dominant-13th (dominant-11th, major 13th)
	major-13th (major-11th, major 13th)
	minor-13th (minor-11th, major 13th)
Suspended:
	suspended-second (major second, perfect fifth)
	suspended-fourth (perfect fourth, perfect fifth)
Functional sixths:
	Neapolitan
	Italian
	French
	German
Other:
	pedal (pedal-point bass)
	power (perfect fifth)
	Tristan

The "other" kind is used when the harmony is entirely composed of add elements. The "none" kind is used to explicitly encode absence of chords or functional harmony.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="major"/>
			<xs:enumeration value="minor"/>
			<xs:enumeration value="augmented"/>
			<xs:enumeration value="diminished"/>
			<xs:enumeration value="dominant"/>
			<xs:enumeration value="major-seventh"/>
			<xs:enumeration value="minor-seventh"/>
			<xs:enumeration value="diminished-seventh"/>
			<xs:enumeration value="augmented-seventh"/>
			<xs:enumeration value="half-diminished"/>
			<xs:enumeration value="major-minor"/>
			<xs:enumeration value="major-sixth"/>
			<xs:enumeration value="minor-sixth"/>
			<xs:enumeration value="dominant-ninth"/>
			<xs:enumeration value="major-ninth"/>
			<xs:enumeration value="minor-ninth"/>
			<xs:enumeration value="dominant-11th"/>
			<xs:enumeration value="major-11th"/>
			<xs:enumeration value="minor-11th"/>
			<xs:enumeration value="dominant-13th"/>
			<xs:enumeration value="major-13th"/>
			<xs:enumeration value="minor-13th"/>
			<xs:enumeration value="suspended-second"/>
			<xs:enumeration value="suspended-fourth"/>
			<xs:enumeration value="Neapolitan"/>
			<xs:enumeration value="Italian"/>
			<xs:enumeration value="French"/>
			<xs:enumeration value="German"/>
			<xs:enumeration value="pedal"/>
			<xs:enumeration value="power"/>
			<xs:enumeration value="Tristan"/>
			<xs:enumeration value="other"/>
			<xs:enumeration value="none"/>
		</xs:restriction>
	</xs:simpleType>



	<xs:simpleType name="measure-numbering-value">
		<xs:annotation>
			<xs:documentation>The measure-numbering-value type describes how measure numbers are displayed on this part: no numbers, numbers every measure, or numbers every system.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="none"/>
			<xs:enumeration value="measure"/>
			<xs:enumeration value="system"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="membrane">
		<xs:annotation>
			<xs:documentation>The membrane type represents pictograms for membrane percussion instruments.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="bass drum"/>
			<xs:enumeration value="bass drum on side"/>
			<xs:enumeration value="bongos"/>
			<xs:enumeration value="Chinese tomtom"/>
			<xs:enumeration value="conga drum"/>
			<xs:enumeration value="cuica"/>
			<xs:enumeration value="goblet drum"/>
			<xs:enumeration value="Indo-American tomtom"/>
			<xs:enumeration value="Japanese tomtom"/>
			<xs:enumeration value="military drum"/>
			<xs:enumeration value="snare drum"/>
			<xs:enumeration value="snare drum snares off"/>
			<xs:enumeration value="tabla"/>
			<xs:enumeration value="tambourine"/>
			<xs:enumeration value="tenor drum"/>
			<xs:enumeration value="timbales"/>
			<xs:enumeration value="tomtom"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="metal">
		<xs:annotation>
			<xs:documentation>The metal type represents pictograms for metal percussion instruments. The hi-hat value refers to a pictogram like Stone's high-hat cymbals but without the long vertical line at the bottom.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="agogo"/>
			<xs:enumeration value="almglocken"/>
			<xs:enumeration value="bell"/>
			<xs:enumeration value="bell plate"/>
			<xs:enumeration value="bell tree"/>
			<xs:enumeration value="brake drum"/>
			<xs:enumeration value="cencerro"/>
			<xs:enumeration value="chain rattle"/>
			<xs:enumeration value="Chinese cymbal"/>
			<xs:enumeration value="cowbell"/>
			<xs:enumeration value="crash cymbals"/>
			<xs:enumeration value="crotale"/>
			<xs:enumeration value="cymbal tongs"/>
			<xs:enumeration value="domed gong"/>
			<xs:enumeration value="finger cymbals"/>
			<xs:enumeration value="flexatone"/>
			<xs:enumeration value="gong"/>
			<xs:enumeration value="hi-hat"/>
			<xs:enumeration value="high-hat cymbals"/>
			<xs:enumeration value="handbell"/>
			<xs:enumeration value="jaw harp"/>
			<xs:enumeration value="jingle bells"/>
			<xs:enumeration value="musical saw"/>
			<xs:enumeration value="shell bells"/>
			<xs:enumeration value="sistrum"/>
			<xs:enumeration value="sizzle cymbal"/>
			<xs:enumeration value="sleigh bells"/>
			<xs:enumeration value="suspended cymbal"/>
			<xs:enumeration value="tam tam"/>
			<xs:enumeration value="tam tam with beater"/>
			<xs:enumeration value="triangle"/>
			<xs:enumeration value="Vietnamese hat"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="on-off">
		<xs:annotation>
			<xs:documentation>The on-off type is used for notation elements such as string mutes.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:token">
			<xs:enumeration value="on"/>
			<xs:enumeration value="off"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="pedal-type">
		<xs:annotation>
			<xs:documentation>The pedal-type simple type is used to distinguish types of pedal directions. The start value indicates the start of a damper pedal, while the sostenuto value indicates the start of a sostenuto pedal. The change, continue, and stop values can be used with either the damper or sostenuto pedal. The soft pedal is not included here because there is no special symbol or graphic used for it beyond what can be specified with words and bracket elements.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:token">
			<xs:enumeration value="start"/>
			<xs:enumeration value="stop"/>
			<xs:enumeration value="sostenuto"/>
			<xs:enumeration value="change"/>
			<xs:enumeration value="continue"/>
		</xs:restriction>
	</xs:simpleType>
	
	<xs:simpleType name="pitched-value">
		<xs:annotation>
			<xs:documentation>The pitched-value type represents pictograms for pitched percussion instruments. The chimes and tubular chimes values distinguish the single-line and double-line versions of the pictogram.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="celesta"/>
			<xs:enumeration value="chimes"/>
			<xs:enumeration value="glockenspiel"/>
			<xs:enumeration value="lithophone"/>
			<xs:enumeration value="mallet"/>
			<xs:enumeration value="marimba"/>
			<xs:enumeration value="steel drums"/>
			<xs:enumeration value="tubaphone"/>
			<xs:enumeration value="tubular chimes"/>
			<xs:enumeration value="vibraphone"/>
			<xs:enumeration value="xylophone"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="principal-voice-symbol">
		<xs:annotation>
			<xs:documentation>The principal-voice-symbol type represents the type of symbol used to indicate the start of a principal or secondary voice. The "plain" value represents a plain square bracket. The value of "none" is used for analysis markup when the principal-voice element does not have a corresponding appearance in the score.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="Hauptstimme"/>
			<xs:enumeration value="Nebenstimme"/>
			<xs:enumeration value="plain"/>
			<xs:enumeration value="none"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="staff-divide-symbol">
		<xs:annotation>
			<xs:documentation>The staff-divide-symbol type is used for staff division symbols. The down, up, and up-down values correspond to SMuFL code points U+E00B, U+E00C, and U+E00D respectively.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:token">
			<xs:enumeration value="down"/>
			<xs:enumeration value="up"/>
			<xs:enumeration value="up-down"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="start-stop-change-continue">
		<xs:annotation>
			<xs:documentation>The start-stop-change-continue type is used to distinguish types of pedal directions.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:token">
			<xs:enumeration value="start"/>
			<xs:enumeration value="stop"/>
			<xs:enumeration value="change"/>
			<xs:enumeration value="continue"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="tip-direction">
		<xs:annotation>
			<xs:documentation>The tip-direction type represents the direction in which the tip of a stick or beater points, using Unicode arrow terminology.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="up"/>
			<xs:enumeration value="down"/>
			<xs:enumeration value="left"/>
			<xs:enumeration value="right"/>
			<xs:enumeration value="northwest"/>
			<xs:enumeration value="northeast"/>
			<xs:enumeration value="southeast"/>
			<xs:enumeration value="southwest"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="stick-location">
		<xs:annotation>
			<xs:documentation>The stick-location type represents pictograms for the location of sticks, beaters, or mallets on cymbals, gongs, drums, and other instruments.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="center"/>
			<xs:enumeration value="rim"/>
			<xs:enumeration value="cymbal bell"/>
			<xs:enumeration value="cymbal edge"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="stick-material">
		<xs:annotation>
			<xs:documentation>The stick-material type represents the material being displayed in a stick pictogram.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="soft"/>
			<xs:enumeration value="medium"/>
			<xs:enumeration value="hard"/>
			<xs:enumeration value="shaded"/>
			<xs:enumeration value="x"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="stick-type">
		<xs:annotation>
			<xs:documentation>The stick-type type represents the shape of pictograms where the material
	in the stick, mallet, or beater is represented in the pictogram.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="bass drum"/>
			<xs:enumeration value="double bass drum"/>
			<xs:enumeration value="glockenspiel"/>
			<xs:enumeration value="gum"/>
			<xs:enumeration value="hammer"/>
			<xs:enumeration value="superball"/>
			<xs:enumeration value="timpani"/>
			<xs:enumeration value="wound"/>
			<xs:enumeration value="xylophone"/>
			<xs:enumeration value="yarn"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="up-down-stop-continue">
		<xs:annotation>
			<xs:documentation>The up-down-stop-continue type is used for octave-shift elements, indicating the direction of the shift from their true pitched values because of printing difficulty.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:token">
			<xs:enumeration value="up"/>
			<xs:enumeration value="down"/>
			<xs:enumeration value="stop"/>
			<xs:enumeration value="continue"/>
		</xs:restriction>
	</xs:simpleType>



	<xs:simpleType name="wood">
		<xs:annotation>
			<xs:documentation>The wood type represents pictograms for wood percussion instruments. The maraca and maracas values distinguish the one- and two-maraca versions of the pictogram.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="bamboo scraper"/>
			<xs:enumeration value="board clapper"/>
			<xs:enumeration value="cabasa"/>
			<xs:enumeration value="castanets"/>
			<xs:enumeration value="castanets with handle"/>
			<xs:enumeration value="claves"/>
			<xs:enumeration value="football rattle"/>
			<xs:enumeration value="guiro"/>
			<xs:enumeration value="log drum"/>
			<xs:enumeration value="maraca"/>
			<xs:enumeration value="maracas"/>
			<xs:enumeration value="quijada"/>
			<xs:enumeration value="rainstick"/>
			<xs:enumeration value="ratchet"/>
			<xs:enumeration value="reco-reco"/>
			<xs:enumeration value="sandpaper blocks"/>
			<xs:enumeration value="slit drum"/>
			<xs:enumeration value="temple block"/>
			<xs:enumeration value="vibraslap"/>
			<xs:enumeration value="whip"/>
			<xs:enumeration value="wood block"/>
		</xs:restriction>
	</xs:simpleType>

	<!-- Simple types derived from layout.mod elements -->

	<xs:simpleType name="distance-type">
		<xs:annotation>
			<xs:documentation>The distance-type defines what type of distance is being defined in a distance element. Values include beam and hyphen. This is left as a string so that other application-specific types can be defined, but it is made a separate type so that it can be redefined more strictly.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:token"/>
	</xs:simpleType>

	<xs:simpleType name="glyph-type">
		<xs:annotation>
			<xs:documentation>The glyph-type defines what type of glyph is being defined in a glyph element. Values include quarter-rest, g-clef-ottava-bassa, c-clef, f-clef, percussion-clef, octave-shift-up-8, octave-shift-down-8, octave-shift-continue-8, octave-shift-down-15, octave-shift-up-15, octave-shift-continue-15, octave-shift-down-22, octave-shift-up-22, and octave-shift-continue-22. This is left as a string so that other application-specific types can be defined, but it is made a separate type so that it can be redefined more strictly.

A quarter-rest type specifies the glyph to use when a note has a rest element and a type value of quarter. The c-clef, f-clef, and percussion-clef types specify the glyph to use when a clef sign element value is C, F, or percussion respectively. The g-clef-ottava-bassa type specifies the glyph to use when a clef sign element value is G and the clef-octave-change element value is -1. The octave-shift types specify the glyph to use when an octave-shift type attribute value is up, down, or continue and the octave-shift size attribute value is 8, 15, or 22.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:token"/>
	</xs:simpleType>




	<xs:simpleType name="note-size-type">
		<xs:annotation>
			<xs:documentation>The note-size-type type indicates the type of note being defined by a note-size element. The grace-cue type is used for notes of grace-cue size. The grace type is used for notes of cue size that include a grace element. The cue type is used for all other notes with cue size, whether defined explicitly or implicitly via a cue element. The large type is used for notes of large size.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:token">
			<xs:enumeration value="cue"/>
			<xs:enumeration value="grace"/>
			<xs:enumeration value="grace-cue"/>
			<xs:enumeration value="large"/>
		</xs:restriction>
	</xs:simpleType>
'''


# ///////////////
# Simple types derived from note.mod elements

class TypeAccidentalValue(SimpleType):
    """
    The accidental-value type represents notated accidentals supported by MusicXML. In the MusicXML 2.0 DTD this was a
    string with values that could be included. The XSD strengthens the data typing to an enumerated list. The quarter- a
    nd three-quarters- accidentals are Tartini-style quarter-tone accidentals. The -down and -up accidentals are
     quarter-tone accidentals that include arrows pointing down or up. The slash- accidentals are used in Turkish
     classical music. The numbered sharp and flat accidentals are superscripted versions of the accidental signs, used
     in Turkish folk music. The sori and koron accidentals are microtonal sharp and flat accidentals used in Iranian
     and Persian music.
    """
    _PERMITTED = ["sharp", "natural", "flat", "double-sharp", "sharp-sharp", "flat-flat", "natural-sharp",
                  "natural-flat", "quarter-flat", "quarter-sharp", "three-quarters-flat", "three-quarters-sharp",
                  "sharp-down", "sharp-up", "natural-down", "natural-up", "flat-down", "flat-up", "triple-sharp",
                  "triple-flat", "slash-quarter-sharp", "slash-sharp", "slash-flat", "double-slash-flat", "sharp-1",
                  "sharp-2", "sharp-3", "sharp-5", "flat-1", "flat-2", "flat-3", "flat-4", "sori", "karon"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeBeamValue(SimpleType):
    """
    The beam-value type represents the type of beam associated with each of 8 beam levels (up to 1024th notes) available
    for each note.
    """
    _PERMITTED = ["begin", "continue", "end", "forward hook", "backward hook"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeBreathMarkValue(SimpleType):
    """
    The breath-mark-value type represents the symbol used for a breath mark.
    """
    _PERMITTED = ["", "comma", "tick", "upbow", "salzedo"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeCaesuraValue(SimpleType):
    """
    The caesura-value type represents the shape of the caesura sign.
    """
    _PERMITTED = ["normal", "thick", "short", "curved", "single", ""]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeFan(SimpleType):
    """
    The fan type represents the type of beam fanning present on a note, used to represent accelerandos and
    ritardandos.
    """
    _PERMITTED = ["accel", "rit", "none"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeNoteTypeValue(SimpleType):
    """
    The note-type type is used for the MusicXML type element and represents the graphic note type, from 1024th (
    shortest) to maxima (longest)
    """
    _PERMITTED = (
        '1024th', '512th', '256th', '128th', '64th', '32nd', '16th', 'eighth', 'quarter', 'half', 'whole', 'breve',
        'long',
        'maxima')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeOctave(SimpleType):
    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        Integer(v)
        if v >= 9:
            raise ValueError(
                'Octave.value {} must be must be greater than or equal to 0. It  must be less than or equal to 9'.format(
                    v))
        self._value = v


class TypeSemitones(Decimal):
    """
    The semitones type is a number representing semitones, used for chromatic alteration. A value of -1 corresponds to
    a flat and a value of 1 to a sharp. Decimal values like 0.5 (quarter tone sharp) are used for microtones.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeShowTuplet(SimpleType):
    """
    The show-tuplet type indicates whether to show a part of a tuplet relating to the tuplet-actual element, both the
    tuplet-actual and tuplet-normal elements, or neither.
    """
    _PERMITTED = ('actual', 'both', 'none')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeStep(SimpleType):
    _PERMITTED = ('A', 'B', 'C', 'D', 'E', 'F', 'G')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeSyllabic(SimpleType):
    """
    documentation>Lyric hyphenation is indicated by the syllabic type. The single, begin, end, and middle values
    represent single-syllable words, word-beginning syllables, word-ending syllables, and mid-word syllables,
    respectively.
    """

    _PERMITTED = ["single", "begin", "end", "middle"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeNoteheadValue(SimpleType):
    """
    The notehead-value type indicates shapes other than the open and closed ovals associated with note durations.
    The values do, re, mi, fa, fa up, so, la, and ti correspond to Aikin's 7-shape system.  The fa up shape is typically
    used with upstems; the fa shape is typically used with downstems or no stems.

    The arrow shapes differ from triangle and inverted triangle by being centered on the stem. Slashed and back slashed
    notes include both the normal notehead and a slash. The triangle shape has the tip of the triangle pointing up;
    the inverted triangle shape has the tip of the triangle pointing down. The left triangle shape is a right triangle
    with the hypotenuse facing up and to the left.

    The other notehead covers noteheads other than those listed here. It is usually used in combination with the smufl
    attribute to specify a particular SMuFL notehead. The smufl attribute may be used with any notehead value to help
    specify the appearance of symbols that share the same MusicXML semantics. Noteheads in the SMuFL "Note name
    noteheads" range (U+E150–U+E1AF) should not use the smufl attribute or the "other" value, but instead use the
    notehead-text element.
    """

    _PERMITTED = ["slash", "triangle", "diamond", "square", "cross", "x", "circle-x", "inverted triangle", "arrow down",
                  "arrow up", "circled", "slashed", "back slashed", "normal", "cluster", "circle dot", "left triangle",
                  "rectangle", "none", "do", "re", "mi", "fa", "fa up", "so", "la", "ti", "other"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeTremoloMarks(SimpleType):
    """
    The number of tremolo marks is represented by a number from 0 to 8: the same as beam-level with 0 added.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        Integer(v)
        if not (0 <= v <= 8):
            raise ValueError(
                '{}.value {} must be must be greater than or equal to 0. It  must be less than or equal to 8'.format(
                    self.__class__, v))
        self._value = v


class TypeHoleClosedLocation(SimpleType):
    """The hole-closed-location type indicates which portion of the hole is filled in when the corresponding
    hole-closed-value is half.
    """

    _PERMITTED = ["right", "bottom", "left", "top"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeHoleClosedValue(SimpleType):
    """
    The hole-closed-value type represents whether the hole is closed, open, or half-open.
    """

    _PERMITTED = ["yes", "no", "half"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeStemValue(SimpleType):
    """
    The stem type represents the notated stem direction.
    """

    _PERMITTED = ["down", "up", "double", "none"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


'''
	<!-- Simple types derived from note.mod elements -->

	<xs:simpleType name="arrow-direction">
		<xs:annotation>
			<xs:documentation>The arrow-direction type represents the direction in which an arrow points, using Unicode arrow terminology.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="left"/>
			<xs:enumeration value="up"/>
			<xs:enumeration value="right"/>
			<xs:enumeration value="down"/>
			<xs:enumeration value="northwest"/>
			<xs:enumeration value="northeast"/>
			<xs:enumeration value="southeast"/>
			<xs:enumeration value="southwest"/>
			<xs:enumeration value="left right"/>
			<xs:enumeration value="up down"/>
			<xs:enumeration value="northwest southeast"/>
			<xs:enumeration value="northeast southwest"/>
			<xs:enumeration value="other"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="arrow-style">
		<xs:annotation>
			<xs:documentation>The arrow-style type represents the style of an arrow, using Unicode arrow terminology. Filled and hollow arrows indicate polygonal single arrows. Paired arrows are duplicate single arrows in the same direction. Combined arrows apply to double direction arrows like left right, indicating that an arrow in one direction should be combined with an arrow in the other direction.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="single"/>
			<xs:enumeration value="double"/>
			<xs:enumeration value="filled"/>
			<xs:enumeration value="hollow"/>
			<xs:enumeration value="paired"/>
			<xs:enumeration value="combined"/>
			<xs:enumeration value="other"/>
		</xs:restriction>
	</xs:simpleType>



	
	<xs:simpleType name="circular-arrow">
		<xs:annotation>
			<xs:documentation>The circular-arrow type represents the direction in which a circular arrow points, using Unicode arrow terminology.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="clockwise"/>
			<xs:enumeration value="anticlockwise"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="handbell-value">
		<xs:annotation>
			<xs:documentation>The handbell-value type represents the type of handbell technique being notated.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="belltree"/>
			<xs:enumeration value="damp"/>
			<xs:enumeration value="echo"/>
			<xs:enumeration value="gyro"/>
			<xs:enumeration value="hand martellato"/>
			<xs:enumeration value="mallet lift"/>
			<xs:enumeration value="mallet table"/>
			<xs:enumeration value="martellato"/>
			<xs:enumeration value="martellato lift"/>
			<xs:enumeration value="muted martellato"/>
			<xs:enumeration value="pluck lift"/>
			<xs:enumeration value="swing"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="harmon-closed-location">
		<xs:annotation>
			<xs:documentation>The harmon-closed-location type indicates which portion of the symbol is filled in when the corresponding harmon-closed-value is half.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="right"/>
			<xs:enumeration value="bottom"/>
			<xs:enumeration value="left"/>
			<xs:enumeration value="top"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="harmon-closed-value">
		<xs:annotation>
			<xs:documentation>The harmon-closed-value type represents whether the harmon mute is closed, open, or half-open.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="yes"/>
			<xs:enumeration value="no"/>
			<xs:enumeration value="half"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="show-tuplet">
		<xs:annotation>
			<xs:documentation>The show-tuplet type indicates whether to show a part of a tuplet relating to the tuplet-actual element, both the tuplet-actual and tuplet-normal elements, or neither.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:token">
			<xs:enumeration value="actual"/>
			<xs:enumeration value="both"/>
			<xs:enumeration value="none"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="stem-value">
		<xs:annotation>
			<xs:documentation>The stem type represents the notated stem direction.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="down"/>
			<xs:enumeration value="up"/>
			<xs:enumeration value="double"/>
			<xs:enumeration value="none"/>
		</xs:restriction>
	</xs:simpleType>

	<xs:simpleType name="tap-hand">
		<xs:annotation>
			<xs:documentation>The tap-hand type represents the symbol to use for a tap element. The left and right values refer to the SMuFL guitarLeftHandTapping and guitarRightHandTapping glyphs respectively.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:string">
			<xs:enumeration value="left"/>
			<xs:enumeration value="right"/>
		</xs:restriction>
	</xs:simpleType>
'''


# ///////////////
# Simple types derived from score.mod elements

class TypeMeasureText(Token):
    """
    The measure - text type is used for the text attribute of measure elements. It has at least one character.
    The implicit attribute of the measure element should be set to "yes" rather than setting the text attribute to an
    empty  string."""

    def __init__(self, value='1', *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        if len(v) < 1:
            raise ValueError(
                '{}.value {} must have at least one character'.format(self.__class__.__name__, v))
        self._value = v


'''
	<!-- Simple types derived from score.mod elements -->
'''


class TypeGroupBarlineValue(SimpleType):
    """
    The group-barline-value type indicates if the group should have common barlines.
    """
    _PERMITTED = ["yes", "no", "Mensurstrich"]


class TypeGroupSymbolValue(SimpleType):
    """
    The group-symbol-value type indicates how the symbol for a group is indicated in the score.
    The default value is none.
    """
    _PERMITTED = ["none", "brace", "line", "bracket", "square"]

    def __init__(self, value=None, *args, **kwargs):
        if not value:
            value = 'none'
        super().__init__(value=value, *args, **kwargs)
