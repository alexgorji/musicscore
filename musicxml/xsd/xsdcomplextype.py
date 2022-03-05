from musicxml.generate_classes.utils import musicxml_xsd_et_root
from musicxml.util.core import convert_to_xsd_class_name
from musicxml.xsd.xsdsimpletype import *
from musicxml.xsd.xsdattribute import *
from musicxml.xsd.xsdindicator import *
from musicxml.xsd.xsdtree import XSDTreeElement, XSDTree
import xml.etree.ElementTree as ET


class XSDComplexType(XSDTreeElement):
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ''

    def __init__(self, value=None, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.value = value
        self._value = None

    def _get_error_class(self):
        if self.parent:
            return self.parent.__class__.__name__
        else:
            return self.__class__.__name__

    def _check_value(self, val):
        if self._SIMPLE_CONTENT:
            try:
                self._SIMPLE_CONTENT(val)
            except TypeError as err:
                raise TypeError(f"{self._get_error_class()}: " + err.args[0])
            except ValueError as err:
                raise ValueError(f"{self._get_error_class()}: " + err.args[0])

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._check_value(v)
        self._value = v

    @classmethod
    def get_xsd_attributes(cls):
        output = []
        if cls.get_xsd_tree().get_simple_content_extension():
            for child in cls.get_xsd_tree().get_simple_content_extension().get_children():
                if child.tag == 'attribute':
                    output.append(XSDAttribute(child))
                elif child.tag == 'attributeGroup':
                    output.extend(eval(child.xsd_element_class_name).get_xsd_attributes())
        elif cls.get_xsd_tree().get_complex_content():
            complex_content_extension = cls.get_xsd_tree().get_complex_content_extension()
            complex_type_extension_base_class_name = convert_to_xsd_class_name(complex_content_extension.get_attributes()['base'],
                                                                               'complex_type')
            extension_base = eval(complex_type_extension_base_class_name)
            output.extend(extension_base.get_xsd_attributes())
            for child in complex_content_extension.get_children():
                if child.tag == 'attribute':
                    output.append(XSDAttribute(child))
                elif child.tag == 'attributeGroup':
                    output.extend(eval(child.xsd_element_class_name).get_xsd_attributes())
            return output
        else:
            for child in cls.get_xsd_tree().get_children():
                if child.tag == 'attribute':
                    output.append(XSDAttribute(child))
                elif child.tag == 'attributeGroup':
                    output.extend(eval(child.xsd_element_class_name).get_xsd_attributes())
        return output

    @classmethod
    def get_xsd_indicator(cls):
        def get_occurrences(ch):
            min_ = ch.get_attributes().get('minOccurs')
            max_ = ch.get_attributes().get('maxOccurs')
            return 1 if not min_ else int(min_), 1 if not max_ else 'unbounded' if max_ == 'unbounded' else int(max_)

        for child in cls.get_xsd_tree().get_children():
            if child.tag == 'sequence':
                return XSDSequence(child), *get_occurrences(child)
            if child.tag == 'choice':
                return XSDChoice(child), *get_occurrences(child)
            if child.tag == 'group':
                return eval(convert_to_xsd_class_name(child.get_attributes()['ref'], 'group'))(), *get_occurrences(child)
            if child.tag == 'complexContent':
                return eval(convert_to_xsd_class_name(child.get_children()[0].get_attributes()['base'],
                                                      'complex_type')).get_xsd_indicator()


class XSDComplexTypeScorePartwise(XSDComplexType):
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='score-partwise']//{*}complexType"


class XSDComplexTypePart(XSDComplexType):
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='score-partwise']//{*}complexType//{*}complexType"


class XSDComplexTypeMeasure(XSDComplexType):
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='score-partwise']//{*}complexType//{*}complexType//{*}complexType"


class XSDComplexTypeDirective(XSDComplexType):
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='attributes']//{*}complexType"


# Note's choice is being manually reordered to avoid using intelligent choice for each Note without grace.
class XSDComplexTypeNote(XSDComplexType):
    """Notes are the most common type of MusicXML data. The MusicXML format distinguishes between elements used for sound information and elements used for notation information (e.g., tie is used for sound, tied for notation). Thus grace notes do not have a duration element. Cue notes have a duration element, as do forward elements, but no tie elements. Having these two types of information available can make interchange easier, as some programs handle one type of information more readily than the other.

The print-leger attribute is used to indicate whether leger lines are printed. Notes without leger lines are used to indicate indeterminate high and low notes. By default, it is set to yes. If print-object is set to no, print-leger is interpreted to also be set to no if not present. This attribute is ignored for rests.

The dynamics and end-dynamics attributes correspond to MIDI 1.0's Note On and Note Off velocities, respectively. They are expressed in terms of percentages of the default forte value (90 for MIDI 1.0).

The attack and release attributes are used to alter the starting and stopping time of the note from when it would otherwise occur based on the flow of durations - information that is specific to a performance. They are expressed in terms of divisions, either positive or negative. A note that starts a tie should not have a release attribute, and a note that stops a tie should not have an attack attribute. The attack and release attributes are independent of each other. The attack attribute only changes the starting time of a note, and the release attribute only changes the stopping time of a note.

If a note is played only particular times through a repeat, the time-only attribute shows which times to play the note.

The pizzicato attribute is used when just this note is sounded pizzicato, vs. the pizzicato element which changes overall playback between pizzicato and arco.
"""

    _XSD_TREE = XSDTree(ET.fromstring("""
<xs:complexType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="note">
    <xs:annotation>
        <xs:documentation>Notes are the most common type of MusicXML data. The MusicXML format distinguishes between elements used for sound information and elements used for notation information (e.g., tie is used for sound, tied for notation). Thus grace notes do not have a duration element. Cue notes have a duration element, as do forward elements, but no tie elements. Having these two types of information available can make interchange easier, as some programs handle one type of information more readily than the other.

The print-leger attribute is used to indicate whether leger lines are printed. Notes without leger lines are used to indicate indeterminate high and low notes. By default, it is set to yes. If print-object is set to no, print-leger is interpreted to also be set to no if not present. This attribute is ignored for rests.

The dynamics and end-dynamics attributes correspond to MIDI 1.0's Note On and Note Off velocities, respectively. They are expressed in terms of percentages of the default forte value (90 for MIDI 1.0).

The attack and release attributes are used to alter the starting and stopping time of the note from when it would otherwise occur based on the flow of durations - information that is specific to a performance. They are expressed in terms of divisions, either positive or negative. A note that starts a tie should not have a release attribute, and a note that stops a tie should not have an attack attribute. The attack and release attributes are independent of each other. The attack attribute only changes the starting time of a note, and the release attribute only changes the stopping time of a note.

If a note is played only particular times through a repeat, the time-only attribute shows which times to play the note.

The pizzicato attribute is used when just this note is sounded pizzicato, vs. the pizzicato element which changes overall playback between pizzicato and arco.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:choice>
            <xs:sequence>
                <xs:group ref="full-note" />
                <xs:group ref="duration" />
                <xs:element name="tie" type="tie" minOccurs="0" maxOccurs="2" />
            </xs:sequence>
            <xs:sequence>
                <xs:element name="cue" type="empty">
                    <xs:annotation>
                        <xs:documentation>The cue element indicates the presence of a cue note. In MusicXML, a cue note is a silent note with no playback. Normal notes that play can be specified as cue size using the type element. A cue note that is specified as full size using the type element will still remain silent.</xs:documentation>
                    </xs:annotation>
                </xs:element>
                <xs:group ref="full-note" />
                <xs:group ref="duration" />
            </xs:sequence>
            <xs:sequence>
                <xs:element name="grace" type="grace" />
                <xs:choice>
                    <xs:sequence>
                        <xs:group ref="full-note" />
                        <xs:element name="tie" type="tie" minOccurs="0" maxOccurs="2" />
                    </xs:sequence>
                    <xs:sequence>
                        <xs:element name="cue" type="empty" />
                        <xs:group ref="full-note" />
                    </xs:sequence>
                </xs:choice>
            </xs:sequence>
        </xs:choice>
        <xs:element name="instrument" type="instrument" minOccurs="0" maxOccurs="unbounded" />
        <xs:group ref="editorial-voice" />
        <xs:element name="type" type="note-type" minOccurs="0" />
        <xs:element name="dot" type="empty-placement" minOccurs="0" maxOccurs="unbounded">
            <xs:annotation>
                <xs:documentation>One dot element is used for each dot of prolongation. The placement attribute is used to specify whether the dot should appear above or below the staff line. It is ignored for notes that appear on a staff space.</xs:documentation>
            </xs:annotation>
        </xs:element>
        <xs:element name="accidental" type="accidental" minOccurs="0" />
        <xs:element name="time-modification" type="time-modification" minOccurs="0" />
        <xs:element name="stem" type="stem" minOccurs="0" />
        <xs:element name="notehead" type="notehead" minOccurs="0" />
        <xs:element name="notehead-text" type="notehead-text" minOccurs="0" />
        <xs:group ref="staff" minOccurs="0" />
        <xs:element name="beam" type="beam" minOccurs="0" maxOccurs="8" />
        <xs:element name="notations" type="notations" minOccurs="0" maxOccurs="unbounded" />
        <xs:element name="lyric" type="lyric" minOccurs="0" maxOccurs="unbounded" />
        <xs:element name="play" type="play" minOccurs="0" />
        <xs:element name="listen" type="listen" minOccurs="0" />
    </xs:sequence>
    <xs:attributeGroup ref="x-position" />
    <xs:attributeGroup ref="font" />
    <xs:attributeGroup ref="color" />
    <xs:attributeGroup ref="printout" />
    <xs:attribute name="print-leger" type="yes-no" />
    <xs:attribute name="dynamics" type="non-negative-decimal" />
    <xs:attribute name="end-dynamics" type="non-negative-decimal" />
    <xs:attribute name="attack" type="divisions" />
    <xs:attribute name="release" type="divisions" />
    <xs:attribute name="time-only" type="time-only" />
    <xs:attribute name="pizzicato" type="yes-no" />
    <xs:attributeGroup ref="optional-unique-id" />
</xs:complexType>
"""
                                      ))
# -----------------------------------------------------
# AUTOMATICALLY GENERATED WITH generate_complex_types.py
# -----------------------------------------------------


class XSDComplexTypeAccidentalText(XSDComplexType):
    """The accidental-text type represents an element with an accidental value and text-formatting attributes.

``simpleContent``: The accidental-value type represents notated accidentals supported by MusicXML. In the MusicXML 2.0 DTD this was a string with values that could be included. The XSD strengthens the data typing to an enumerated list. The quarter- and three-quarters- accidentals are Tartini-style quarter-tone accidentals. The -down and -up accidentals are quarter-tone accidentals that include arrows pointing down or up. The slash- accidentals are used in Turkish classical music. The numbered sharp and flat accidentals are superscripted versions of the accidental signs, used in Turkish folk music. The sori and koron accidentals are microtonal sharp and flat accidentals used in Iranian and Persian music. The other accidental covers accidentals other than those listed here. It is usually used in combination with the smufl attribute to specify a particular SMuFL accidental. The smufl attribute may be used with any accidental value to help specify the appearance of symbols that share the same MusicXML semantics.
    
    Permitted Values: ``'sharp'``, ``'natural'``, ``'flat'``, ``'double-sharp'``, ``'sharp-sharp'``, ``'flat-flat'``, ``'natural-sharp'``, ``'natural-flat'``, ``'quarter-flat'``, ``'quarter-sharp'``, ``'three-quarters-flat'``, ``'three-quarters-sharp'``, ``'sharp-down'``, ``'sharp-up'``, ``'natural-down'``, ``'natural-up'``, ``'flat-down'``, ``'flat-up'``, ``'double-sharp-down'``, ``'double-sharp-up'``, ``'flat-flat-down'``, ``'flat-flat-up'``, ``'arrow-down'``, ``'arrow-up'``, ``'triple-sharp'``, ``'triple-flat'``, ``'slash-quarter-sharp'``, ``'slash-sharp'``, ``'slash-flat'``, ``'double-slash-flat'``, ``'sharp-1'``, ``'sharp-2'``, ``'sharp-3'``, ``'sharp-5'``, ``'flat-1'``, ``'flat-2'``, ``'flat-3'``, ``'flat-4'``, ``'sori'``, ``'koron'``, ``'other'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeAccidentalValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='accidental-text']"


class XSDComplexTypeCoda(XSDComplexType):
    """The coda type is the visual indicator of a coda sign. The exact glyph can be specified with the smufl attribute. A sound element is also needed to guide playback applications reliably."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='coda']"


class XSDComplexTypeDynamics(XSDComplexType):
    """Dynamics can be associated either with a note or a general musical direction. To avoid inconsistencies between and amongst the letter abbreviations for dynamics (what is sf vs. sfz, standing alone or with a trailing dynamic that is not always piano), we use the actual letters as the names of these dynamic elements. The other-dynamics element allows other dynamic marks that are not covered here. Dynamics elements may also be combined to create marks not covered by a single element, such as sfmp.

These letter dynamic symbols are separated from crescendo, decrescendo, and wedge indications. Dynamic representation is inconsistent in scores. Many things are assumed by the composer and left out, such as returns to original dynamics. The MusicXML format captures what is in the score, but does not try to be optimal for analysis or synthesis of dynamics.

The placement attribute is used when the dynamics are associated with a note. It is ignored when the dynamics are associated with a direction. In that case the direction element's placement attribute is used instead."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='dynamics']"


class XSDComplexTypeEmpty(XSDComplexType):
    """The empty type represents an empty element with no attributes."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='empty']"


class XSDComplexTypeEmptyPlacement(XSDComplexType):
    """The empty-placement type represents an empty element with print-style and placement attributes."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='empty-placement']"


class XSDComplexTypeEmptyPlacementSmufl(XSDComplexType):
    """The empty-placement-smufl type represents an empty element with print-style, placement, and smufl attributes."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='empty-placement-smufl']"


class XSDComplexTypeEmptyPrintStyle(XSDComplexType):
    """The empty-print-style type represents an empty element with print-style attribute group."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='empty-print-style']"


class XSDComplexTypeEmptyPrintStyleAlign(XSDComplexType):
    """The empty-print-style-align type represents an empty element with print-style-align attribute group."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='empty-print-style-align']"


class XSDComplexTypeEmptyPrintStyleAlignId(XSDComplexType):
    """The empty-print-style-align-id type represents an empty element with print-style-align and optional-unique-id attribute groups."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='empty-print-style-align-id']"


class XSDComplexTypeEmptyPrintObjectStyleAlign(XSDComplexType):
    """The empty-print-style-align-object type represents an empty element with print-object and print-style-align attribute groups."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='empty-print-object-style-align']"


class XSDComplexTypeEmptyTrillSound(XSDComplexType):
    """The empty-trill-sound type represents an empty element with print-style, placement, and trill-sound attributes."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='empty-trill-sound']"


class XSDComplexTypeHorizontalTurn(XSDComplexType):
    """The horizontal-turn type represents turn elements that are horizontal rather than vertical. These are empty elements with print-style, placement, trill-sound, and slash attributes. If the slash attribute is yes, then a vertical line is used to slash the turn. It is no if not specified."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='horizontal-turn']"


class XSDComplexTypeFermata(XSDComplexType):
    """The fermata text content represents the shape of the fermata sign. An empty fermata element represents a normal fermata. The fermata type is upright if not specified.

``simpleContent``: The fermata-shape type represents the shape of the fermata sign. The empty value is equivalent to the normal value.
    
    Permitted Values: ``'normal'``, ``'angled'``, ``'square'``, ``'double-angled'``, ``'double-square'``, ``'double-dot'``, ``'half-curve'``, ``'curlew'``, ``''``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeFermataShape
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='fermata']"


class XSDComplexTypeFingering(XSDComplexType):
    """Fingering is typically indicated 1,2,3,4,5. Multiple fingerings may be given, typically to substitute fingerings in the middle of a note. The substitution and alternate values are "no" if the attribute is not present. For guitar and other fretted instruments, the fingering element represents the fretting finger; the pluck element represents the plucking finger."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='fingering']"


class XSDComplexTypeFormattedSymbol(XSDComplexType):
    """The formatted-symbol type represents a SMuFL musical symbol element with formatting attributes.

``simpleContent``: The smufl-glyph-name type is used for attributes that reference a specific Standard Music Font Layout (SMuFL) character. The value is a SMuFL canonical glyph name, not a code point. For instance, the value for a standard piano pedal mark would be keyboardPedalPed, not U+E650."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeSmuflGlyphName
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='formatted-symbol']"


class XSDComplexTypeFormattedSymbolId(XSDComplexType):
    """The formatted-symbol-id type represents a SMuFL musical symbol element with formatting and id attributes.

``simpleContent``: The smufl-glyph-name type is used for attributes that reference a specific Standard Music Font Layout (SMuFL) character. The value is a SMuFL canonical glyph name, not a code point. For instance, the value for a standard piano pedal mark would be keyboardPedalPed, not U+E650."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeSmuflGlyphName
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='formatted-symbol-id']"


class XSDComplexTypeFormattedText(XSDComplexType):
    """The formatted-text type represents a text element with text-formatting attributes."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='formatted-text']"


class XSDComplexTypeFormattedTextId(XSDComplexType):
    """The formatted-text-id type represents a text element with text-formatting and id attributes."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='formatted-text-id']"


class XSDComplexTypeFret(XSDComplexType):
    """The fret element is used with tablature notation and chord diagrams. Fret numbers start with 0 for an open string and 1 for the first fret."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeNonNegativeInteger
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='fret']"


class XSDComplexTypeLevel(XSDComplexType):
    """The level type is used to specify editorial information for different MusicXML elements. The content contains identifying and/or descriptive text about the editorial status of the parent element.

If the reference attribute is yes, this indicates editorial information that is for display only and should not affect playback. For instance, a modern edition of older music may set reference="yes" on the attributes containing the music's original clef, key, and time signature. It is no if not specified.

The type attribute indicates whether the editorial information applies to the start of a series of symbols, the end of a series of symbols, or a single symbol. It is single if not specified for compatibility with earlier MusicXML versions."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='level']"


class XSDComplexTypeMidiDevice(XSDComplexType):
    """The midi-device type corresponds to the DeviceName meta event in Standard MIDI Files. The optional port attribute is a number from 1 to 16 that can be used with the unofficial MIDI 1.0 port (or cable) meta event. Unlike the DeviceName meta event, there can be multiple midi-device elements per MusicXML part. The optional id attribute refers to the score-instrument assigned to this device. If missing, the device assignment affects all score-instrument elements in the score-part."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='midi-device']"


class XSDComplexTypeMidiInstrument(XSDComplexType):
    """The midi-instrument type defines MIDI 1.0 instrument playback. The midi-instrument element can be a part of either the score-instrument element at the start of a part, or the sound element within a part. The id attribute refers to the score-instrument affected by the change."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='midi-instrument']"


class XSDComplexTypeNameDisplay(XSDComplexType):
    """The name-display type is used for exact formatting of multi-font text in part and group names to the left of the system. The print-object attribute can be used to determine what, if anything, is printed at the start of each system. Enclosure for the display-text element is none by default. Language for the display-text element is Italian ("it") by default."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='name-display']"


class XSDComplexTypeOtherPlay(XSDComplexType):
    """The other-play element represents other types of playback. The required type attribute indicates the type of playback to which the element content applies."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='other-play']"


class XSDComplexTypePlay(XSDComplexType):
    """The play type specifies playback techniques to be used in conjunction with the instrument-sound element. When used as part of a sound element, it applies to all notes going forward in score order. In multi-instrument parts, the affected instrument should be specified using the id attribute. When used as part of a note element, it applies to the current note only."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='play']"


class XSDComplexTypeSegno(XSDComplexType):
    """The segno type is the visual indicator of a segno sign. The exact glyph can be specified with the smufl attribute. A sound element is also needed to guide playback applications reliably."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='segno']"


class XSDComplexTypeString(XSDComplexType):
    """The string type is used with tablature notation, regular notation (where it is often circled), and chord diagrams. String numbers start with 1 for the highest pitched full-length string.

``simpleContent``: The string-number type indicates a string number. Strings are numbered from high to low, with 1 being the highest pitched full-length string."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeStringNumber
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='string']"


class XSDComplexTypeTypedText(XSDComplexType):
    """The typed-text type represents a text element with a type attribute."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='typed-text']"


class XSDComplexTypeWavyLine(XSDComplexType):
    """Wavy lines are one way to indicate trills and vibrato. When used with a barline element, they should always have type="continue" set. The smufl attribute specifies a particular wavy line glyph from the SMuFL Multi-segment lines range."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='wavy-line']"


class XSDComplexTypeAttributes(XSDComplexType):
    """The attributes element contains musical information that typically changes on measure boundaries. This includes key and time signatures, clefs, transpositions, and staving. When attributes are changed mid-measure, it affects the music in score order, not in MusicXML document order."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='attributes']"


class XSDComplexTypeBeatRepeat(XSDComplexType):
    """The beat-repeat type is used to indicate that a single beat (but possibly many notes) is repeated. The slashes attribute specifies the number of slashes to use in the symbol. The use-dots attribute indicates whether or not to use dots as well (for instance, with mixed rhythm patterns). The value for slashes is 1 and the value for use-dots is no if not specified.

The stop type indicates the first beat where the repeats are no longer displayed. Both the start and stop of the beat being repeated should be specified unless the repeats are displayed through the end of the part.

The beat-repeat element specifies a notation style for repetitions. The actual music being repeated needs to be repeated within the MusicXML file. This element specifies the notation that indicates the repeat."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='beat-repeat']"


class XSDComplexTypeCancel(XSDComplexType):
    """A cancel element indicates that the old key signature should be cancelled before the new one appears. This will always happen when changing to C major or A minor and need not be specified then. The cancel value matches the fifths value of the cancelled key signature (e.g., a cancel of -2 will provide an explicit cancellation for changing from B flat major to F major). The optional location attribute indicates where the cancellation appears relative to the new key signature.

``simpleContent``: The fifths type represents the number of flats or sharps in a traditional key signature. Negative numbers are used for flats and positive numbers for sharps, reflecting the key's placement within the circle of fifths (hence the type name)."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeFifths
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='cancel']"


class XSDComplexTypeClef(XSDComplexType):
    """Clefs are represented by a combination of sign, line, and clef-octave-change elements. The optional number attribute refers to staff numbers within the part. A value of 1 is assumed if not present.

Sometimes clefs are added to the staff in non-standard line positions, either to indicate cue passages, or when there are multiple clefs present simultaneously on one staff. In this situation, the additional attribute is set to "yes" and the line value is ignored. The size attribute is used for clefs where the additional attribute is "yes". It is typically used to indicate cue clefs.

Sometimes clefs at the start of a measure need to appear after the barline rather than before, as for cues or for use after a repeated section. The after-barline attribute is set to "yes" in this situation. The attribute is ignored for mid-measure clefs.

Clefs appear at the start of each system unless the print-object attribute has been set to "no" or the additional attribute has been set to "yes"."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='clef']"


class XSDComplexTypeDouble(XSDComplexType):
    """The double type indicates that the music is doubled one octave from what is currently written. If the above attribute is set to yes, the doubling is one octave above what is written, as for mixed flute / piccolo parts in band literature. Otherwise the doubling is one octave below what is written, as for mixed cello / bass parts in orchestral literature."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='double']"


class XSDComplexTypeForPart(XSDComplexType):
    """The for-part type is used in a concert score to indicate the transposition for a transposed part created from that score. It is only used in score files that contain a concert-score element in the defaults. This allows concert scores with transposed parts to be represented in a single uncompressed MusicXML file.

The optional number attribute refers to staff numbers, from top to bottom on the system. If absent, the child elements apply to all staves in the created part."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='for-part']"


class XSDComplexTypeInterchangeable(XSDComplexType):
    """The interchangeable type is used to represent the second in a pair of interchangeable dual time signatures, such as the 6/8 in 3/4 (6/8). A separate symbol attribute value is available compared to the time element's symbol attribute, which applies to the first of the dual time signatures."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='interchangeable']"


class XSDComplexTypeKey(XSDComplexType):
    """The key type represents a key signature. Both traditional and non-traditional key signatures are supported. The optional number attribute refers to staff numbers. If absent, the key signature applies to all staves in the part. Key signatures appear at the start of each system unless the print-object attribute has been set to "no"."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='key']"


class XSDComplexTypeKeyAccidental(XSDComplexType):
    """The key-accidental type indicates the accidental to be displayed in a non-traditional key signature, represented in the same manner as the accidental type without the formatting attributes.

``simpleContent``: The accidental-value type represents notated accidentals supported by MusicXML. In the MusicXML 2.0 DTD this was a string with values that could be included. The XSD strengthens the data typing to an enumerated list. The quarter- and three-quarters- accidentals are Tartini-style quarter-tone accidentals. The -down and -up accidentals are quarter-tone accidentals that include arrows pointing down or up. The slash- accidentals are used in Turkish classical music. The numbered sharp and flat accidentals are superscripted versions of the accidental signs, used in Turkish folk music. The sori and koron accidentals are microtonal sharp and flat accidentals used in Iranian and Persian music. The other accidental covers accidentals other than those listed here. It is usually used in combination with the smufl attribute to specify a particular SMuFL accidental. The smufl attribute may be used with any accidental value to help specify the appearance of symbols that share the same MusicXML semantics.
    
    Permitted Values: ``'sharp'``, ``'natural'``, ``'flat'``, ``'double-sharp'``, ``'sharp-sharp'``, ``'flat-flat'``, ``'natural-sharp'``, ``'natural-flat'``, ``'quarter-flat'``, ``'quarter-sharp'``, ``'three-quarters-flat'``, ``'three-quarters-sharp'``, ``'sharp-down'``, ``'sharp-up'``, ``'natural-down'``, ``'natural-up'``, ``'flat-down'``, ``'flat-up'``, ``'double-sharp-down'``, ``'double-sharp-up'``, ``'flat-flat-down'``, ``'flat-flat-up'``, ``'arrow-down'``, ``'arrow-up'``, ``'triple-sharp'``, ``'triple-flat'``, ``'slash-quarter-sharp'``, ``'slash-sharp'``, ``'slash-flat'``, ``'double-slash-flat'``, ``'sharp-1'``, ``'sharp-2'``, ``'sharp-3'``, ``'sharp-5'``, ``'flat-1'``, ``'flat-2'``, ``'flat-3'``, ``'flat-4'``, ``'sori'``, ``'koron'``, ``'other'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeAccidentalValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='key-accidental']"


class XSDComplexTypeKeyOctave(XSDComplexType):
    """The key-octave type specifies in which octave an element of a key signature appears. The content specifies the octave value using the same values as the display-octave element. The number attribute is a positive integer that refers to the key signature element in left-to-right order. If the cancel attribute is set to yes, then this number refers to the canceling key signature specified by the cancel element in the parent key element. The cancel attribute cannot be set to yes if there is no corresponding cancel element within the parent key element. It is no by default.

``simpleContent``: Octaves are represented by the numbers 0 to 9, where 4 indicates the octave started by middle C."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeOctave
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='key-octave']"


class XSDComplexTypeLineDetail(XSDComplexType):
    """If the staff-lines element is present, the appearance of each line may be individually specified with a line-detail type. Staff lines are numbered from bottom to top. The print-object attribute allows lines to be hidden within a staff. This is used in special situations such as a widely-spaced percussion staff where a note placed below the higher line is distinct from a note placed above the lower line. Hidden staff lines are included when specifying clef lines and determining display-step / display-octave values, but are not counted as lines for the purposes of the system-layout and staff-layout elements."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='line-detail']"


class XSDComplexTypeMeasureRepeat(XSDComplexType):
    """The measure-repeat type is used for both single and multiple measure repeats. The text of the element indicates the number of measures to be repeated in a single pattern. The slashes attribute specifies the number of slashes to use in the repeat sign. It is 1 if not specified. The text of the element is ignored when the type is stop.

The stop type indicates the first measure where the repeats are no longer displayed. Both the start and the stop of the measure-repeat should be specified unless the repeats are displayed through the end of the part.

The measure-repeat element specifies a notation style for repetitions. The actual music being repeated needs to be repeated within each measure of the MusicXML file. This element specifies the notation that indicates the repeat."""
    
    _SIMPLE_CONTENT = XSDSimpleTypePositiveIntegerOrEmpty
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='measure-repeat']"


class XSDComplexTypeMeasureStyle(XSDComplexType):
    """A measure-style indicates a special way to print partial to multiple measures within a part. This includes multiple rests over several measures, repeats of beats, single, or multiple measures, and use of slash notation.

The multiple-rest and measure-repeat elements indicate the number of measures covered in the element content. The beat-repeat and slash elements can cover partial measures. All but the multiple-rest element use a type attribute to indicate starting and stopping the use of the style. The optional number attribute specifies the staff number from top to bottom on the system, as with clef."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='measure-style']"


class XSDComplexTypeMultipleRest(XSDComplexType):
    """The text of the multiple-rest type indicates the number of measures in the multiple rest. Multiple rests may use the 1-bar / 2-bar / 4-bar rest symbols, or a single shape. The use-symbols attribute indicates which to use; it is no if not specified."""
    
    _SIMPLE_CONTENT = XSDSimpleTypePositiveInteger
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='multiple-rest']"


class XSDComplexTypePartClef(XSDComplexType):
    """The child elements of the part-clef type have the same meaning as for the clef type. However that meaning applies to a transposed part created from the existing score file."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='part-clef']"


class XSDComplexTypePartSymbol(XSDComplexType):
    """The part-symbol type indicates how a symbol for a multi-staff part is indicated in the score; brace is the default value. The top-staff and bottom-staff attributes are used when the brace does not extend across the entire part. For example, in a 3-staff organ part, the top-staff will typically be 1 for the right hand, while the bottom-staff will typically be 2 for the left hand. Staff 3 for the pedals is usually outside the brace. By default, the presence of a part-symbol element that does not extend across the entire part also indicates a corresponding change in the common barlines within a part.

``simpleContent``: The group-symbol-value type indicates how the symbol for a group or multi-staff part is indicated in the score.
    
    Permitted Values: ``'none'``, ``'brace'``, ``'line'``, ``'bracket'``, ``'square'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeGroupSymbolValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='part-symbol']"


class XSDComplexTypePartTranspose(XSDComplexType):
    """The child elements of the part-transpose type have the same meaning as for the transpose type. However that meaning applies to a transposed part created from the existing score file."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='part-transpose']"


class XSDComplexTypeSlash(XSDComplexType):
    """The slash type is used to indicate that slash notation is to be used. If the slash is on every beat, use-stems is no (the default). To indicate rhythms but not pitches, use-stems is set to yes. The type attribute indicates whether this is the start or stop of a slash notation style. The use-dots attribute works as for the beat-repeat element, and only has effect if use-stems is no."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='slash']"


class XSDComplexTypeStaffDetails(XSDComplexType):
    """The staff-details element is used to indicate different types of staves. The optional number attribute specifies the staff number from top to bottom on the system, as with clef. The print-object attribute is used to indicate when a staff is not printed in a part, usually in large scores where empty parts are omitted. It is yes by default. If print-spacing is yes while print-object is no, the score is printed in cutaway format where vertical space is left for the empty part."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='staff-details']"


class XSDComplexTypeStaffSize(XSDComplexType):
    """The staff-size element indicates how large a staff space is on this staff, expressed as a percentage of the work's default scaling. Values less than 100 make the staff space smaller while values over 100 make the staff space larger. A staff-type of cue, ossia, or editorial implies a staff-size of less than 100, but the exact value is implementation-dependent unless specified here. Staff size affects staff height only, not the relationship of the staff to the left and right margins.

In some cases, a staff-size different than 100 also scales the notation on the staff, such as with a cue staff. In other cases, such as percussion staves, the lines may be more widely spaced without scaling the notation on the staff. The scaling attribute allows these two cases to be distinguished. It specifies the percentage scaling that applies to the notation. Values less that 100 make the notation smaller while values over 100 make the notation larger. The staff-size content and scaling attribute are both non-negative decimal values.

``simpleContent``: The non-negative-decimal type specifies a non-negative decimal value."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeNonNegativeDecimal
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='staff-size']"


class XSDComplexTypeStaffTuning(XSDComplexType):
    """The staff-tuning type specifies the open, non-capo tuning of the lines on a tablature staff."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='staff-tuning']"


class XSDComplexTypeTime(XSDComplexType):
    """Time signatures are represented by the beats element for the numerator and the beat-type element for the denominator. The symbol attribute is used to indicate common and cut time symbols as well as a single number display. Multiple pairs of beat and beat-type elements are used for composite time signatures with multiple denominators, such as 2/4 + 3/8. A composite such as 3+2/8 requires only one beat/beat-type pair.

The print-object attribute allows a time signature to be specified but not printed, as is the case for excerpts from the middle of a score. The value is "yes" if not present. The optional number attribute refers to staff numbers within the part. If absent, the time signature applies to all staves in the part."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='time']"


class XSDComplexTypeTranspose(XSDComplexType):
    """The transpose type represents what must be added to a written pitch to get a correct sounding pitch. The optional number attribute refers to staff numbers, from top to bottom on the system. If absent, the transposition applies to all staves in the part. Per-staff transposition is most often used in parts that represent multiple instruments."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='transpose']"


class XSDComplexTypeBarStyleColor(XSDComplexType):
    """The bar-style-color type contains barline style and color information.

``simpleContent``: The bar-style type represents barline style information. Choices are regular, dotted, dashed, heavy, light-light, light-heavy, heavy-light, heavy-heavy, tick (a short stroke through the top line), short (a partial barline between the 2nd and 4th lines), and none.
    
    Permitted Values: ``'regular'``, ``'dotted'``, ``'dashed'``, ``'heavy'``, ``'light-light'``, ``'light-heavy'``, ``'heavy-light'``, ``'heavy-heavy'``, ``'tick'``, ``'short'``, ``'none'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeBarStyle
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='bar-style-color']"


class XSDComplexTypeBarline(XSDComplexType):
    """If a barline is other than a normal single barline, it should be represented by a barline type that describes it. This includes information about repeats and multiple endings, as well as line style. Barline data is on the same level as the other musical data in a score - a child of a measure in a partwise score, or a part in a timewise score. This allows for barlines within measures, as in dotted barlines that subdivide measures in complex meters. The two fermata elements allow for fermatas on both sides of the barline (the lower one inverted).

Barlines have a location attribute to make it easier to process barlines independently of the other musical data in a score. It is often easier to set up measures separately from entering notes. The location attribute must match where the barline element occurs within the rest of the musical data in the score. If location is left, it should be the first element in the measure, aside from the print, bookmark, and link elements. If location is right, it should be the last element, again with the possible exception of the print, bookmark, and link elements. If no location is specified, the right barline is the default. The segno, coda, and divisions attributes work the same way as in the sound element. They are used for playback when barline elements contain segno or coda child elements."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='barline']"


class XSDComplexTypeEnding(XSDComplexType):
    """The ending type represents multiple (e.g. first and second) endings. Typically, the start type is associated with the left barline of the first measure in an ending. The stop and discontinue types are associated with the right barline of the last measure in an ending. Stop is used when the ending mark concludes with a downward jog, as is typical for first endings. Discontinue is used when there is no downward jog, as is typical for second endings that do not conclude a piece. The length of the jog can be specified using the end-length attribute. The text-x and text-y attributes are offsets that specify where the baseline of the start of the ending text appears, relative to the start of the ending line.

The number attribute indicates which times the ending is played, similar to the time-only attribute used by other elements. While this often represents the numeric values for what is under the ending line, it can also indicate whether an ending is played during a larger dal segno or da capo repeat. Single endings such as "1" or comma-separated multiple endings such as "1,2" may be used. The ending element text is used when the text displayed in the ending is different than what appears in the number attribute. The print-object attribute is used to indicate when an ending is present but not printed, as is often the case for many parts in a full score."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='ending']"


class XSDComplexTypeRepeat(XSDComplexType):
    """The repeat type represents repeat marks. The start of the repeat has a forward direction while the end of the repeat has a backward direction. The times and after-jump attributes are only used with backward repeats that are not part of an ending. The times attribute indicates the number of times the repeated section is played. The after-jump attribute indicates if the repeats are played after a jump due to a da capo or dal segno."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='repeat']"


class XSDComplexTypeAccord(XSDComplexType):
    """The accord type represents the tuning of a single string in the scordatura element. It uses the same group of elements as the staff-tuning element. Strings are numbered from high to low."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='accord']"


class XSDComplexTypeAccordionRegistration(XSDComplexType):
    """The accordion-registration type is used for accordion registration symbols. These are circular symbols divided horizontally into high, middle, and low sections that correspond to 4', 8', and 16' pipes. Each accordion-high, accordion-middle, and accordion-low element represents the presence of one or more dots in the registration diagram. An accordion-registration element needs to have at least one of the child elements present."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='accordion-registration']"


class XSDComplexTypeBarre(XSDComplexType):
    """The barre element indicates placing a finger over multiple strings on a single fret. The type is "start" for the lowest pitched string (e.g., the string with the highest MusicXML number) and is "stop" for the highest pitched string."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='barre']"


class XSDComplexTypeBass(XSDComplexType):
    """The bass type is used to indicate a bass note in popular music chord symbols, e.g. G/C. It is generally not used in functional harmony, as inversion is generally not used in pop chord symbols. As with root, it is divided into step and alter elements, similar to pitches. The arrangement attribute specifies where the bass is displayed relative to what precedes it."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='bass']"


class XSDComplexTypeHarmonyAlter(XSDComplexType):
    """The harmony-alter type represents the chromatic alteration of the root, numeral, or bass of the current harmony-chord group within the harmony element. In some chord styles, the text of the preceding element may include alteration information. In that case, the print-object attribute of this type can be set to no. The location attribute indicates whether the alteration should appear to the left or the right of the preceding element. Its default value varies by element.

``simpleContent``: The semitones type is a number representing semitones, used for chromatic alteration. A value of -1 corresponds to a flat and a value of 1 to a sharp. Decimal values like 0.5 (quarter tone sharp) are used for microtones."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeSemitones
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='harmony-alter']"


class XSDComplexTypeBassStep(XSDComplexType):
    """The bass-step type represents the pitch step of the bass of the current chord within the harmony element. The text attribute indicates how the bass should appear in a score if not using the element contents.

``simpleContent``: The step type represents a step of the diatonic scale, represented using the English letters A through G.
    
    Permitted Values: ``'A'``, ``'B'``, ``'C'``, ``'D'``, ``'E'``, ``'F'``, ``'G'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeStep
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='bass-step']"


class XSDComplexTypeBeater(XSDComplexType):
    """The beater type represents pictograms for beaters, mallets, and sticks that do not have different materials represented in the pictogram.

``simpleContent``: The beater-value type represents pictograms for beaters, mallets, and sticks that do not have different materials represented in the pictogram. The finger and hammer values are in addition to Stone's list.
    
    Permitted Values: ``'bow'``, ``'chime hammer'``, ``'coin'``, ``'drum stick'``, ``'finger'``, ``'fingernail'``, ``'fist'``, ``'guiro scraper'``, ``'hammer'``, ``'hand'``, ``'jazz stick'``, ``'knitting needle'``, ``'metal hammer'``, ``'slide brush on gong'``, ``'snare stick'``, ``'spoon mallet'``, ``'superball'``, ``'triangle beater'``, ``'triangle beater plain'``, ``'wire brush'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeBeaterValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='beater']"


class XSDComplexTypeBeatUnitTied(XSDComplexType):
    """The beat-unit-tied type indicates a beat-unit within a metronome mark that is tied to the preceding beat-unit. This allows two or more tied notes to be associated with a per-minute value in a metronome mark, whereas the metronome-tied element is restricted to metric relationship marks."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='beat-unit-tied']"


class XSDComplexTypeBracket(XSDComplexType):
    """Brackets are combined with words in a variety of modern directions. The line-end attribute specifies if there is a jog up or down (or both), an arrow, or nothing at the start or end of the bracket. If the line-end is up or down, the length of the jog can be specified using the end-length attribute. The line-type is solid if not specified."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='bracket']"


class XSDComplexTypeDashes(XSDComplexType):
    """The dashes type represents dashes, used for instance with cresc. and dim. marks."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='dashes']"


class XSDComplexTypeDegree(XSDComplexType):
    """The degree type is used to add, alter, or subtract individual notes in the chord. The print-object attribute can be used to keep the degree from printing separately when it has already taken into account in the text attribute of the kind element. The degree-value and degree-type text attributes specify how the value and type of the degree should be displayed.

A harmony of kind "other" can be spelled explicitly by using a series of degree elements together with a root."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='degree']"


class XSDComplexTypeDegreeAlter(XSDComplexType):
    """The degree-alter type represents the chromatic alteration for the current degree. If the degree-type value is alter or subtract, the degree-alter value is relative to the degree already in the chord based on its kind element. If the degree-type value is add, the degree-alter is relative to a dominant chord (major and perfect intervals except for a minor seventh). The plus-minus attribute is used to indicate if plus and minus symbols should be used instead of sharp and flat symbols to display the degree alteration. It is no if not specified.

``simpleContent``: The semitones type is a number representing semitones, used for chromatic alteration. A value of -1 corresponds to a flat and a value of 1 to a sharp. Decimal values like 0.5 (quarter tone sharp) are used for microtones."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeSemitones
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='degree-alter']"


class XSDComplexTypeDegreeType(XSDComplexType):
    """The degree-type type indicates if this degree is an addition, alteration, or subtraction relative to the kind of the current chord. The value of the degree-type element affects the interpretation of the value of the degree-alter element. The text attribute specifies how the type of the degree should be displayed.

``simpleContent``: The degree-type-value type indicates whether the current degree element is an addition, alteration, or subtraction to the kind of the current chord in the harmony element.
    
    Permitted Values: ``'add'``, ``'alter'``, ``'subtract'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeDegreeTypeValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='degree-type']"


class XSDComplexTypeDegreeValue(XSDComplexType):
    """The content of the degree-value type is a number indicating the degree of the chord (1 for the root, 3 for third, etc). The text attribute specifies how the value of the degree should be displayed. The symbol attribute indicates that a symbol should be used in specifying the degree. If the symbol attribute is present, the value of the text attribute follows the symbol."""
    
    _SIMPLE_CONTENT = XSDSimpleTypePositiveInteger
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='degree-value']"


class XSDComplexTypeDirection(XSDComplexType):
    """A direction is a musical indication that is not necessarily attached to a specific note. Two or more may be combined to indicate words followed by the start of a dashed line, the end of a wedge followed by dynamics, etc. For applications where a specific direction is indeed attached to a specific note, the direction element can be associated with the first note element that follows it in score order that is not in a different voice.

By default, a series of direction-type elements and a series of child elements of a direction-type within a single direction element follow one another in sequence visually. For a series of direction-type children, non-positional formatting attributes are carried over from the previous element by default."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='direction']"


class XSDComplexTypeDirectionType(XSDComplexType):
    """Textual direction types may have more than 1 component due to multiple fonts. The dynamics element may also be used in the notations element. Attribute groups related to print suggestions apply to the individual direction-type, not to the overall direction."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='direction-type']"


class XSDComplexTypeEffect(XSDComplexType):
    """The effect type represents pictograms for sound effect percussion instruments. The smufl attribute is used to distinguish different SMuFL stylistic alternates.

``simpleContent``: The effect-value type represents pictograms for sound effect percussion instruments. The cannon, lotus flute, and megaphone values are in addition to Stone's list.
    
    Permitted Values: ``'anvil'``, ``'auto horn'``, ``'bird whistle'``, ``'cannon'``, ``'duck call'``, ``'gun shot'``, ``'klaxon horn'``, ``'lions roar'``, ``'lotus flute'``, ``'megaphone'``, ``'police whistle'``, ``'siren'``, ``'slide whistle'``, ``'thunder sheet'``, ``'wind machine'``, ``'wind whistle'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeEffectValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='effect']"


class XSDComplexTypeFeature(XSDComplexType):
    """The feature type is a part of the grouping element used for musical analysis. The type attribute represents the type of the feature and the element content represents its value. This type is flexible to allow for different analyses."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='feature']"


class XSDComplexTypeFirstFret(XSDComplexType):
    """The first-fret type indicates which fret is shown in the top space of the frame; it is fret 1 if the element is not present. The optional text attribute indicates how this is represented in the fret diagram, while the location attribute indicates whether the text appears to the left or right of the frame."""
    
    _SIMPLE_CONTENT = XSDSimpleTypePositiveInteger
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='first-fret']"


class XSDComplexTypeFrame(XSDComplexType):
    """The frame type represents a frame or fretboard diagram used together with a chord symbol. The representation is based on the NIFF guitar grid with additional information. The frame type's unplayed attribute indicates what to display above a string that has no associated frame-note element. Typical values are x and the empty string. If the attribute is not present, the display of the unplayed string is application-defined."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='frame']"


class XSDComplexTypeFrameNote(XSDComplexType):
    """The frame-note type represents each note included in the frame. An open string will have a fret value of 0, while a muted string will not be associated with a frame-note element."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='frame-note']"


class XSDComplexTypeGlass(XSDComplexType):
    """The glass type represents pictograms for glass percussion instruments. The smufl attribute is used to distinguish different SMuFL glyphs for wind chimes in the Chimes pictograms range, including those made of materials other than glass.

``simpleContent``: The glass-value type represents pictograms for glass percussion instruments.
    
    Permitted Values: ``'glass harmonica'``, ``'glass harp'``, ``'wind chimes'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeGlassValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='glass']"


class XSDComplexTypeGrouping(XSDComplexType):
    """The grouping type is used for musical analysis. When the type attribute is "start" or "single", it usually contains one or more feature elements. The number attribute is used for distinguishing between overlapping and hierarchical groupings. The member-of attribute allows for easy distinguishing of what grouping elements are in what hierarchy. Feature elements contained within a "stop" type of grouping may be ignored.

This element is flexible to allow for different types of analyses. Future versions of the MusicXML format may add elements that can represent more standardized categories of analysis data, allowing for easier data sharing."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='grouping']"


class XSDComplexTypeHarmony(XSDComplexType):
    """The harmony type represents harmony analysis, including chord symbols in popular music as well as functional harmony analysis in classical music.

If there are alternate harmonies possible, this can be specified using multiple harmony elements differentiated by type. Explicit harmonies have all note present in the music; implied have some notes missing but implied; alternate represents alternate analyses.

The print-object attribute controls whether or not anything is printed due to the harmony element. The print-frame attribute controls printing of a frame or fretboard diagram. The print-style attribute group sets the default for the harmony, but individual elements can override this with their own print-style values. The arrangement attribute specifies how multiple harmony-chord groups are arranged relative to each other. Harmony-chords with vertical arrangement are separated by horizontal lines. Harmony-chords with diagonal or horizontal arrangement are separated by diagonal lines or slashes."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='harmony']"


class XSDComplexTypeHarpPedals(XSDComplexType):
    """The harp-pedals type is used to create harp pedal diagrams. The pedal-step and pedal-alter elements use the same values as the step and alter elements. For easiest reading, the pedal-tuning elements should follow standard harp pedal order, with pedal-step values of D, C, B, E, F, G, and A."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='harp-pedals']"


class XSDComplexTypeImage(XSDComplexType):
    """The image type is used to include graphical images in a score."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='image']"


class XSDComplexTypeInstrumentChange(XSDComplexType):
    """The instrument-change element type represents a change to the virtual instrument sound for a given score-instrument. The id attribute refers to the score-instrument affected by the change. All instrument-change child elements can also be initially specified within the score-instrument element."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='instrument-change']"


class XSDComplexTypeInversion(XSDComplexType):
    """The inversion type represents harmony inversions. The value is a number indicating which inversion is used: 0 for root position, 1 for first inversion, etc.  The text attribute indicates how the inversion should be displayed in a score."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeNonNegativeInteger
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='inversion']"


class XSDComplexTypeKind(XSDComplexType):
    """Kind indicates the type of chord. Degree elements can then add, subtract, or alter from these starting points

The attributes are used to indicate the formatting of the symbol. Since the kind element is the constant in all the harmony-chord groups that can make up a polychord, many formatting attributes are here.

The use-symbols attribute is yes if the kind should be represented when possible with harmony symbols rather than letters and numbers. These symbols include:

	major: a triangle, like Unicode 25B3
	minor: -, like Unicode 002D
	augmented: +, like Unicode 002B
	diminished: °, like Unicode 00B0
	half-diminished: ø, like Unicode 00F8

For the major-minor kind, only the minor symbol is used when use-symbols is yes. The major symbol is set using the symbol attribute in the degree-value element. The corresponding degree-alter value will usually be 0 in this case.

The text attribute describes how the kind should be spelled in a score. If use-symbols is yes, the value of the text attribute follows the symbol. The stack-degrees attribute is yes if the degree elements should be stacked above each other. The parentheses-degrees attribute is yes if all the degrees should be in parentheses. The bracket-degrees attribute is yes if all the degrees should be in a bracket. If not specified, these values are implementation-specific. The alignment attributes are for the entire harmony-chord group of which this kind element is a part.

The text attribute may use strings such as "13sus" that refer to both the kind and one or more degree elements. In this case, the corresponding degree elements should have the print-object attribute set to "no" to keep redundant alterations from being displayed.

``simpleContent``: A kind-value indicates the type of chord. Degree elements can then add, subtract, or alter from these starting points. Values include:

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

The "other" kind is used when the harmony is entirely composed of add elements.

The "none" kind is used to explicitly encode absence of chords or functional harmony. In this case, the root, numeral, or function element has no meaning. When using the root or numeral element, the root-step or numeral-step text attribute should be set to the empty string to keep the root or numeral from being displayed.
    
    Permitted Values: ``'major'``, ``'minor'``, ``'augmented'``, ``'diminished'``, ``'dominant'``, ``'major-seventh'``, ``'minor-seventh'``, ``'diminished-seventh'``, ``'augmented-seventh'``, ``'half-diminished'``, ``'major-minor'``, ``'major-sixth'``, ``'minor-sixth'``, ``'dominant-ninth'``, ``'major-ninth'``, ``'minor-ninth'``, ``'dominant-11th'``, ``'major-11th'``, ``'minor-11th'``, ``'dominant-13th'``, ``'major-13th'``, ``'minor-13th'``, ``'suspended-second'``, ``'suspended-fourth'``, ``'Neapolitan'``, ``'Italian'``, ``'French'``, ``'German'``, ``'pedal'``, ``'power'``, ``'Tristan'``, ``'other'``, ``'none'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeKindValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='kind']"


class XSDComplexTypeListening(XSDComplexType):
    """The listen and listening types, new in Version 4.0, specify different ways that a score following or machine listening application can interact with a performer. The listening type handles interactions that change the state of the listening application from the specified point in the performance onward. If multiple child elements of the same type are present, they should have distinct player and/or time-only attributes.

The offset element is used to indicate that the listening change takes place offset from the current score position. If the listening element is a child of a direction element, the listening offset element overrides the direction offset element if both elements are present. Note that the offset reflects the intended musical position for the change in state. It should not be used to compensate for latency issues in particular hardware configurations."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='listening']"


class XSDComplexTypeMeasureNumbering(XSDComplexType):
    """The measure-numbering type describes how frequently measure numbers are displayed on this part. The text attribute from the measure element is used for display, or the number attribute if the text attribute is not present. Measures with an implicit attribute set to "yes" never display a measure number, regardless of the measure-numbering setting.

The optional staff attribute refers to staff numbers within the part, from top to bottom on the system. It indicates which staff is used as the reference point for vertical positioning. A value of 1 is assumed if not present.

The optional multiple-rest-always and multiple-rest-range attributes describe how measure numbers are shown on multiple rests when the measure-numbering value is not set to none. The multiple-rest-always attribute is set to yes when the measure number should always be shown, even if the multiple rest starts midway through a system when measure numbering is set to system level. The multiple-rest-range attribute is set to yes when measure numbers on multiple rests display the range of numbers for the first and last measure, rather than just the number of the first measure.

``simpleContent``: The measure-numbering-value type describes how measure numbers are displayed on this part: no numbers, numbers every measure, or numbers every system.
    
    Permitted Values: ``'none'``, ``'measure'``, ``'system'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeMeasureNumberingValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='measure-numbering']"


class XSDComplexTypeMembrane(XSDComplexType):
    """The membrane type represents pictograms for membrane percussion instruments. The smufl attribute is used to distinguish different SMuFL stylistic alternates.

``simpleContent``: The membrane-value type represents pictograms for membrane percussion instruments.
    
    Permitted Values: ``'bass drum'``, ``'bass drum on side'``, ``'bongos'``, ``'Chinese tomtom'``, ``'conga drum'``, ``'cuica'``, ``'goblet drum'``, ``'Indo-American tomtom'``, ``'Japanese tomtom'``, ``'military drum'``, ``'snare drum'``, ``'snare drum snares off'``, ``'tabla'``, ``'tambourine'``, ``'tenor drum'``, ``'timbales'``, ``'tomtom'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeMembraneValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='membrane']"


class XSDComplexTypeMetal(XSDComplexType):
    """The metal type represents pictograms for metal percussion instruments. The smufl attribute is used to distinguish different SMuFL stylistic alternates.

``simpleContent``: The metal-value type represents pictograms for metal percussion instruments. The hi-hat value refers to a pictogram like Stone's high-hat cymbals but without the long vertical line at the bottom.
    
    Permitted Values: ``'agogo'``, ``'almglocken'``, ``'bell'``, ``'bell plate'``, ``'bell tree'``, ``'brake drum'``, ``'cencerro'``, ``'chain rattle'``, ``'Chinese cymbal'``, ``'cowbell'``, ``'crash cymbals'``, ``'crotale'``, ``'cymbal tongs'``, ``'domed gong'``, ``'finger cymbals'``, ``'flexatone'``, ``'gong'``, ``'hi-hat'``, ``'high-hat cymbals'``, ``'handbell'``, ``'jaw harp'``, ``'jingle bells'``, ``'musical saw'``, ``'shell bells'``, ``'sistrum'``, ``'sizzle cymbal'``, ``'sleigh bells'``, ``'suspended cymbal'``, ``'tam tam'``, ``'tam tam with beater'``, ``'triangle'``, ``'Vietnamese hat'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeMetalValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='metal']"


class XSDComplexTypeMetronome(XSDComplexType):
    """The metronome type represents metronome marks and other metric relationships. The beat-unit group and per-minute element specify regular metronome marks. The metronome-note and metronome-relation elements allow for the specification of metric modulations and other metric relationships, such as swing tempo marks where two eighths are equated to a quarter note / eighth note triplet. Tied notes can be represented in both types of metronome marks by using the beat-unit-tied and metronome-tied elements. The parentheses attribute indicates whether or not to put the metronome mark in parentheses; its value is no if not specified. The print-object attribute is set to no in cases where the metronome element represents a relationship or range that is not displayed in the music notation."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='metronome']"


class XSDComplexTypeMetronomeBeam(XSDComplexType):
    """The metronome-beam type works like the beam type in defining metric relationships, but does not include all the attributes available in the beam type.

``simpleContent``: The beam-value type represents the type of beam associated with each of 8 beam levels (up to 1024th notes) available for each note.
    
    Permitted Values: ``'begin'``, ``'continue'``, ``'end'``, ``'forward hook'``, ``'backward hook'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeBeamValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='metronome-beam']"


class XSDComplexTypeMetronomeNote(XSDComplexType):
    """The metronome-note type defines the appearance of a note within a metric relationship mark."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='metronome-note']"


class XSDComplexTypeMetronomeTied(XSDComplexType):
    """The metronome-tied indicates the presence of a tie within a metric relationship mark. As with the tied element, both the start and stop of the tie should be specified, in this case within separate metronome-note elements."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='metronome-tied']"


class XSDComplexTypeMetronomeTuplet(XSDComplexType):
    """The metronome-tuplet type uses the same element structure as the time-modification element along with some attributes from the tuplet element."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='metronome-tuplet']"


class XSDComplexTypeNumeral(XSDComplexType):
    """The numeral type represents the Roman numeral or Nashville number part of a harmony. It requires that the key be specified in the encoding, either with a key or numeral-key element."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='numeral']"


class XSDComplexTypeNumeralKey(XSDComplexType):
    """The numeral-key type is used when the key for the numeral is different than the key specified by the key signature. The numeral-fifths element specifies the key in the same way as the fifths element. The numeral-mode element specifies the mode similar to the mode element, but with a restricted set of values"""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='numeral-key']"


class XSDComplexTypeNumeralRoot(XSDComplexType):
    """The numeral-root type represents the Roman numeral or Nashville number as a positive integer from 1 to 7. The text attribute indicates how the numeral should appear in the score. A numeral-root value of 5 with a kind of major would have a text attribute of "V" if displayed as a Roman numeral, and "5" if displayed as a Nashville number. If the text attribute is not specified, the display is application-dependent.

``simpleContent``: The numeral-value type represents a Roman numeral or Nashville number value as a positive integer from 1 to 7."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeNumeralValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='numeral-root']"


class XSDComplexTypeOctaveShift(XSDComplexType):
    """The octave shift type indicates where notes are shifted up or down from their true pitched values because of printing difficulty. Thus a treble clef line noted with 8va will be indicated with an octave-shift down from the pitch data indicated in the notes. A size of 8 indicates one octave; a size of 15 indicates two octaves."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='octave-shift']"


class XSDComplexTypeOffset(XSDComplexType):
    """An offset is represented in terms of divisions, and indicates where the direction will appear relative to the current musical location. The current musical location is always within the current measure, even at the end of a measure.

The offset affects the visual appearance of the direction. If the sound attribute is "yes", then the offset affects playback and listening too. If the sound attribute is "no", then any sound or listening associated with the direction takes effect at the current location. The sound attribute is "no" by default for compatibility with earlier versions of the MusicXML format. If an element within a direction includes a default-x attribute, the offset value will be ignored when determining the appearance of that element.

``simpleContent``: The divisions type is used to express values in terms of the musical divisions defined by the divisions element. It is preferred that these be integer values both for MIDI interoperability and to avoid roundoff errors."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeDivisions
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='offset']"


class XSDComplexTypeOtherDirection(XSDComplexType):
    """The other-direction type is used to define any direction symbols not yet in the MusicXML format. The smufl attribute can be used to specify a particular direction symbol, allowing application interoperability without requiring every SMuFL glyph to have a MusicXML element equivalent. Using the other-direction type without the smufl attribute allows for extended representation, though without application interoperability."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='other-direction']"


class XSDComplexTypeOtherListening(XSDComplexType):
    """The other-listening type represents other types of listening control and interaction. The required type attribute indicates the type of listening to which the element content applies. The optional player and time-only attributes restrict the element to apply to a single player or set of times through a repeated section, respectively."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='other-listening']"


class XSDComplexTypePedal(XSDComplexType):
    """The pedal type represents piano pedal marks, including damper and sostenuto pedal marks. The line attribute is yes if pedal lines are used. The sign attribute is yes if Ped, Sost, and * signs are used. For compatibility with older versions, the sign attribute is yes by default if the line attribute is no, and is no by default if the line attribute is yes. If the sign attribute is set to yes and the type is start or sostenuto, the abbreviated attribute is yes if the short P and S signs are used, and no if the full Ped and Sost signs are used. It is no by default. Otherwise the abbreviated attribute is ignored. The alignment attributes are ignored if the sign attribute is no."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='pedal']"


class XSDComplexTypePedalTuning(XSDComplexType):
    """The pedal-tuning type specifies the tuning of a single harp pedal."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='pedal-tuning']"


class XSDComplexTypePerMinute(XSDComplexType):
    """The per-minute type can be a number, or a text description including numbers. If a font is specified, it overrides the font specified for the overall metronome element. This allows separate specification of a music font for the beat-unit and a text font for the numeric value, in cases where a single metronome font is not used."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='per-minute']"


class XSDComplexTypePercussion(XSDComplexType):
    """The percussion element is used to define percussion pictogram symbols. Definitions for these symbols can be found in Kurt Stone's "Music Notation in the Twentieth Century" on pages 206-212 and 223. Some values are added to these based on how usage has evolved in the 30 years since Stone's book was published."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='percussion']"


class XSDComplexTypePitched(XSDComplexType):
    """The pitched-value type represents pictograms for pitched percussion instruments. The smufl attribute is used to distinguish different SMuFL glyphs for a particular pictogram within the Tuned mallet percussion pictograms range.

``simpleContent``: The pitched-value type represents pictograms for pitched percussion instruments. The chimes and tubular chimes values distinguish the single-line and double-line versions of the pictogram.
    
    Permitted Values: ``'celesta'``, ``'chimes'``, ``'glockenspiel'``, ``'lithophone'``, ``'mallet'``, ``'marimba'``, ``'steel drums'``, ``'tubaphone'``, ``'tubular chimes'``, ``'vibraphone'``, ``'xylophone'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypePitchedValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='pitched']"


class XSDComplexTypePrincipalVoice(XSDComplexType):
    """The principal-voice type represents principal and secondary voices in a score, either for analysis or for square bracket symbols that appear in a score. The element content is used for analysis and may be any text value. The symbol attribute indicates the type of symbol used. When used for analysis separate from any printed score markings, it should be set to none. Otherwise if the type is stop it should be set to plain."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='principal-voice']"


class XSDComplexTypePrint(XSDComplexType):
    """The print type contains general printing parameters, including layout elements. The part-name-display and part-abbreviation-display elements may also be used here to change how a part name or abbreviation is displayed over the course of a piece. They take effect when the current measure or a succeeding measure starts a new system.

Layout group elements in a print element only apply to the current page, system, or staff. Music that follows continues to take the default values from the layout determined by the defaults element."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='print']"


class XSDComplexTypeRoot(XSDComplexType):
    """The root type indicates a pitch like C, D, E vs. a scale degree like 1, 2, 3. It is used with chord symbols in popular music. The root element has a root-step and optional root-alter element similar to the step and alter elements, but renamed to distinguish the different musical meanings."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='root']"


class XSDComplexTypeRootStep(XSDComplexType):
    """The root-step type represents the pitch step of the root of the current chord within the harmony element. The text attribute indicates how the root should appear in a score if not using the element contents.

``simpleContent``: The step type represents a step of the diatonic scale, represented using the English letters A through G.
    
    Permitted Values: ``'A'``, ``'B'``, ``'C'``, ``'D'``, ``'E'``, ``'F'``, ``'G'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeStep
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='root-step']"


class XSDComplexTypeScordatura(XSDComplexType):
    """Scordatura string tunings are represented by a series of accord elements, similar to the staff-tuning elements. Strings are numbered from high to low."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='scordatura']"


class XSDComplexTypeSound(XSDComplexType):
    """The sound element contains general playback parameters. They can stand alone within a part/measure, or be a component element within a direction.

Tempo is expressed in quarter notes per minute. If 0, the sound-generating program should prompt the user at the time of compiling a sound (MIDI) file.

Dynamics (or MIDI velocity) are expressed as a percentage of the default forte value (90 for MIDI 1.0).

Dacapo indicates to go back to the beginning of the movement. When used it always has the value "yes".

Segno and dalsegno are used for backwards jumps to a segno sign; coda and tocoda are used for forward jumps to a coda sign. If there are multiple jumps, the value of these parameters can be used to name and distinguish them. If segno or coda is used, the divisions attribute can also be used to indicate the number of divisions per quarter note. Otherwise sound and MIDI generating programs may have to recompute this.

By default, a dalsegno or dacapo attribute indicates that the jump should occur the first time through, while a tocoda attribute indicates the jump should occur the second time through. The time that jumps occur can be changed by using the time-only attribute.

The forward-repeat attribute indicates that a forward repeat sign is implied but not displayed. It is used for example in two-part forms with repeats, such as a minuet and trio where no repeat is displayed at the start of the trio. This usually occurs after a barline. When used it always has the value of "yes".

The fine attribute follows the final note or rest in a movement with a da capo or dal segno direction. If numeric, the value represents the actual duration of the final note or rest, which can be ambiguous in written notation and different among parts and voices. The value may also be "yes" to indicate no change to the final duration.

If the sound element applies only particular times through a repeat, the time-only attribute indicates which times to apply the sound element.

Pizzicato in a sound element effects all following notes. Yes indicates pizzicato, no indicates arco.

The pan and elevation attributes are deprecated in Version 2.0. The pan and elevation elements in the midi-instrument element should be used instead. The meaning of the pan and elevation attributes is the same as for the pan and elevation elements. If both are present, the mid-instrument elements take priority.

The damper-pedal, soft-pedal, and sostenuto-pedal attributes effect playback of the three common piano pedals and their MIDI controller equivalents. The yes value indicates the pedal is depressed; no indicates the pedal is released. A numeric value from 0 to 100 may also be used for half pedaling. This value is the percentage that the pedal is depressed. A value of 0 is equivalent to no, and a value of 100 is equivalent to yes.

Instrument changes, MIDI devices, MIDI instruments, and playback techniques are changed using the instrument-change, midi-device, midi-instrument, and play elements. When there are multiple instances of these elements, they should be grouped together by instrument using the id attribute values.

The offset element is used to indicate that the sound takes place offset from the current score position. If the sound element is a child of a direction element, the sound offset element overrides the direction offset element if both elements are present. Note that the offset reflects the intended musical position for the change in sound. It should not be used to compensate for latency issues in particular hardware configurations."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='sound']"


class XSDComplexTypeStaffDivide(XSDComplexType):
    """The staff-divide element represents the staff division arrow symbols found at SMuFL code points U+E00B, U+E00C, and U+E00D."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='staff-divide']"


class XSDComplexTypeStick(XSDComplexType):
    """The stick type represents pictograms where the material of the stick, mallet, or beater is included.The parentheses and dashed-circle attributes indicate the presence of these marks around the round beater part of a pictogram. Values for these attributes are "no" if not present."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='stick']"


class XSDComplexTypeStringMute(XSDComplexType):
    """The string-mute type represents string mute on and mute off symbols."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='string-mute']"


class XSDComplexTypeSwing(XSDComplexType):
    """The swing element specifies whether or not to use swing playback, where consecutive on-beat / off-beat eighth or 16th notes are played with unequal nominal durations. 

The straight element specifies that no swing is present, so consecutive notes have equal durations.

The first and second elements are positive integers that specify the ratio between durations of consecutive notes. For example, a first element with a value of 2 and a second element with a value of 1 applied to eighth notes specifies a quarter note / eighth note tuplet playback, where the first note is twice as long as the second note. Ratios should be specified with the smallest integers possible. For example, a ratio of 6 to 4 should be specified as 3 to 2 instead.

The optional swing-type element specifies the note type, either eighth or 16th, to which the ratio is applied. The value is eighth if this element is not present.

The optional swing-style element is a string describing the style of swing used.

The swing element has no effect for playback of grace notes, notes where a type element is not present, and notes where the specified duration is different than the nominal value associated with the specified type. If a swung note has attack and release attributes, those values modify the swung playback."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='swing']"


class XSDComplexTypeSync(XSDComplexType):
    """The sync type specifies the style that a score following application should use the synchronize an accompaniment with a performer. If this type is not included in a score, default synchronization depends on the application.

The optional latency attribute specifies a time in milliseconds that the listening application should expect from the performer. The optional player and time-only attributes restrict the element to apply to a single player or set of times through a repeated section, respectively."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='sync']"


class XSDComplexTypeTimpani(XSDComplexType):
    """The timpani type represents the timpani pictogram. The smufl attribute is used to distinguish different SMuFL stylistic alternates."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='timpani']"


class XSDComplexTypeWedge(XSDComplexType):
    """The wedge type represents crescendo and diminuendo wedge symbols. The type attribute is crescendo for the start of a wedge that is closed at the left side, and diminuendo for the start of a wedge that is closed on the right side. Spread values are measured in tenths; those at the start of a crescendo wedge or end of a diminuendo wedge are ignored. The niente attribute is yes if a circle appears at the point of the wedge, indicating a crescendo from nothing or diminuendo to nothing. It is no by default, and used only when the type is crescendo, or the type is stop for a wedge that began with a diminuendo type. The line-type is solid if not specified."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='wedge']"


class XSDComplexTypeWood(XSDComplexType):
    """The wood type represents pictograms for wood percussion instruments. The smufl attribute is used to distinguish different SMuFL stylistic alternates.

``simpleContent``: The wood-value type represents pictograms for wood percussion instruments. The maraca and maracas values distinguish the one- and two-maraca versions of the pictogram.
    
    Permitted Values: ``'bamboo scraper'``, ``'board clapper'``, ``'cabasa'``, ``'castanets'``, ``'castanets with handle'``, ``'claves'``, ``'football rattle'``, ``'guiro'``, ``'log drum'``, ``'maraca'``, ``'maracas'``, ``'quijada'``, ``'rainstick'``, ``'ratchet'``, ``'reco-reco'``, ``'sandpaper blocks'``, ``'slit drum'``, ``'temple block'``, ``'vibraslap'``, ``'whip'``, ``'wood block'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeWoodValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='wood']"


class XSDComplexTypeEncoding(XSDComplexType):
    """The encoding element contains information about who did the digital encoding, when, with what software, and in what aspects. Standard type values for the encoder element are music, words, and arrangement, but other types may be used. The type attribute is only needed when there are multiple encoder elements."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='encoding']"


class XSDComplexTypeIdentification(XSDComplexType):
    """Identification contains basic metadata about the score. It includes information that may apply at a score-wide, movement-wide, or part-wide level. The creator, rights, source, and relation elements are based on Dublin Core."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='identification']"


class XSDComplexTypeMiscellaneous(XSDComplexType):
    """If a program has other metadata not yet supported in the MusicXML format, it can go in the miscellaneous element. The miscellaneous type puts each separate part of metadata into its own miscellaneous-field type."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='miscellaneous']"


class XSDComplexTypeMiscellaneousField(XSDComplexType):
    """If a program has other metadata not yet supported in the MusicXML format, each type of metadata can go in a miscellaneous-field element. The required name attribute indicates the type of metadata the element content represents."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='miscellaneous-field']"


class XSDComplexTypeSupports(XSDComplexType):
    """The supports type indicates if a MusicXML encoding supports a particular MusicXML element. This is recommended for elements like beam, stem, and accidental, where the absence of an element is ambiguous if you do not know if the encoding supports that element. For Version 2.0, the supports element is expanded to allow programs to indicate support for particular attributes or particular values. This lets applications communicate, for example, that all system and/or page breaks are contained in the MusicXML file."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='supports']"


class XSDComplexTypeAppearance(XSDComplexType):
    """The appearance type controls general graphical settings for the music's final form appearance on a printed page of display. This includes support for line widths, definitions for note sizes, and standard distances between notation elements, plus an extension element for other aspects of appearance."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='appearance']"


class XSDComplexTypeDistance(XSDComplexType):
    """The distance element represents standard distances between notation elements in tenths. The type attribute defines what type of distance is being defined. Valid values include hyphen (for hyphens in lyrics) and beam.

``simpleContent``: The tenths type is a number representing tenths of interline staff space (positive or negative). Both integer and decimal values are allowed, such as 5 for a half space and 2.5 for a quarter space. Interline space is measured from the middle of a staff line.

Distances in a MusicXML file are measured in tenths of staff space. Tenths are then scaled to millimeters within the scaling element, used in the defaults element at the start of a score. Individual staves can apply a scaling factor to adjust staff size. When a MusicXML element or attribute refers to tenths, it means the global tenths defined by the scaling element, not the local tenths as adjusted by the staff-size element."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeTenths
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='distance']"


class XSDComplexTypeGlyph(XSDComplexType):
    """The glyph element represents what SMuFL glyph should be used for different variations of symbols that are semantically identical. The type attribute specifies what type of glyph is being defined. The element value specifies what SMuFL glyph to use, including recommended stylistic alternates. The SMuFL glyph name should match the type. For instance, a type of quarter-rest would use values restQuarter, restQuarterOld, or restQuarterZ. A type of g-clef-ottava-bassa would use values gClef8vb, gClef8vbOld, or gClef8vbCClef. A type of octave-shift-up-8 would use values ottava, ottavaBassa, ottavaBassaBa, ottavaBassaVb, or octaveBassa.

``simpleContent``: The smufl-glyph-name type is used for attributes that reference a specific Standard Music Font Layout (SMuFL) character. The value is a SMuFL canonical glyph name, not a code point. For instance, the value for a standard piano pedal mark would be keyboardPedalPed, not U+E650."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeSmuflGlyphName
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='glyph']"


class XSDComplexTypeLineWidth(XSDComplexType):
    """The line-width type indicates the width of a line type in tenths. The type attribute defines what type of line is being defined. Values include beam, bracket, dashes, enclosure, ending, extend, heavy barline, leger, light barline, octave shift, pedal, slur middle, slur tip, staff, stem, tie middle, tie tip, tuplet bracket, and wedge. The text content is expressed in tenths.

``simpleContent``: The tenths type is a number representing tenths of interline staff space (positive or negative). Both integer and decimal values are allowed, such as 5 for a half space and 2.5 for a quarter space. Interline space is measured from the middle of a staff line.

Distances in a MusicXML file are measured in tenths of staff space. Tenths are then scaled to millimeters within the scaling element, used in the defaults element at the start of a score. Individual staves can apply a scaling factor to adjust staff size. When a MusicXML element or attribute refers to tenths, it means the global tenths defined by the scaling element, not the local tenths as adjusted by the staff-size element."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeTenths
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='line-width']"


class XSDComplexTypeMeasureLayout(XSDComplexType):
    """The measure-layout type includes the horizontal distance from the previous measure. It applies to the current measure only."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='measure-layout']"


class XSDComplexTypeNoteSize(XSDComplexType):
    """The note-size type indicates the percentage of the regular note size to use for notes with a cue and large size as defined in the type element. The grace type is used for notes of cue size that that include a grace element. The cue type is used for all other notes with cue size, whether defined explicitly or implicitly via a cue element. The large type is used for notes of large size. The text content represent the numeric percentage. A value of 100 would be identical to the size of a regular note as defined by the music font.

``simpleContent``: The non-negative-decimal type specifies a non-negative decimal value."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeNonNegativeDecimal
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='note-size']"


class XSDComplexTypeOtherAppearance(XSDComplexType):
    """The other-appearance type is used to define any graphical settings not yet in the current version of the MusicXML format. This allows extended representation, though without application interoperability."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='other-appearance']"


class XSDComplexTypePageLayout(XSDComplexType):
    """Page layout can be defined both in score-wide defaults and in the print element. Page margins are specified either for both even and odd pages, or via separate odd and even page number values. The type is not needed when used as part of a print element. If omitted when used in the defaults element, "both" is the default.

If no page-layout element is present in the defaults element, default page layout values are chosen by the application.

When used in the print element, the page-layout element affects the appearance of the current page only. All other pages use the default values as determined by the defaults element. If any child elements are missing from the page-layout element in a print element, the values determined by the defaults element are used there as well."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='page-layout']"


class XSDComplexTypePageMargins(XSDComplexType):
    """Page margins are specified either for both even and odd pages, or via separate odd and even page number values. The type attribute is not needed when used as part of a print element. If omitted when the page-margins type is used in the defaults element, "both" is the default value."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='page-margins']"


class XSDComplexTypeScaling(XSDComplexType):
    """Margins, page sizes, and distances are all measured in tenths to keep MusicXML data in a consistent coordinate system as much as possible. The translation to absolute units is done with the scaling type, which specifies how many millimeters are equal to how many tenths. For a staff height of 7 mm, millimeters would be set to 7 while tenths is set to 40. The ability to set a formula rather than a single scaling factor helps avoid roundoff errors."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='scaling']"


class XSDComplexTypeStaffLayout(XSDComplexType):
    """Staff layout includes the vertical distance from the bottom line of the previous staff in this system to the top line of the staff specified by the number attribute. The optional number attribute refers to staff numbers within the part, from top to bottom on the system. A value of 1 is used if not present.

When used in the defaults element, the values apply to all systems in all parts. When used in the print element, the values apply to the current system only. This value is ignored for the first staff in a system."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='staff-layout']"


class XSDComplexTypeSystemDividers(XSDComplexType):
    """The system-dividers element indicates the presence or absence of system dividers (also known as system separation marks) between systems displayed on the same page. Dividers on the left and right side of the page are controlled by the left-divider and right-divider elements respectively. The default vertical position is half the system-distance value from the top of the system that is below the divider. The default horizontal position is the left and right system margin, respectively.

When used in the print element, the system-dividers element affects the dividers that would appear between the current system and the previous system."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='system-dividers']"


class XSDComplexTypeSystemLayout(XSDComplexType):
    """A system is a group of staves that are read and played simultaneously. System layout includes left and right margins and the vertical distance from the previous system. The system distance is measured from the bottom line of the previous system to the top line of the current system. It is ignored for the first system on a page. The top system distance is measured from the page's top margin to the top line of the first system. It is ignored for all but the first system on a page.

Sometimes the sum of measure widths in a system may not equal the system width specified by the layout elements due to roundoff or other errors. The behavior when reading MusicXML files in these cases is application-dependent. For instance, applications may find that the system layout data is more reliable than the sum of the measure widths, and adjust the measure widths accordingly.

When used in the defaults element, the system-layout element defines a default appearance for all systems in the score. If no system-layout element is present in the defaults element, default system layout values are chosen by the application.

When used in the print element, the system-layout element affects the appearance of the current system only. All other systems use the default values as determined by the defaults element. If any child elements are missing from the system-layout element in a print element, the values determined by the defaults element are used there as well. This type of system-layout element need only be read from or written to the first visible part in the score."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='system-layout']"


class XSDComplexTypeSystemMargins(XSDComplexType):
    """System margins are relative to the page margins. Positive values indent and negative values reduce the margin size."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='system-margins']"


class XSDComplexTypeBookmark(XSDComplexType):
    """The bookmark type serves as a well-defined target for an incoming simple XLink."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='bookmark']"


class XSDComplexTypeLink(XSDComplexType):
    """The link type serves as an outgoing simple XLink. If a relative link is used within a document that is part of a compressed MusicXML file, the link is relative to the root folder of the zip file."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='link']"


class XSDComplexTypeAccidental(XSDComplexType):
    """The accidental type represents actual notated accidentals. Editorial and cautionary indications are indicated by attributes. Values for these attributes are "no" if not present. Specific graphic display such as parentheses, brackets, and size are controlled by the level-display attribute group.

``simpleContent``: The accidental-value type represents notated accidentals supported by MusicXML. In the MusicXML 2.0 DTD this was a string with values that could be included. The XSD strengthens the data typing to an enumerated list. The quarter- and three-quarters- accidentals are Tartini-style quarter-tone accidentals. The -down and -up accidentals are quarter-tone accidentals that include arrows pointing down or up. The slash- accidentals are used in Turkish classical music. The numbered sharp and flat accidentals are superscripted versions of the accidental signs, used in Turkish folk music. The sori and koron accidentals are microtonal sharp and flat accidentals used in Iranian and Persian music. The other accidental covers accidentals other than those listed here. It is usually used in combination with the smufl attribute to specify a particular SMuFL accidental. The smufl attribute may be used with any accidental value to help specify the appearance of symbols that share the same MusicXML semantics.
    
    Permitted Values: ``'sharp'``, ``'natural'``, ``'flat'``, ``'double-sharp'``, ``'sharp-sharp'``, ``'flat-flat'``, ``'natural-sharp'``, ``'natural-flat'``, ``'quarter-flat'``, ``'quarter-sharp'``, ``'three-quarters-flat'``, ``'three-quarters-sharp'``, ``'sharp-down'``, ``'sharp-up'``, ``'natural-down'``, ``'natural-up'``, ``'flat-down'``, ``'flat-up'``, ``'double-sharp-down'``, ``'double-sharp-up'``, ``'flat-flat-down'``, ``'flat-flat-up'``, ``'arrow-down'``, ``'arrow-up'``, ``'triple-sharp'``, ``'triple-flat'``, ``'slash-quarter-sharp'``, ``'slash-sharp'``, ``'slash-flat'``, ``'double-slash-flat'``, ``'sharp-1'``, ``'sharp-2'``, ``'sharp-3'``, ``'sharp-5'``, ``'flat-1'``, ``'flat-2'``, ``'flat-3'``, ``'flat-4'``, ``'sori'``, ``'koron'``, ``'other'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeAccidentalValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='accidental']"


class XSDComplexTypeAccidentalMark(XSDComplexType):
    """An accidental-mark can be used as a separate notation or as part of an ornament. When used in an ornament, position and placement are relative to the ornament, not relative to the note.

``simpleContent``: The accidental-value type represents notated accidentals supported by MusicXML. In the MusicXML 2.0 DTD this was a string with values that could be included. The XSD strengthens the data typing to an enumerated list. The quarter- and three-quarters- accidentals are Tartini-style quarter-tone accidentals. The -down and -up accidentals are quarter-tone accidentals that include arrows pointing down or up. The slash- accidentals are used in Turkish classical music. The numbered sharp and flat accidentals are superscripted versions of the accidental signs, used in Turkish folk music. The sori and koron accidentals are microtonal sharp and flat accidentals used in Iranian and Persian music. The other accidental covers accidentals other than those listed here. It is usually used in combination with the smufl attribute to specify a particular SMuFL accidental. The smufl attribute may be used with any accidental value to help specify the appearance of symbols that share the same MusicXML semantics.
    
    Permitted Values: ``'sharp'``, ``'natural'``, ``'flat'``, ``'double-sharp'``, ``'sharp-sharp'``, ``'flat-flat'``, ``'natural-sharp'``, ``'natural-flat'``, ``'quarter-flat'``, ``'quarter-sharp'``, ``'three-quarters-flat'``, ``'three-quarters-sharp'``, ``'sharp-down'``, ``'sharp-up'``, ``'natural-down'``, ``'natural-up'``, ``'flat-down'``, ``'flat-up'``, ``'double-sharp-down'``, ``'double-sharp-up'``, ``'flat-flat-down'``, ``'flat-flat-up'``, ``'arrow-down'``, ``'arrow-up'``, ``'triple-sharp'``, ``'triple-flat'``, ``'slash-quarter-sharp'``, ``'slash-sharp'``, ``'slash-flat'``, ``'double-slash-flat'``, ``'sharp-1'``, ``'sharp-2'``, ``'sharp-3'``, ``'sharp-5'``, ``'flat-1'``, ``'flat-2'``, ``'flat-3'``, ``'flat-4'``, ``'sori'``, ``'koron'``, ``'other'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeAccidentalValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='accidental-mark']"


class XSDComplexTypeArpeggiate(XSDComplexType):
    """The arpeggiate type indicates that this note is part of an arpeggiated chord. The number attribute can be used to distinguish between two simultaneous chords arpeggiated separately (different numbers) or together (same number). The direction attribute is used if there is an arrow on the arpeggio sign. By default, arpeggios go from the lowest to highest note.  The length of the sign can be determined from the position attributes for the arpeggiate elements used with the top and bottom notes of the arpeggiated chord. If the unbroken attribute is set to yes, it indicates that the arpeggio continues onto another staff within the part. This serves as a hint to applications and is not required for cross-staff arpeggios."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='arpeggiate']"


class XSDComplexTypeArticulations(XSDComplexType):
    """Articulations and accents are grouped together here."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='articulations']"


class XSDComplexTypeArrow(XSDComplexType):
    """The arrow element represents an arrow used for a musical technical indication. It can represent both Unicode and SMuFL arrows. The presence of an arrowhead element indicates that only the arrowhead is displayed, not the arrow stem. The smufl attribute distinguishes different SMuFL glyphs that have an arrow appearance such as arrowBlackUp, guitarStrumUp, or handbellsSwingUp. The specified glyph should match the descriptive representation."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='arrow']"


class XSDComplexTypeAssess(XSDComplexType):
    """By default, an assessment application should assess all notes without a cue child element, and not assess any note with a cue child element. The assess type allows this default assessment to be overridden for individual notes. The optional player and time-only attributes restrict the type to apply to a single player or set of times through a repeated section, respectively. If missing, the type applies to all players or all times through the repeated section, respectively. The player attribute references the id attribute of a player element defined within the matching score-part."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='assess']"


class XSDComplexTypeBackup(XSDComplexType):
    """The backup and forward elements are required to coordinate multiple voices in one part, including music on multiple staves. The backup type is generally used to move between voices and staves. Thus the backup element does not include voice or staff elements. Duration values should always be positive, and should not cross measure boundaries or mid-measure changes in the divisions value."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='backup']"


class XSDComplexTypeBeam(XSDComplexType):
    """Beam values include begin, continue, end, forward hook, and backward hook. Up to eight concurrent beams are available to cover up to 1024th notes. Each beam in a note is represented with a separate beam element, starting with the eighth note beam using a number attribute of 1.

Note that the beam number does not distinguish sets of beams that overlap, as it does for slur and other elements. Beaming groups are distinguished by being in different voices and/or the presence or absence of grace and cue elements.

Beams that have a begin value can also have a fan attribute to indicate accelerandos and ritardandos using fanned beams. The fan attribute may also be used with a continue value if the fanning direction changes on that note. The value is "none" if not specified.

The repeater attribute has been deprecated in MusicXML 3.0. Formerly used for tremolos, it needs to be specified with a "yes" value for each beam using it.

``simpleContent``: The beam-value type represents the type of beam associated with each of 8 beam levels (up to 1024th notes) available for each note.
    
    Permitted Values: ``'begin'``, ``'continue'``, ``'end'``, ``'forward hook'``, ``'backward hook'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeBeamValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='beam']"


class XSDComplexTypeBend(XSDComplexType):
    """The bend type is used in guitar notation and tablature. A single note with a bend and release will contain two bend elements: the first to represent the bend and the second to represent the release. The shape attribute distinguishes between the angled bend symbols commonly used in standard notation and the curved bend symbols commonly used in both tablature and standard notation."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='bend']"


class XSDComplexTypeBreathMark(XSDComplexType):
    """The breath-mark element indicates a place to take a breath.

``simpleContent``: The breath-mark-value type represents the symbol used for a breath mark.
    
    Permitted Values: ``''``, ``'comma'``, ``'tick'``, ``'upbow'``, ``'salzedo'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeBreathMarkValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='breath-mark']"


class XSDComplexTypeCaesura(XSDComplexType):
    """The caesura element indicates a slight pause. It is notated using a "railroad tracks" symbol or other variations specified in the element content.

``simpleContent``: The caesura-value type represents the shape of the caesura sign.
    
    Permitted Values: ``'normal'``, ``'thick'``, ``'short'``, ``'curved'``, ``'single'``, ``''``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeCaesuraValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='caesura']"


class XSDComplexTypeElision(XSDComplexType):
    """The elision type represents an elision between lyric syllables. The text content specifies the symbol used to display the elision. Common values are a no-break space (Unicode 00A0), an underscore (Unicode 005F), or an undertie (Unicode 203F). If the text content is empty, the smufl attribute is used to specify the symbol to use. Its value is a SMuFL canonical glyph name that starts with lyrics. The SMuFL attribute is ignored if the elision glyph is already specified by the text content. If neither text content nor a smufl attribute are present, the elision glyph is application-specific."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='elision']"


class XSDComplexTypeEmptyLine(XSDComplexType):
    """The empty-line type represents an empty element with line-shape, line-type, line-length, dashed-formatting, print-style and placement attributes."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='empty-line']"


class XSDComplexTypeExtend(XSDComplexType):
    """The extend type represents lyric word extension / melisma lines as well as figured bass extensions. The optional type and position attributes are added in Version 3.0 to provide better formatting control."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='extend']"


class XSDComplexTypeFigure(XSDComplexType):
    """The figure type represents a single figure within a figured-bass element."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='figure']"


class XSDComplexTypeFiguredBass(XSDComplexType):
    """The figured-bass element represents figured bass notation. Figured bass elements take their position from the first regular note (not a grace note or chord note) that follows in score order. The optional duration element is used to indicate changes of figures under a note.

Figures are ordered from top to bottom. The value of parentheses is "no" if not present."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='figured-bass']"


class XSDComplexTypeForward(XSDComplexType):
    """The backup and forward elements are required to coordinate multiple voices in one part, including music on multiple staves. The forward element is generally used within voices and staves. Duration values should always be positive, and should not cross measure boundaries or mid-measure changes in the divisions value."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='forward']"


class XSDComplexTypeGlissando(XSDComplexType):
    """Glissando and slide types both indicate rapidly moving from one pitch to the other so that individual notes are not discerned. A glissando sounds the distinct notes in between the two pitches and defaults to a wavy line. The optional text is printed alongside the line."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='glissando']"


class XSDComplexTypeGrace(XSDComplexType):
    """The grace type indicates the presence of a grace note. The slash attribute for a grace note is yes for slashed grace notes. The steal-time-previous attribute indicates the percentage of time to steal from the previous note for the grace note. The steal-time-following attribute indicates the percentage of time to steal from the following note for the grace note, as for appoggiaturas. The make-time attribute indicates to make time, not steal time; the units are in real-time divisions for the grace note."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='grace']"


class XSDComplexTypeHammerOnPullOff(XSDComplexType):
    """The hammer-on and pull-off elements are used in guitar and fretted instrument notation. Since a single slur can be marked over many notes, the hammer-on and pull-off elements are separate so the individual pair of notes can be specified. The element content can be used to specify how the hammer-on or pull-off should be notated. An empty element leaves this choice up to the application."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='hammer-on-pull-off']"


class XSDComplexTypeHandbell(XSDComplexType):
    """The handbell element represents notation for various techniques used in handbell and handchime music.

``simpleContent``: The handbell-value type represents the type of handbell technique being notated.
    
    Permitted Values: ``'belltree'``, ``'damp'``, ``'echo'``, ``'gyro'``, ``'hand martellato'``, ``'mallet lift'``, ``'mallet table'``, ``'martellato'``, ``'martellato lift'``, ``'muted martellato'``, ``'pluck lift'``, ``'swing'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeHandbellValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='handbell']"


class XSDComplexTypeHarmonClosed(XSDComplexType):
    """The harmon-closed type represents whether the harmon mute is closed, open, or half-open. The optional location attribute indicates which portion of the symbol is filled in when the element value is half.

``simpleContent``: The harmon-closed-value type represents whether the harmon mute is closed, open, or half-open.
    
    Permitted Values: ``'yes'``, ``'no'``, ``'half'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeHarmonClosedValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='harmon-closed']"


class XSDComplexTypeHarmonMute(XSDComplexType):
    """The harmon-mute type represents the symbols used for harmon mutes in brass notation."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='harmon-mute']"


class XSDComplexTypeHarmonic(XSDComplexType):
    """The harmonic type indicates natural and artificial harmonics. Allowing the type of pitch to be specified, combined with controls for appearance/playback differences, allows both the notation and the sound to be represented. Artificial harmonics can add a notated touching pitch; artificial pinch harmonics will usually not notate a touching pitch. The attributes for the harmonic element refer to the use of the circular harmonic symbol, typically but not always used with natural harmonics."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='harmonic']"


class XSDComplexTypeHeelToe(XSDComplexType):
    """The heel and toe elements are used with organ pedals. The substitution value is "no" if the attribute is not present."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='heel-toe']"


class XSDComplexTypeHole(XSDComplexType):
    """The hole type represents the symbols used for woodwind and brass fingerings as well as other notations."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='hole']"


class XSDComplexTypeHoleClosed(XSDComplexType):
    """The hole-closed type represents whether the hole is closed, open, or half-open. The optional location attribute indicates which portion of the hole is filled in when the element value is half.

``simpleContent``: The hole-closed-value type represents whether the hole is closed, open, or half-open.
    
    Permitted Values: ``'yes'``, ``'no'``, ``'half'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeHoleClosedValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='hole-closed']"


class XSDComplexTypeInstrument(XSDComplexType):
    """The instrument type distinguishes between score-instrument elements in a score-part. The id attribute is an IDREF back to the score-instrument ID. If multiple score-instruments are specified in a score-part, there should be an instrument element for each note in the part. Notes that are shared between multiple score-instruments can have more than one instrument element."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='instrument']"


class XSDComplexTypeListen(XSDComplexType):
    """The listen and listening types, new in Version 4.0, specify different ways that a score following or machine listening application can interact with a performer. The listen type handles interactions that are specific to a note. If multiple child elements of the same type are present, they should have distinct player and/or time-only attributes."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='listen']"


class XSDComplexTypeLyric(XSDComplexType):
    """The lyric type represents text underlays for lyrics. Two text elements that are not separated by an elision element are part of the same syllable, but may have different text formatting. The MusicXML XSD is more strict than the DTD in enforcing this by disallowing a second syllabic element unless preceded by an elision element. The lyric number indicates multiple lines, though a name can be used as well. Common name examples are verse and chorus.

Justification is center by default; placement is below by default. Vertical alignment is to the baseline of the text and horizontal alignment matches justification. The print-object attribute can override a note's print-lyric attribute in cases where only some lyrics on a note are printed, as when lyrics for later verses are printed in a block of text rather than with each note. The time-only attribute precisely specifies which lyrics are to be sung which time through a repeated section."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='lyric']"


class XSDComplexTypeMordent(XSDComplexType):
    """The mordent type is used for both represents the mordent sign with the vertical line and the inverted-mordent sign without the line. The long attribute is "no" by default. The approach and departure attributes are used for compound ornaments, indicating how the beginning and ending of the ornament look relative to the main part of the mordent."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='mordent']"


class XSDComplexTypeNonArpeggiate(XSDComplexType):
    """The non-arpeggiate type indicates that this note is at the top or bottom of a bracket indicating to not arpeggiate these notes. Since this does not involve playback, it is only used on the top or bottom notes, not on each note as for the arpeggiate type."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='non-arpeggiate']"


class XSDComplexTypeNotations(XSDComplexType):
    """Notations refer to musical notations, not XML notations. Multiple notations are allowed in order to represent multiple editorial levels. The print-object attribute, added in Version 3.0, allows notations to represent details of performance technique, such as fingerings, without having them appear in the score."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='notations']"


class XSDComplexTypeNoteType(XSDComplexType):
    """The note-type type indicates the graphic note type. Values range from 1024th to maxima. The size attribute indicates full, cue, grace-cue, or large size. The default is full for regular notes, grace-cue for notes that contain both grace and cue elements, and cue for notes that contain either a cue or a grace element, but not both.

``simpleContent``: The note-type-value type is used for the MusicXML type element and represents the graphic note type, from 1024th (shortest) to maxima (longest).
    
    Permitted Values: ``'1024th'``, ``'512th'``, ``'256th'``, ``'128th'``, ``'64th'``, ``'32nd'``, ``'16th'``, ``'eighth'``, ``'quarter'``, ``'half'``, ``'whole'``, ``'breve'``, ``'long'``, ``'maxima'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeNoteTypeValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='note-type']"


class XSDComplexTypeNotehead(XSDComplexType):
    """The notehead type indicates shapes other than the open and closed ovals associated with note durations. 

The smufl attribute can be used to specify a particular notehead, allowing application interoperability without requiring every SMuFL glyph to have a MusicXML element equivalent. This attribute can be used either with the "other" value, or to refine a specific notehead value such as "cluster". Noteheads in the SMuFL Note name noteheads and Note name noteheads supplement ranges (U+E150–U+E1AF and U+EEE0–U+EEFF) should not use the smufl attribute or the "other" value, but instead use the notehead-text element.

For the enclosed shapes, the default is to be hollow for half notes and longer, and filled otherwise. The filled attribute can be set to change this if needed.

If the parentheses attribute is set to yes, the notehead is parenthesized. It is no by default.

``simpleContent``: The notehead-value type indicates shapes other than the open and closed ovals associated with note durations. 

The values do, re, mi, fa, fa up, so, la, and ti correspond to Aikin's 7-shape system.  The fa up shape is typically used with upstems; the fa shape is typically used with downstems or no stems.

The arrow shapes differ from triangle and inverted triangle by being centered on the stem. Slashed and back slashed notes include both the normal notehead and a slash. The triangle shape has the tip of the triangle pointing up; the inverted triangle shape has the tip of the triangle pointing down. The left triangle shape is a right triangle with the hypotenuse facing up and to the left.

The other notehead covers noteheads other than those listed here. It is usually used in combination with the smufl attribute to specify a particular SMuFL notehead. The smufl attribute may be used with any notehead value to help specify the appearance of symbols that share the same MusicXML semantics. Noteheads in the SMuFL Note name noteheads and Note name noteheads supplement ranges (U+E150–U+E1AF and U+EEE0–U+EEFF) should not use the smufl attribute or the "other" value, but instead use the notehead-text element.
    
    Permitted Values: ``'slash'``, ``'triangle'``, ``'diamond'``, ``'square'``, ``'cross'``, ``'x'``, ``'circle-x'``, ``'inverted triangle'``, ``'arrow down'``, ``'arrow up'``, ``'circled'``, ``'slashed'``, ``'back slashed'``, ``'normal'``, ``'cluster'``, ``'circle dot'``, ``'left triangle'``, ``'rectangle'``, ``'none'``, ``'do'``, ``'re'``, ``'mi'``, ``'fa'``, ``'fa up'``, ``'so'``, ``'la'``, ``'ti'``, ``'other'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeNoteheadValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='notehead']"


class XSDComplexTypeNoteheadText(XSDComplexType):
    """The notehead-text type represents text that is displayed inside a notehead, as is done in some educational music. It is not needed for the numbers used in tablature or jianpu notation. The presence of a TAB or jianpu clefs is sufficient to indicate that numbers are used. The display-text and accidental-text elements allow display of fully formatted text and accidentals."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='notehead-text']"


class XSDComplexTypeOrnaments(XSDComplexType):
    """Ornaments can be any of several types, followed optionally by accidentals. The accidental-mark element's content is represented the same as an accidental element, but with a different name to reflect the different musical meaning."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='ornaments']"


class XSDComplexTypeOtherNotation(XSDComplexType):
    """The other-notation type is used to define any notations not yet in the MusicXML format. It handles notations where more specific extension elements such as other-dynamics and other-technical are not appropriate. The smufl attribute can be used to specify a particular notation, allowing application interoperability without requiring every SMuFL glyph to have a MusicXML element equivalent. Using the other-notation type without the smufl attribute allows for extended representation, though without application interoperability."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='other-notation']"


class XSDComplexTypeOtherPlacementText(XSDComplexType):
    """The other-placement-text type represents a text element with print-style, placement, and smufl attribute groups. This type is used by MusicXML notation extension elements to allow specification of specific SMuFL glyphs without needed to add every glyph as a MusicXML element."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='other-placement-text']"


class XSDComplexTypeOtherText(XSDComplexType):
    """The other-text type represents a text element with a smufl attribute group. This type is used by MusicXML direction extension elements to allow specification of specific SMuFL glyphs without needed to add every glyph as a MusicXML element."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='other-text']"


class XSDComplexTypePitch(XSDComplexType):
    """Pitch is represented as a combination of the step of the diatonic scale, the chromatic alteration, and the octave."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='pitch']"


class XSDComplexTypePlacementText(XSDComplexType):
    """The placement-text type represents a text element with print-style and placement attribute groups."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='placement-text']"


class XSDComplexTypeRelease(XSDComplexType):
    """The release type indicates that a bend is a release rather than a normal bend or pre-bend. The offset attribute specifies where the release starts in terms of divisions relative to the current note. The first-beat and last-beat attributes of the parent bend element are relative to the original note position, not this offset value."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='release']"


class XSDComplexTypeRest(XSDComplexType):
    """The rest element indicates notated rests or silences. Rest elements are usually empty, but placement on the staff can be specified using display-step and display-octave elements. If the measure attribute is set to yes, this indicates this is a complete measure rest."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='rest']"


class XSDComplexTypeSlide(XSDComplexType):
    """Glissando and slide types both indicate rapidly moving from one pitch to the other so that individual notes are not discerned. A slide is continuous between the two pitches and defaults to a solid line. The optional text for a is printed alongside the line."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='slide']"


class XSDComplexTypeSlur(XSDComplexType):
    """Slur types are empty. Most slurs are represented with two elements: one with a start type, and one with a stop type. Slurs can add more elements using a continue type. This is typically used to specify the formatting of cross-system slurs, or to specify the shape of very complex slurs."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='slur']"


class XSDComplexTypeStem(XSDComplexType):
    """Stems can be down, up, none, or double. For down and up stems, the position attributes can be used to specify stem length. The relative values specify the end of the stem relative to the program default. Default values specify an absolute end stem position. Negative values of relative-y that would flip a stem instead of shortening it are ignored. A stem element associated with a rest refers to a stemlet.

``simpleContent``: The stem-value type represents the notated stem direction.
    
    Permitted Values: ``'down'``, ``'up'``, ``'double'``, ``'none'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeStemValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='stem']"


class XSDComplexTypeStrongAccent(XSDComplexType):
    """The strong-accent type indicates a vertical accent mark. The type attribute indicates if the point of the accent is down or up."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='strong-accent']"


class XSDComplexTypeStyleText(XSDComplexType):
    """The style-text type represents a text element with a print-style attribute group."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='style-text']"


class XSDComplexTypeTap(XSDComplexType):
    """The tap type indicates a tap on the fretboard. The text content allows specification of the notation; + and T are common choices. If the element is empty, the hand attribute is used to specify the symbol to use. The hand attribute is ignored if the tap glyph is already specified by the text content. If neither text content nor the hand attribute are present, the display is application-specific."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='tap']"


class XSDComplexTypeTechnical(XSDComplexType):
    """Technical indications give performance information for individual instruments."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='technical']"


class XSDComplexTypeTextElementData(XSDComplexType):
    """The text-element-data type represents a syllable or portion of a syllable for lyric text underlay. A hyphen in the string content should only be used for an actual hyphenated word. Language names for text elements come from ISO 639, with optional country subcodes from ISO 3166."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='text-element-data']"


class XSDComplexTypeTie(XSDComplexType):
    """The tie element indicates that a tie begins or ends with this note. If the tie element applies only particular times through a repeat, the time-only attribute indicates which times to apply it. The tie element indicates sound; the tied element indicates notation."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='tie']"


class XSDComplexTypeTied(XSDComplexType):
    """The tied element represents the notated tie. The tie element represents the tie sound.

The number attribute is rarely needed to disambiguate ties, since note pitches will usually suffice. The attribute is implied rather than defaulting to 1 as with most elements. It is available for use in more complex tied notation situations.

Ties that join two notes of the same pitch together should be represented with a tied element on the first note with type="start" and a tied element on the second note with type="stop".  This can also be done if the two notes being tied are enharmonically equivalent, but have different step values. It is not recommended to use tied elements to join two notes with enharmonically inequivalent pitches.

Ties that indicate that an instrument should be undamped are specified with a single tied element with type="let-ring".

Ties that are visually attached to only one note, other than undamped ties, should be specified with two tied elements on the same note, first type="start" then type="stop". This can be used to represent ties into or out of repeated sections or codas."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='tied']"


class XSDComplexTypeTimeModification(XSDComplexType):
    """Time modification indicates tuplets, double-note tremolos, and other durational changes. A time-modification element shows how the cumulative, sounding effect of tuplets and double-note tremolos compare to the written note type represented by the type and dot elements. Nested tuplets and other notations that use more detailed information need both the time-modification and tuplet elements to be represented accurately."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='time-modification']"


class XSDComplexTypeTremolo(XSDComplexType):
    """The tremolo ornament can be used to indicate single-note, double-note, or unmeasured tremolos. Single-note tremolos use the single type, double-note tremolos use the start and stop types, and unmeasured tremolos use the unmeasured type. The default is "single" for compatibility with Version 1.1. The text of the element indicates the number of tremolo marks and is an integer from 0 to 8. Note that the number of attached beams is not included in this value, but is represented separately using the beam element. The value should be 0 for unmeasured tremolos.

When using double-note tremolos, the duration of each note in the tremolo should correspond to half of the notated type value. A time-modification element should also be added with an actual-notes value of 2 and a normal-notes value of 1. If used within a tuplet, this 2/1 ratio should be multiplied by the existing tuplet ratio.

The smufl attribute specifies the glyph to use from the SMuFL Tremolos range for an unmeasured tremolo. It is ignored for other tremolo types. The SMuFL buzzRoll glyph is used by default if the attribute is missing.

Using repeater beams for indicating tremolos is deprecated as of MusicXML 3.0.

``simpleContent``: The number of tremolo marks is represented by a number from 0 to 8: the same as beam-level with 0 added."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeTremoloMarks
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='tremolo']"


class XSDComplexTypeTuplet(XSDComplexType):
    """A tuplet element is present when a tuplet is to be displayed graphically, in addition to the sound data provided by the time-modification elements. The number attribute is used to distinguish nested tuplets. The bracket attribute is used to indicate the presence of a bracket. If unspecified, the results are implementation-dependent. The line-shape attribute is used to specify whether the bracket is straight or in the older curved or slurred style. It is straight by default.

Whereas a time-modification element shows how the cumulative, sounding effect of tuplets and double-note tremolos compare to the written note type, the tuplet element describes how this is displayed. The tuplet element also provides more detailed representation information than the time-modification element, and is needed to represent nested tuplets and other complex tuplets accurately.

The show-number attribute is used to display either the number of actual notes, the number of both actual and normal notes, or neither. It is actual by default. The show-type attribute is used to display either the actual type, both the actual and normal types, or neither. It is none by default."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='tuplet']"


class XSDComplexTypeTupletDot(XSDComplexType):
    """The tuplet-dot type is used to specify dotted tuplet types."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='tuplet-dot']"


class XSDComplexTypeTupletNumber(XSDComplexType):
    """The tuplet-number type indicates the number of notes for this portion of the tuplet."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeNonNegativeInteger
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='tuplet-number']"


class XSDComplexTypeTupletPortion(XSDComplexType):
    """The tuplet-portion type provides optional full control over tuplet specifications. It allows the number and note type (including dots) to be set for the actual and normal portions of a single tuplet. If any of these elements are absent, their values are based on the time-modification element."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='tuplet-portion']"


class XSDComplexTypeTupletType(XSDComplexType):
    """The tuplet-type type indicates the graphical note type of the notes for this portion of the tuplet.

``simpleContent``: The note-type-value type is used for the MusicXML type element and represents the graphic note type, from 1024th (shortest) to maxima (longest).
    
    Permitted Values: ``'1024th'``, ``'512th'``, ``'256th'``, ``'128th'``, ``'64th'``, ``'32nd'``, ``'16th'``, ``'eighth'``, ``'quarter'``, ``'half'``, ``'whole'``, ``'breve'``, ``'long'``, ``'maxima'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeNoteTypeValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='tuplet-type']"


class XSDComplexTypeUnpitched(XSDComplexType):
    """The unpitched type represents musical elements that are notated on the staff but lack definite pitch, such as unpitched percussion and speaking voice. If the child elements are not present, the note is placed on the middle line of the staff. This is generally used with a one-line staff. Notes in percussion clef should always use an unpitched element rather than a pitch element."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='unpitched']"


class XSDComplexTypeWait(XSDComplexType):
    """The wait type specifies a point where the accompaniment should wait for a performer event before continuing. This typically happens at the start of new sections or after a held note or indeterminate music. These waiting points cannot always be inferred reliably from the contents of the displayed score. The optional player and time-only attributes restrict the type to apply to a single player or set of times through a repeated section, respectively."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='wait']"


class XSDComplexTypeCredit(XSDComplexType):
    """The credit type represents the appearance of the title, composer, arranger, lyricist, copyright, dedication, and other text, symbols, and graphics that commonly appear on the first page of a score. The credit-words, credit-symbol, and credit-image elements are similar to the words, symbol, and image elements for directions. However, since the credit is not part of a measure, the default-x and default-y attributes adjust the origin relative to the bottom left-hand corner of the page. The enclosure for credit-words and credit-symbol is none by default.

By default, a series of credit-words and credit-symbol elements within a single credit element follow one another in sequence visually. Non-positional formatting attributes are carried over from the previous element by default.

The page attribute for the credit element specifies the page number where the credit should appear. This is an integer value that starts with 1 for the first page. Its value is 1 by default. Since credits occur before the music, these page numbers do not refer to the page numbering specified by the print element's page-number attribute.

The credit-type element indicates the purpose behind a credit. Multiple types of data may be combined in a single credit, so multiple elements may be used. Standard values include page number, title, subtitle, composer, arranger, lyricist, rights, and part name."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='credit']"


class XSDComplexTypeDefaults(XSDComplexType):
    """The defaults type specifies score-wide defaults for scaling; whether or not the file is a concert score; layout; and default values for the music font, word font, lyric font, and lyric language. Except for the concert-score element, if any defaults are missing, the choice of what to use is determined by the application."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='defaults']"


class XSDComplexTypeEmptyFont(XSDComplexType):
    """The empty-font type represents an empty element with font attributes."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='empty-font']"


class XSDComplexTypeGroupBarline(XSDComplexType):
    """The group-barline type indicates if the group should have common barlines.

``simpleContent``: The group-barline-value type indicates if the group should have common barlines.
    
    Permitted Values: ``'yes'``, ``'no'``, ``'Mensurstrich'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeGroupBarlineValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='group-barline']"


class XSDComplexTypeGroupName(XSDComplexType):
    """The group-name type describes the name or abbreviation of a part-group element. Formatting attributes in the group-name type are deprecated in Version 2.0 in favor of the new group-name-display and group-abbreviation-display elements."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='group-name']"


class XSDComplexTypeGroupSymbol(XSDComplexType):
    """The group-symbol type indicates how the symbol for a group is indicated in the score. It is none if not specified.

``simpleContent``: The group-symbol-value type indicates how the symbol for a group or multi-staff part is indicated in the score.
    
    Permitted Values: ``'none'``, ``'brace'``, ``'line'``, ``'bracket'``, ``'square'``
"""
    
    _SIMPLE_CONTENT = XSDSimpleTypeGroupSymbolValue
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='group-symbol']"


class XSDComplexTypeInstrumentLink(XSDComplexType):
    """Multiple part-link elements can link a condensed part within a score file to multiple MusicXML parts files. For example, a "Clarinet 1 and 2" part in a score file could link to separate "Clarinet 1" and "Clarinet 2" part files. The instrument-link type distinguish which of the score-instruments within a score-part are in which part file. The instrument-link id attribute refers to a score-instrument id attribute."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='instrument-link']"


class XSDComplexTypeLyricFont(XSDComplexType):
    """The lyric-font type specifies the default font for a particular name and number of lyric."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='lyric-font']"


class XSDComplexTypeLyricLanguage(XSDComplexType):
    """The lyric-language type specifies the default language for a particular name and number of lyric."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='lyric-language']"


class XSDComplexTypeOpus(XSDComplexType):
    """The opus type represents a link to a MusicXML opus document that composes multiple MusicXML scores into a collection."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='opus']"


class XSDComplexTypePartGroup(XSDComplexType):
    """The part-group element indicates groupings of parts in the score, usually indicated by braces and brackets. Braces that are used for multi-staff parts should be defined in the attributes element for that part. The part-group start element appears before the first score-part in the group. The part-group stop element appears after the last score-part in the group.

The number attribute is used to distinguish overlapping and nested part-groups, not the sequence of groups. As with parts, groups can have a name and abbreviation. Values for the child elements are ignored at the stop of a group.

A part-group element is not needed for a single multi-staff part. By default, multi-staff parts include a brace symbol and (if appropriate given the bar-style) common barlines. The symbol formatting for a multi-staff part can be more fully specified using the part-symbol element."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='part-group']"


class XSDComplexTypePartLink(XSDComplexType):
    """The part-link type allows MusicXML data for both score and parts to be contained within a single compressed MusicXML file. It links a score-part from a score document to MusicXML documents that contain parts data. In the case of a single compressed MusicXML file, the link href values are paths that are relative to the root folder of the zip file."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='part-link']"


class XSDComplexTypePartList(XSDComplexType):
    """The part-list identifies the different musical parts in this document. Each part has an ID that is used later within the musical data. Since parts may be encoded separately and combined later, identification elements are present at both the score and score-part levels. There must be at least one score-part, combined as desired with part-group elements that indicate braces and brackets. Parts are ordered from top to bottom in a score based on the order in which they appear in the part-list."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='part-list']"


class XSDComplexTypePartName(XSDComplexType):
    """The part-name type describes the name or abbreviation of a score-part element. Formatting attributes for the part-name element are deprecated in Version 2.0 in favor of the new part-name-display and part-abbreviation-display elements."""
    
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='part-name']"


class XSDComplexTypePlayer(XSDComplexType):
    """The player type allows for multiple players per score-part for use in listening applications. One player may play multiple instruments, while a single instrument may include multiple players in divisi sections."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='player']"


class XSDComplexTypeScoreInstrument(XSDComplexType):
    """The score-instrument type represents a single instrument within a score-part. As with the score-part type, each score-instrument has a required ID attribute, a name, and an optional abbreviation.

A score-instrument type is also required if the score specifies MIDI 1.0 channels, banks, or programs. An initial midi-instrument assignment can also be made here. MusicXML software should be able to automatically assign reasonable channels and instruments without these elements in simple cases, such as where part names match General MIDI instrument names.

The score-instrument element can also distinguish multiple instruments of the same type that are on the same part, such as Clarinet 1 and Clarinet 2 instruments within a Clarinets 1 and 2 part."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='score-instrument']"


class XSDComplexTypeScorePart(XSDComplexType):
    """The score-part type collects part-wide information for each part in a score. Often, each MusicXML part corresponds to a track in a Standard MIDI Format 1 file. In this case, the midi-device element is used to make a MIDI device or port assignment for the given track or specific MIDI instruments. Initial midi-instrument assignments may be made here as well. The score-instrument elements are used when there are multiple instruments per track."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='score-part']"


class XSDComplexTypeVirtualInstrument(XSDComplexType):
    """The virtual-instrument element defines a specific virtual instrument used for an instrument sound."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='virtual-instrument']"


class XSDComplexTypeWork(XSDComplexType):
    """Works are optionally identified by number and title. The work type also may indicate a link to the opus document that composes multiple scores into a collection."""
    
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='work']"

__all__=['XSDComplexType', 'XSDComplexTypeScorePartwise', 'XSDComplexTypePart', 'XSDComplexTypeMeasure', 'XSDComplexTypeDirective', 'XSDComplexTypeNote', 'XSDComplexTypeAccidentalText', 'XSDComplexTypeCoda', 'XSDComplexTypeDynamics', 'XSDComplexTypeEmpty', 'XSDComplexTypeEmptyPlacement', 'XSDComplexTypeEmptyPlacementSmufl', 'XSDComplexTypeEmptyPrintStyle', 'XSDComplexTypeEmptyPrintStyleAlign', 'XSDComplexTypeEmptyPrintStyleAlignId', 'XSDComplexTypeEmptyPrintObjectStyleAlign', 'XSDComplexTypeEmptyTrillSound', 'XSDComplexTypeHorizontalTurn', 'XSDComplexTypeFermata', 'XSDComplexTypeFingering', 'XSDComplexTypeFormattedSymbol', 'XSDComplexTypeFormattedSymbolId', 'XSDComplexTypeFormattedText', 'XSDComplexTypeFormattedTextId', 'XSDComplexTypeFret', 'XSDComplexTypeLevel', 'XSDComplexTypeMidiDevice', 'XSDComplexTypeMidiInstrument', 'XSDComplexTypeNameDisplay', 'XSDComplexTypeOtherPlay', 'XSDComplexTypePlay', 'XSDComplexTypeSegno', 'XSDComplexTypeString', 'XSDComplexTypeTypedText', 'XSDComplexTypeWavyLine', 'XSDComplexTypeAttributes', 'XSDComplexTypeBeatRepeat', 'XSDComplexTypeCancel', 'XSDComplexTypeClef', 'XSDComplexTypeDouble', 'XSDComplexTypeForPart', 'XSDComplexTypeInterchangeable', 'XSDComplexTypeKey', 'XSDComplexTypeKeyAccidental', 'XSDComplexTypeKeyOctave', 'XSDComplexTypeLineDetail', 'XSDComplexTypeMeasureRepeat', 'XSDComplexTypeMeasureStyle', 'XSDComplexTypeMultipleRest', 'XSDComplexTypePartClef', 'XSDComplexTypePartSymbol', 'XSDComplexTypePartTranspose', 'XSDComplexTypeSlash', 'XSDComplexTypeStaffDetails', 'XSDComplexTypeStaffSize', 'XSDComplexTypeStaffTuning', 'XSDComplexTypeTime', 'XSDComplexTypeTranspose', 'XSDComplexTypeBarStyleColor', 'XSDComplexTypeBarline', 'XSDComplexTypeEnding', 'XSDComplexTypeRepeat', 'XSDComplexTypeAccord', 'XSDComplexTypeAccordionRegistration', 'XSDComplexTypeBarre', 'XSDComplexTypeBass', 'XSDComplexTypeHarmonyAlter', 'XSDComplexTypeBassStep', 'XSDComplexTypeBeater', 'XSDComplexTypeBeatUnitTied', 'XSDComplexTypeBracket', 'XSDComplexTypeDashes', 'XSDComplexTypeDegree', 'XSDComplexTypeDegreeAlter', 'XSDComplexTypeDegreeType', 'XSDComplexTypeDegreeValue', 'XSDComplexTypeDirection', 'XSDComplexTypeDirectionType', 'XSDComplexTypeEffect', 'XSDComplexTypeFeature', 'XSDComplexTypeFirstFret', 'XSDComplexTypeFrame', 'XSDComplexTypeFrameNote', 'XSDComplexTypeGlass', 'XSDComplexTypeGrouping', 'XSDComplexTypeHarmony', 'XSDComplexTypeHarpPedals', 'XSDComplexTypeImage', 'XSDComplexTypeInstrumentChange', 'XSDComplexTypeInversion', 'XSDComplexTypeKind', 'XSDComplexTypeListening', 'XSDComplexTypeMeasureNumbering', 'XSDComplexTypeMembrane', 'XSDComplexTypeMetal', 'XSDComplexTypeMetronome', 'XSDComplexTypeMetronomeBeam', 'XSDComplexTypeMetronomeNote', 'XSDComplexTypeMetronomeTied', 'XSDComplexTypeMetronomeTuplet', 'XSDComplexTypeNumeral', 'XSDComplexTypeNumeralKey', 'XSDComplexTypeNumeralRoot', 'XSDComplexTypeOctaveShift', 'XSDComplexTypeOffset', 'XSDComplexTypeOtherDirection', 'XSDComplexTypeOtherListening', 'XSDComplexTypePedal', 'XSDComplexTypePedalTuning', 'XSDComplexTypePerMinute', 'XSDComplexTypePercussion', 'XSDComplexTypePitched', 'XSDComplexTypePrincipalVoice', 'XSDComplexTypePrint', 'XSDComplexTypeRoot', 'XSDComplexTypeRootStep', 'XSDComplexTypeScordatura', 'XSDComplexTypeSound', 'XSDComplexTypeStaffDivide', 'XSDComplexTypeStick', 'XSDComplexTypeStringMute', 'XSDComplexTypeSwing', 'XSDComplexTypeSync', 'XSDComplexTypeTimpani', 'XSDComplexTypeWedge', 'XSDComplexTypeWood', 'XSDComplexTypeEncoding', 'XSDComplexTypeIdentification', 'XSDComplexTypeMiscellaneous', 'XSDComplexTypeMiscellaneousField', 'XSDComplexTypeSupports', 'XSDComplexTypeAppearance', 'XSDComplexTypeDistance', 'XSDComplexTypeGlyph', 'XSDComplexTypeLineWidth', 'XSDComplexTypeMeasureLayout', 'XSDComplexTypeNoteSize', 'XSDComplexTypeOtherAppearance', 'XSDComplexTypePageLayout', 'XSDComplexTypePageMargins', 'XSDComplexTypeScaling', 'XSDComplexTypeStaffLayout', 'XSDComplexTypeSystemDividers', 'XSDComplexTypeSystemLayout', 'XSDComplexTypeSystemMargins', 'XSDComplexTypeBookmark', 'XSDComplexTypeLink', 'XSDComplexTypeAccidental', 'XSDComplexTypeAccidentalMark', 'XSDComplexTypeArpeggiate', 'XSDComplexTypeArticulations', 'XSDComplexTypeArrow', 'XSDComplexTypeAssess', 'XSDComplexTypeBackup', 'XSDComplexTypeBeam', 'XSDComplexTypeBend', 'XSDComplexTypeBreathMark', 'XSDComplexTypeCaesura', 'XSDComplexTypeElision', 'XSDComplexTypeEmptyLine', 'XSDComplexTypeExtend', 'XSDComplexTypeFigure', 'XSDComplexTypeFiguredBass', 'XSDComplexTypeForward', 'XSDComplexTypeGlissando', 'XSDComplexTypeGrace', 'XSDComplexTypeHammerOnPullOff', 'XSDComplexTypeHandbell', 'XSDComplexTypeHarmonClosed', 'XSDComplexTypeHarmonMute', 'XSDComplexTypeHarmonic', 'XSDComplexTypeHeelToe', 'XSDComplexTypeHole', 'XSDComplexTypeHoleClosed', 'XSDComplexTypeInstrument', 'XSDComplexTypeListen', 'XSDComplexTypeLyric', 'XSDComplexTypeMordent', 'XSDComplexTypeNonArpeggiate', 'XSDComplexTypeNotations', 'XSDComplexTypeNoteType', 'XSDComplexTypeNotehead', 'XSDComplexTypeNoteheadText', 'XSDComplexTypeOrnaments', 'XSDComplexTypeOtherNotation', 'XSDComplexTypeOtherPlacementText', 'XSDComplexTypeOtherText', 'XSDComplexTypePitch', 'XSDComplexTypePlacementText', 'XSDComplexTypeRelease', 'XSDComplexTypeRest', 'XSDComplexTypeSlide', 'XSDComplexTypeSlur', 'XSDComplexTypeStem', 'XSDComplexTypeStrongAccent', 'XSDComplexTypeStyleText', 'XSDComplexTypeTap', 'XSDComplexTypeTechnical', 'XSDComplexTypeTextElementData', 'XSDComplexTypeTie', 'XSDComplexTypeTied', 'XSDComplexTypeTimeModification', 'XSDComplexTypeTremolo', 'XSDComplexTypeTuplet', 'XSDComplexTypeTupletDot', 'XSDComplexTypeTupletNumber', 'XSDComplexTypeTupletPortion', 'XSDComplexTypeTupletType', 'XSDComplexTypeUnpitched', 'XSDComplexTypeWait', 'XSDComplexTypeCredit', 'XSDComplexTypeDefaults', 'XSDComplexTypeEmptyFont', 'XSDComplexTypeGroupBarline', 'XSDComplexTypeGroupName', 'XSDComplexTypeGroupSymbol', 'XSDComplexTypeInstrumentLink', 'XSDComplexTypeLyricFont', 'XSDComplexTypeLyricLanguage', 'XSDComplexTypeOpus', 'XSDComplexTypePartGroup', 'XSDComplexTypePartLink', 'XSDComplexTypePartList', 'XSDComplexTypePartName', 'XSDComplexTypePlayer', 'XSDComplexTypeScoreInstrument', 'XSDComplexTypeScorePart', 'XSDComplexTypeVirtualInstrument', 'XSDComplexTypeWork']
