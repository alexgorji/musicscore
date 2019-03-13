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


class Divisions(Integer):
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


class ClefSign(SimpleType):
    """
    The clef-sign element represents the different clef symbols.
    The jianpu sign indicates that the music that follows should be in jianpu numbered notation,
    just as the TAB sign indicates that the music that follows should be in tablature notation.
    Unlike TAB, a jianpu sign does not correspond to a visual clef notation.
    """
    permitted = ('G', 'F', 'C', 'percussion', 'TAB', 'jianpu', 'none')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class StaffLine(PositiveInteger):
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


class FontWeightType(SimpleType):
    permitted = ('normal', 'bold')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class FontSizeType(Decimal):

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class FontStyleType(SimpleType):
    permitted = ('normal', 'italic')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class CommaSeparatedText(SimpleType):
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


class RightLeftMiddle(SimpleType):
    permitted = ('right', 'left', 'middle')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class BarStyleType(SimpleType):
    permitted = ('regular', 'dotted', 'dashed', 'heavy', 'light-light', 'light-heavy', 'heavy-light', 'heavy-heavy',
                 'tick', 'short' 'none')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class ColorType(SimpleType):
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
        if v >= 100 or v <= 0:
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

class SmulfGlyphName(SimpleType):
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


class CancelLocation(SimpleType):
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


class SymbolSize(SimpleType):
    """
    The symbol-size type is used to distinguish between full, cue sized, grace cue sized, and oversized symbols.
    """
    permitted = ["full", "cue", "grace-cue", "large"]

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)
