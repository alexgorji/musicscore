import re


class SimpleType(object):
    permitted = ()

    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if v is not None and v not in self.permitted:
            raise ValueError('{}.value {} must be None or in {} '.format(self.__class__.__name__, v, self.permitted))
        self._value = v
        self._text = v

    def __repr__(self):
        return str(self.value)


# ///////////////

class ExampleType(SimpleType):
    permitted = ('one', 'two', 'three')

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


class Integer(SimpleType):
    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        if not isinstance(v, int):
            raise TypeError('value {} must be an int'.format(v))
        self._value = v


class NonNegativeDecimal(SimpleType):
    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        if not isinstance(v, float) and not isinstance(v, int):
            raise TypeError('value {} must a be a non negative float or int'.format(v))
        if v < 0:
            raise ValueError('value {} must be non negative'.format(v))
        self._value = v


class PositiveDecimal(SimpleType):
    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        if not isinstance(v, float) and not isinstance(v, int):
            raise TypeError('value {} must a be a positive float or int'.format(v))
        if v <= 0:
            raise ValueError('value {} must be positive'.format(v))
        self._value = v


class PositiveInteger(SimpleType):
    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        Integer(v)
        if v < 1:
            raise ValueError('value {} must a be positive.'.format(v))

        self._value = v


class String(SimpleType):
    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        if not isinstance(v, str):
            raise TypeError('value {} must a be string'.format(v))
        self._value = v


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


# ///////////////


class TypeStep(SimpleType):
    permitted = ('A', 'B', 'C', 'D', 'E', 'F', 'G')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeAlter(SimpleType):
    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        Decimal(v)
        if v < -2 or v > 2:
            raise ValueError('Alter.value {} must be greater than -2 and  less than 2'.format(v))
        self._value = v


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


# ///////////////


class TypeDivisions(Integer):
    """
    The divisions type is used to express values in terms of the musical divisions defined by the divisions element.
    It is preferred that these be integer values both for MIDI interoperability and to avoid roundoff errors.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class Tenths(Decimal):
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


class PositiveDivisions(PositiveInteger):
    """
    The positive-divisions type restricts divisions values to positive numbers.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeClefSign(SimpleType):
    """
    The clef-sign element represents the different clef symbols.
    The jianpu sign indicates that the music that follows should be in jianpu numbered notation,
    just as the TAB sign indicates that the music that follows should be in tablature notation.
    Unlike TAB, a jianpu sign does not correspond to a visual clef notation.
    """
    permitted = ('G', 'F', 'C', 'percussion', 'TAB', 'jianpu', 'none')

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


class NoteTypeValue(SimpleType):
    """
    The note-type type is used for the MusicXML type element and represents the graphic note type, from 1024th (
    shortest) to maxima (longest)
    """
    permitted = (
        '1024th', '512th', '256th', '128th', '64th', '32nd', '16th', 'eighth', 'quarter', 'half', 'whole', 'breve',
        'long',
        'maxima')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class YesNo(SimpleType):
    permitted = ('yes', 'no')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeFontWeight(SimpleType):
    permitted = ('normal', 'bold')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeFontSize(Decimal):

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeFontStyle(SimpleType):
    permitted = ('normal', 'italic')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class CommaSeparatedText(Token):
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


class RightLeftMiddle(SimpleType):
    permitted = ('right', 'left', 'middle')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class AboveBelow(SimpleType):
    permitted = ('above', 'below')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeBarStyle(SimpleType):
    permitted = ('regular', 'dotted', 'dashed', 'heavy', 'light-light', 'light-heavy', 'heavy-light', 'heavy-heavy',
                 'tick', 'short' 'none')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeColor(Token):
    pattern = r'^#[\dA-F]{6}([\dA-F][\dA-F])?$'
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


class Percent(Decimal):
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


class TypeSemitones(Decimal):
    """
    The semitones type is a number representing semitones, used for chromatic alteration. A value of -1 corresponds to
    a flat and a value of 1 to a sharp. Decimal values like 0.5 (quarter tone sharp) are used for microtones.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


# /////////////// KEY

class SmulfGlyphName(Token):
    """
    The smufl-glyph-name type is used for attributes that reference a specific Standard Music Font Layout (SMuFL)
    character. The value is a SMuFL canonical glyph name, not a code point. For instance, the value for a standard piano
    pedal mark would be keyboardPedalPed, not U+E650.
    <xs:restriction base="xs:NMTOKEN"/>
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)
        raise NotImplementedError()


class SmulfAccidentalGlyphName(SmulfGlyphName):
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
    permitted = ["sharp", "natural", "flat", "double-sharp", "sharp-sharp", "flat-flat", "natural-sharp",
                 "natural-flat", "quarter-flat", "quarter-sharp", "three-quarters-flat", "three-quarters-sharp",
                 "sharp-down", "sharp-up", "natural-down", "natural-up", "flat-down", "flat-up", "triple-sharp",
                 "triple-flat", "slash-quarter-sharp", "slash-sharp", "slash-flat", "double-slash-flat", "sharp-1",
                 "sharp-2", "sharp-3", "sharp-5", "flat-1", "flat-2", "flat-3", "flat-4", "sori", "karon"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeCancelLocation(SimpleType):
    """
    The cancel-location type is used to indicate where a key signature cancellation appears relative to a new key
    signature: to the left, to the right, or before the barline and to the left. It is left by default. For mid-measure
    key elements, a cancel-location of before-barline should be treated like a cancel-location of left.
    """
    permitted = ['left', 'right', 'before-barline']

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeFifths(Integer):
    """
    The fifths type represents the number of flats or sharps in a traditional key signature. Negative numbers are used
    for flats and positive numbers for sharps, reflecting the key's placement within the circle of fifths
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeMode(SimpleType):
    """
    The mode type is used to specify major/minor and other mode distinctions. Valid mode values include major, minor,
    dorian, phrygian, lydian, mixolydian, aeolian, ionian, locrian, and none
    """
    permitted = ['major', 'minor', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'ionian', 'locrian', 'none']

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeSymbolSize(SimpleType):
    """
    The symbol-size type is used to distinguish between full, cue sized, grace cue sized, and oversized symbols.
    """
    permitted = ["full", "cue", "grace-cue", "large"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeMeasureText(Token):
    """
    The measure-text type is used for the text attribute of measure elements. It has at least one character. The
    implicit attribute of the measure element should be set to "yes" rather than setting the text attribute to an empty
    string.
    """

    def __init__(self, value='1', *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        if len(v) < 1:
            raise ValueError(
                '{}.value {} must have at least one character'.format(self.__class__.__name__, v))
        self._value = v


# BEAM

class TypeBeamValue(SimpleType):
    """
    The beam-value type represents the type of beam associated with each of 8 beam levels (up to 1024th notes) available
    for each note.
    """
    permitted = ["begin", "continue", "end", "forward hook", "backward hook"]

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
        if v < 1 or v > 8:
            raise ValueError(
                '{}.value {} must be between 1 and 8'.format(self.__class__.__name__, v))
        self._value = v


class TypeFan(SimpleType):
    """
    The fan type represents the type of beam fanning present on a note, used to represent accelerandos and
    ritardandos.
    """
    permitted = ["accel", "rit", "none"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeValign(SimpleType):
    """
    The valign type is used to indicate vertical alignment to the top, middle, bottom, or baseline of the text.
    Defaults are implementation-dependent.
    """

    permitted = ["top", "middle", "bottom", "baseline"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


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


class NumberOrNormal(SimpleType):
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


class TypeTextDirection(SimpleType):
    """documentation>The text-direction type is used to adjust and override the Unicode bidirectional text algorithm,
    similar to the W3C Internationalization Tag Set recommendation. Values are ltr (left-to-right embed), rtl (right-to-
    left embed), lro (left-to-right bidi-override), and rlo (right-to-left bidi-override). The default value is ltr.
    This type is typically used by applications that store text in left-to-right visual order rather than logical order.
    Such applications can use the lro value to better communicate with other applications that more fully support
    bidirectional text.
    """

    permitted = ["ltr", "rtl", "lro", "rlo"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class TypeEnclosureShape(SimpleType):
    """The enclosure-shape type describes the shape and presence / absence of an enclosure around text or symbols. A
    bracket enclosure is similar to a rectangle with the bottom line missing, as is common in jazz notation.
    """
    permitted = ["rectangle", "square", "oval", "circle", "bracket", "triangle", "diamond", "pentagon", "hexagon",
                 "heptagon", "octagon", "nonagon", "decagon", "none"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)

class TypeLevel():
    pass