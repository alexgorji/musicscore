import importlib
from musicxml.util.helperclasses import MusicXmlTestCase
from musicxml.types.simpletype import XMLSimpleType, XMLSimpleTypeAboveBelow, XMLSimpleTypeNumberOrNormal, \
    XMLSimpleTypePositiveIntegerOrEmpty, XMLSimpleTypeNonNegativeDecimal, XMLSimpleTypeDecimal, XMLSimpleTypeInteger, \
    XMLSimpleTypeNonNegativeInteger, XMLSimpleTypePositiveInteger, XMLSimpleTypeString, XMLSimpleTypeToken, \
    XMLSimpleTypeNMTOKEN, XMLSimpleTypeDate, XMLSimpleTypeMeasureText, XMLSimpleTypePositiveDecimal, \
    XMLSimpleTypeBeamLevel, XMLSimpleTypeColor, XMLSimpleTypeCommaSeparatedText, XMLSimpleTypeSmuflAccidentalGlyphName, \
    XMLSimpleTypeSmuflCodaGlyphName, XMLSimpleTypeSmuflLyricsGlyphName, XMLSimpleTypeSmuflWavyLineGlyphName, \
    XMLSimpleTypeYyyyMmDd
from musicxml.types.simpletype import xml_simple_type_class_names


class TestSimpleTypes(MusicXmlTestCase):
    def test_simple_types_list(self):
        """
        Test if SIMPLE_TYPES in module musicxml.types.simpletype return all simple types
        """
        assert xml_simple_type_class_names == ['XMLSimpleTypeInteger', 'XMLSimpleTypeNonNegativeInteger',
                                               'XMLSimpleTypePositiveInteger', 'XMLSimpleTypeDecimal',
                                               'XMLSimpleTypeString', 'XMLSimpleTypeString', 'XMLSimpleTypeToken',
                                               'XMLSimpleTypeNMTOKEN', 'XMLSimpleTypeDate', 'XMLSimpleTypeAboveBelow',
                                               'XMLSimpleTypeBeamLevel', 'XMLSimpleTypeColor', 'XMLSimpleTypeCommaSeparatedText',
                                               'XMLSimpleTypeCssFontSize', 'XMLSimpleTypeDivisions',
                                               'XMLSimpleTypeEnclosureShape', 'XMLSimpleTypeFermataShape',
                                               'XMLSimpleTypeFontFamily', 'XMLSimpleTypeFontSize', 'XMLSimpleTypeFontStyle',
                                               'XMLSimpleTypeFontWeight', 'XMLSimpleTypeLeftCenterRight',
                                               'XMLSimpleTypeLeftRight', 'XMLSimpleTypeLineLength', 'XMLSimpleTypeLineShape',
                                               'XMLSimpleTypeLineType', 'XMLSimpleTypeMidi16', 'XMLSimpleTypeMidi128',
                                               'XMLSimpleTypeMidi16384', 'XMLSimpleTypeMute', 'XMLSimpleTypeNonNegativeDecimal',
                                               'XMLSimpleTypeNumberLevel', 'XMLSimpleTypeNumberOfLines',
                                               'XMLSimpleTypeNumberOrNormal', 'XMLSimpleTypeNumeralValue',
                                               'XMLSimpleTypeOverUnder', 'XMLSimpleTypePercent', 'XMLSimpleTypePositiveDecimal',
                                               'XMLSimpleTypePositiveDivisions', 'XMLSimpleTypePositiveIntegerOrEmpty',
                                               'XMLSimpleTypeRotationDegrees', 'XMLSimpleTypeSemiPitched',
                                               'XMLSimpleTypeSmuflGlyphName', 'XMLSimpleTypeSmuflAccidentalGlyphName',
                                               'XMLSimpleTypeSmuflCodaGlyphName', 'XMLSimpleTypeSmuflLyricsGlyphName',
                                               'XMLSimpleTypeSmuflPictogramGlyphName', 'XMLSimpleTypeSmuflSegnoGlyphName',
                                               'XMLSimpleTypeSmuflWavyLineGlyphName', 'XMLSimpleTypeStartNote',
                                               'XMLSimpleTypeStartStop', 'XMLSimpleTypeStartStopContinue',
                                               'XMLSimpleTypeStartStopSingle', 'XMLSimpleTypeStringNumber',
                                               'XMLSimpleTypeSymbolSize', 'XMLSimpleTypeTenths', 'XMLSimpleTypeTextDirection',
                                               'XMLSimpleTypeTiedType', 'XMLSimpleTypeTimeOnly', 'XMLSimpleTypeTopBottom',
                                               'XMLSimpleTypeTremoloType', 'XMLSimpleTypeTrillBeats', 'XMLSimpleTypeTrillStep',
                                               'XMLSimpleTypeTwoNoteTurn', 'XMLSimpleTypeUpDown', 'XMLSimpleTypeUprightInverted',
                                               'XMLSimpleTypeValign', 'XMLSimpleTypeValignImage', 'XMLSimpleTypeYesNo',
                                               'XMLSimpleTypeYesNoNumber', 'XMLSimpleTypeYyyyMmDd',
                                               'XMLSimpleTypeCancelLocation', 'XMLSimpleTypeClefSign', 'XMLSimpleTypeFifths',
                                               'XMLSimpleTypeMode', 'XMLSimpleTypeShowFrets', 'XMLSimpleTypeStaffLine',
                                               'XMLSimpleTypeStaffLinePosition', 'XMLSimpleTypeStaffNumber',
                                               'XMLSimpleTypeStaffType', 'XMLSimpleTypeTimeRelation',
                                               'XMLSimpleTypeTimeSeparator', 'XMLSimpleTypeTimeSymbol',
                                               'XMLSimpleTypeBackwardForward', 'XMLSimpleTypeBarStyle',
                                               'XMLSimpleTypeEndingNumber', 'XMLSimpleTypeRightLeftMiddle',
                                               'XMLSimpleTypeStartStopDiscontinue', 'XMLSimpleTypeWinged',
                                               'XMLSimpleTypeAccordionMiddle', 'XMLSimpleTypeBeaterValue',
                                               'XMLSimpleTypeDegreeSymbolValue', 'XMLSimpleTypeDegreeTypeValue',
                                               'XMLSimpleTypeEffectValue', 'XMLSimpleTypeGlassValue',
                                               'XMLSimpleTypeHarmonyArrangement', 'XMLSimpleTypeHarmonyType',
                                               'XMLSimpleTypeKindValue', 'XMLSimpleTypeLineEnd',
                                               'XMLSimpleTypeMeasureNumberingValue', 'XMLSimpleTypeMembraneValue',
                                               'XMLSimpleTypeMetalValue', 'XMLSimpleTypeMilliseconds',
                                               'XMLSimpleTypeNumeralMode', 'XMLSimpleTypeOnOff', 'XMLSimpleTypePedalType',
                                               'XMLSimpleTypePitchedValue', 'XMLSimpleTypePrincipalVoiceSymbol',
                                               'XMLSimpleTypeStaffDivideSymbol', 'XMLSimpleTypeStartStopChangeContinue',
                                               'XMLSimpleTypeSyncType', 'XMLSimpleTypeSystemRelationNumber',
                                               'XMLSimpleTypeSystemRelation', 'XMLSimpleTypeTipDirection',
                                               'XMLSimpleTypeStickLocation', 'XMLSimpleTypeStickMaterial',
                                               'XMLSimpleTypeStickType', 'XMLSimpleTypeUpDownStopContinue',
                                               'XMLSimpleTypeWedgeType', 'XMLSimpleTypeWoodValue', 'XMLSimpleTypeDistanceType',
                                               'XMLSimpleTypeGlyphType', 'XMLSimpleTypeLineWidthType', 'XMLSimpleTypeMarginType',
                                               'XMLSimpleTypeMillimeters', 'XMLSimpleTypeNoteSizeType',
                                               'XMLSimpleTypeAccidentalValue', 'XMLSimpleTypeArrowDirection',
                                               'XMLSimpleTypeArrowStyle', 'XMLSimpleTypeBeamValue', 'XMLSimpleTypeBendShape',
                                               'XMLSimpleTypeBreathMarkValue', 'XMLSimpleTypeCaesuraValue',
                                               'XMLSimpleTypeCircularArrow', 'XMLSimpleTypeFan', 'XMLSimpleTypeHandbellValue',
                                               'XMLSimpleTypeHarmonClosedLocation', 'XMLSimpleTypeHarmonClosedValue',
                                               'XMLSimpleTypeHoleClosedLocation', 'XMLSimpleTypeHoleClosedValue',
                                               'XMLSimpleTypeNoteTypeValue', 'XMLSimpleTypeNoteheadValue', 'XMLSimpleTypeOctave',
                                               'XMLSimpleTypeSemitones', 'XMLSimpleTypeShowTuplet', 'XMLSimpleTypeStemValue',
                                               'XMLSimpleTypeStep', 'XMLSimpleTypeSyllabic', 'XMLSimpleTypeTapHand',
                                               'XMLSimpleTypeTremoloMarks', 'XMLSimpleTypeGroupBarlineValue',
                                               'XMLSimpleTypeGroupSymbolValue', 'XMLSimpleTypeMeasureText',
                                               'XMLSimpleTypeSwingTypeValue']

    def test_generated_simple_type_xsd_snippet(self):
        """
        Test that the instance of an in module musicxml.types.simpletype generated class can show corresponding xsd
        show its version
        """
        expected = """<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="above-below">
		<xs:annotation>
			<xs:documentation>The above-below type is used to indicate whether one element appears above or below another element.</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:token">
			<xs:enumeration value="above" />
			<xs:enumeration value="below" />
		</xs:restriction>
	</xs:simpleType>
"""
        assert XMLSimpleTypeAboveBelow.get_xsd() == expected

    def test_generated_simple_type_doc_string_from_annotation(self):
        """
        Test that the instance of an in module musicxml.types.simpletype generated class has a documentation string
        matching its xsd annotation
        """
        assert isinstance(XMLSimpleTypeAboveBelow, type(XMLSimpleType))
        assert XMLSimpleTypeAboveBelow.__doc__ == 'The above-below type is used to indicate whether one element appears ' \
                                                  'above or below another element.'

    def test_simple_type_xsd_is_converted_to_classes(self):
        """
        Test that all XMLSimpleType classes are generated
        """
        for simple_type in self.all_simple_type_xsd_elements:
            module = importlib.import_module('musicxml.types.simpletype')
            simple_type_class = getattr(module, simple_type.xml_tree_class_name)
            assert simple_type.xml_tree_class_name == simple_type_class.__name__

    def test_base_classes_are_implemented(self):
        """
        Test that all needed base classes are actually inherited by all XMLSimpleType classes
        """
        for simple_type in self.all_simple_type_xsd_elements:
            module = importlib.import_module('musicxml.types.simpletype')
            simpletype_class = getattr(module, simple_type.xml_tree_class_name)
            mro = simpletype_class.__mro__
            for base_class_name in simple_type.xml_tree_base_class_names:
                base_class = getattr(module, base_class_name)
                assert base_class in mro

    # Test Basic XMLSimpleType classes which are created manually

    def test_xs_integer(self):
        XMLSimpleTypeInteger(0)
        XMLSimpleTypeInteger(-4)
        XMLSimpleTypeInteger(3)

        with self.assertRaises(TypeError):
            XMLSimpleTypeInteger(None)
        with self.assertRaises(TypeError):
            XMLSimpleTypeInteger('string')
        with self.assertRaises(TypeError):
            XMLSimpleTypeInteger(1.4)

    def test_xs_non_negative_integer(self):
        XMLSimpleTypeNonNegativeInteger(0)
        XMLSimpleTypeNonNegativeInteger(3)

        with self.assertRaises(TypeError):
            XMLSimpleTypeNonNegativeInteger(1.4)
        with self.assertRaises(TypeError):
            XMLSimpleTypeNonNegativeInteger(-1.4)

        with self.assertRaises(ValueError):
            XMLSimpleTypeNonNegativeInteger(-4)

    def test_xs_positive_integer(self):
        XMLSimpleTypePositiveInteger(3)

        with self.assertRaises(TypeError):
            XMLSimpleTypePositiveInteger(1.4)
        with self.assertRaises(TypeError):
            XMLSimpleTypePositiveInteger(-1.4)

        with self.assertRaises(ValueError):
            XMLSimpleTypePositiveInteger(-4)
        with self.assertRaises(ValueError):
            XMLSimpleTypePositiveInteger(0)

    def test_xs_decimal(self):
        XMLSimpleTypeDecimal(1.4)
        XMLSimpleTypeDecimal(0)
        XMLSimpleTypeDecimal(-4)

        with self.assertRaises(TypeError):
            XMLSimpleTypeDecimal(None)
        with self.assertRaises(TypeError):
            XMLSimpleTypeDecimal('string')

    def test_xs_string(self):
        XMLSimpleTypeString("")
        XMLSimpleTypeString("hello")

        with self.assertRaises(TypeError):
            XMLSimpleTypeString(None)
        with self.assertRaises(TypeError):
            XMLSimpleTypeString(1)
        with self.assertRaises(TypeError):
            XMLSimpleTypeString(1.5)

    def test_xs_token(self):
        with self.assertRaises(TypeError):
            XMLSimpleTypeToken(1)
        XMLSimpleTypeString("Hello Alfons")
        assert XMLSimpleTypeToken("Hello\tAlfons").value == "Hello Alfons"
        assert XMLSimpleTypeToken("Hello\rAlfons").value == "Hello Alfons"
        assert XMLSimpleTypeToken("Hello\nAlfons").value == "Hello Alfons"
        assert XMLSimpleTypeToken("Hello    Alfons").value == "Hello Alfons"
        assert XMLSimpleTypeToken("Hello\n  Alfons").value == "Hello Alfons"

    def test_xs_NMTOKEN(self):
        XMLSimpleTypeNMTOKEN("Hello_Alfons")
        XMLSimpleTypeNMTOKEN("HeL1.o")
        XMLSimpleTypeNMTOKEN("HeL1:._-o")
        XMLSimpleTypeNMTOKEN("ÖÜöüäÄ:._-o")

        with self.assertRaises(TypeError):
            XMLSimpleTypeNMTOKEN(1)

        with self.assertRaises(ValueError):
            XMLSimpleTypeNMTOKEN("Hello Alfons")
        with self.assertRaises(ValueError):
            XMLSimpleTypeNMTOKEN("Hello\tAlfons")
        with self.assertRaises(ValueError):
            XMLSimpleTypeNMTOKEN("Hello,Alfons")
        with self.assertRaises(ValueError):
            XMLSimpleTypeNMTOKEN("Hello;Alfons")
        with self.assertRaises(ValueError):
            XMLSimpleTypeNMTOKEN("Hello%Alfons")
        with self.assertRaises(ValueError):
            XMLSimpleTypeNMTOKEN("Hello|Alfons")
        with self.assertRaises(ValueError):
            XMLSimpleTypeNMTOKEN("Hello'Alfons")
        with self.assertRaises(ValueError):
            XMLSimpleTypeNMTOKEN("Hello?Alfons")
        with self.assertRaises(ValueError):
            XMLSimpleTypeNMTOKEN("HelloAlfons!")

    def test_xs_date(self):
        XMLSimpleTypeDate('1982-11-23+07:00')
        XMLSimpleTypeDate('1982-11-23')

        with self.assertRaises(TypeError):
            XMLSimpleTypeDate(19821223)

        with self.assertRaises(ValueError):
            XMLSimpleTypeDate('1982-21-23')
        with self.assertRaises(ValueError):
            XMLSimpleTypeDate('19822123')

    # Test XMLSimpleType classes with union restrictions
    def test_simple_type_number_or_normal(self):
        """
        Test if the intern simple format of restriction is applied
        """
        """
        <xs:simpleType name="number-or-normal">
            <xs:annotation>
                <xs:documentation>The number-or-normal values can be either a decimal number or the string "normal". This is used by the line-height and letter-spacing attributes.</xs:documentation>
            </xs:annotation>
            <xs:union memberTypes="xs:decimal">
                <xs:simpleType>
                    <xs:restriction base="xs:token">
                        <xs:enumeration value="normal"/>
                    </xs:restriction>
                </xs:simpleType>
            </xs:union>
        </xs:simpleType>
        """
        XMLSimpleTypeNumberOrNormal(1)
        XMLSimpleTypeNumberOrNormal(1.5)
        XMLSimpleTypeNumberOrNormal(-1)
        XMLSimpleTypeNumberOrNormal(-1.5)
        XMLSimpleTypeNumberOrNormal(0)
        XMLSimpleTypeNumberOrNormal('normal')

        with self.assertRaises(TypeError):
            XMLSimpleTypeNumberOrNormal('something')

    def test_simple_type_positive_integer_or_empty(self):
        """
        Test if the intern simple format of restriction is applied
        """
        """
        <xs:simpleType name="positive-integer-or-empty">
            <xs:annotation>
                <xs:documentation>The positive-integer-or-empty values can be either a positive integer or an empty string.</xs:documentation>
            </xs:annotation>
            <xs:union memberTypes="xs:positiveInteger">
                <xs:simpleType>
                    <xs:restriction base="xs:string">
                        <xs:enumeration value=""/>
                    </xs:restriction>
                </xs:simpleType>
            </xs:union>
        </xs:simpleType>
        """
        XMLSimpleTypePositiveIntegerOrEmpty(1)
        XMLSimpleTypePositiveIntegerOrEmpty('')

        with self.assertRaises(TypeError):
            XMLSimpleTypePositiveIntegerOrEmpty('something')
        with self.assertRaises(TypeError):
            XMLSimpleTypePositiveIntegerOrEmpty(-1.5)
        with self.assertRaises(TypeError):
            XMLSimpleTypePositiveIntegerOrEmpty(1.5)

        with self.assertRaises(ValueError):
            XMLSimpleTypePositiveIntegerOrEmpty(-1)
        with self.assertRaises(ValueError):
            XMLSimpleTypePositiveIntegerOrEmpty(0)

    def test_simple_type_measure_text_min_length(self):
        """
        Test minLength
        """
        XMLSimpleTypeMeasureText('some text')

        with self.assertRaises(TypeError):
            XMLSimpleTypeMeasureText(1)

        with self.assertRaises(ValueError):
            XMLSimpleTypeMeasureText('')

    def test_simple_type_positive_decimal(self):
        """
        Test minExclusive
        """
        XMLSimpleTypePositiveDecimal(10)

        with self.assertRaises(TypeError):
            XMLSimpleTypePositiveDecimal('hello')

        with self.assertRaises(ValueError):
            XMLSimpleTypePositiveDecimal(0)
        with self.assertRaises(ValueError):
            XMLSimpleTypePositiveDecimal(-10)

    def test_non_negative_decimal(self):
        """
        Test minInclusive
        """
        XMLSimpleTypeNonNegativeDecimal(1.4)
        XMLSimpleTypeNonNegativeDecimal(0)

        with self.assertRaises(TypeError):
            XMLSimpleTypeNonNegativeDecimal(None)
        with self.assertRaises(TypeError):
            XMLSimpleTypeNonNegativeDecimal('string')

        with self.assertRaises(ValueError):
            XMLSimpleTypeNonNegativeDecimal(-4)
        with self.assertRaises(ValueError):
            XMLSimpleTypeNonNegativeDecimal(-1.4)

    def test_beam_level(self):
        """
        Test minInclusive and maxInclusive
        """
        for x in range(1, 9):
            XMLSimpleTypeBeamLevel(x)

        with self.assertRaises(TypeError):
            XMLSimpleTypeBeamLevel(None)
        with self.assertRaises(TypeError):
            XMLSimpleTypeBeamLevel('string')
        with self.assertRaises(TypeError):
            XMLSimpleTypeBeamLevel(1.4)

        with self.assertRaises(ValueError):
            XMLSimpleTypeBeamLevel(-4)
        with self.assertRaises(ValueError):
            XMLSimpleTypeBeamLevel(0)
        with self.assertRaises(ValueError):
            XMLSimpleTypeBeamLevel(9)

    def test_simple_type_validator_from_restriction(self):
        """
        Test that the instance of an in module musicxml.types.simpletype generated class has a validator corresponding to its xsd
        restriction
        """
        XMLSimpleTypeAboveBelow('above')
        XMLSimpleTypeAboveBelow('below')

        with self.assertRaises(TypeError):
            XMLSimpleTypeAboveBelow(None)
        with self.assertRaises(TypeError):
            XMLSimpleTypeAboveBelow(1)

        with self.assertRaises(ValueError):
            XMLSimpleTypeAboveBelow('side')

    # Test XMLSimpleType classes with pattern restrictions
    def test_simple_type_color(self):
        """
        <xs:simpleType name="color">
            <xs:annotation>
                <xs:documentation>The color type indicates the color of an element. Color may be represented as hexadecimal RGB triples, as
                in HTML, or as hexadecimal ARGB tuples, with the A indicating alpha of transparency. An alpha value of 00 is totally
                transparent; FF is totally opaque. If RGB is used, the A value is assumed to be FF.
                For instance, the RGB value "#800080" represents purple. An ARGB value of "#40800080" would be a transparent purple.
                As in SVG 1.1, colors are defined in terms of the sRGB color space (IEC 61966).</xs:documentation>
            </xs:annotation>
            <xs:restriction base="xs:token">
                <xs:pattern value="#[\dA-F]{6}([\dA-F][\dA-F])?"/>
            </xs:restriction>
        </xs:simpleType>
        """
        XMLSimpleTypeColor('#40800080')

        with self.assertRaises(TypeError):
            XMLSimpleTypeColor(None)
        with self.assertRaises(TypeError):
            XMLSimpleTypeColor(1)

        with self.assertRaises(ValueError):
            XMLSimpleTypeColor('40800080')

    def test_comma_separated_text(self):
        """
        <xs:simpleType name="comma-separated-text">
            <xs:annotation>
                <xs:documentation>The comma-separated-text type is used to specify a comma-separated list of text elements, as is used by
                    the font-family attribute.
                </xs:documentation>
            </xs:annotation>
        <xs:restriction base="xs:token">
            <xs:pattern value="[^,]+(, ?[^,]+)*"/>
            </xs:restriction>
        </xs:simpleType>
        """
        XMLSimpleTypeCommaSeparatedText('arial,times')

        with self.assertRaises(TypeError):
            XMLSimpleTypeCommaSeparatedText(None)
        with self.assertRaises(TypeError):
            XMLSimpleTypeCommaSeparatedText(1)

        with self.assertRaises(ValueError):
            XMLSimpleTypeCommaSeparatedText('arial,,times')
        with self.assertRaises(ValueError):
            XMLSimpleTypeCommaSeparatedText(',arial,times')
        with self.assertRaises(ValueError):
            XMLSimpleTypeCommaSeparatedText('arial,times,')

    def test_smufl_accidental_glyph_name(self):
        """
        <xs:simpleType name="smufl-accidental-glyph-name">
            <xs:annotation>
                <xs:documentation>The smufl-accidental-glyph-name type is used to reference a specific Standard Music Font Layout (SMuFL) accidental character. The value is a SMuFL canonical glyph name that starts with one of the strings used at the start of glyph names for SMuFL accidentals.</xs:documentation>
            </xs:annotation>
            <xs:restriction base="smufl-glyph-name">
                <xs:pattern value="(acc|medRenFla|medRenNatura|medRenShar|kievanAccidental)(\c+)"/>
            </xs:restriction>
        </xs:simpleType>
        """
        XMLSimpleTypeSmuflAccidentalGlyphName('accSomething')
        XMLSimpleTypeSmuflAccidentalGlyphName('kievanAccidentalSomething')

        with self.assertRaises(TypeError):
            XMLSimpleTypeSmuflAccidentalGlyphName(None)
        with self.assertRaises(TypeError):
            XMLSimpleTypeSmuflAccidentalGlyphName(1)

        with self.assertRaises(ValueError):
            XMLSimpleTypeSmuflAccidentalGlyphName('something')
        with self.assertRaises(ValueError):
            XMLSimpleTypeSmuflAccidentalGlyphName('kievanAccidental')
        with self.assertRaises(ValueError):
            XMLSimpleTypeSmuflAccidentalGlyphName('kievanAccidental Something')

    def test_smufl_coda_glyph_name(self):
        """
        <xs:simpleType name="smufl-coda-glyph-name">
            <xs:annotation>
                <xs:documentation>The smufl-coda-glyph-name type is used to reference a specific Standard Music Font Layout (SMuFL) coda character. The value is a SMuFL canonical glyph name that starts with coda.</xs:documentation>
            </xs:annotation>
            <xs:restriction base="smufl-glyph-name">
                <xs:pattern value="coda\c*"/>
            </xs:restriction>
        </xs:simpleType>
        """
        XMLSimpleTypeSmuflCodaGlyphName('codaSomething')
        XMLSimpleTypeSmuflCodaGlyphName('coda')

        with self.assertRaises(TypeError):
            XMLSimpleTypeSmuflCodaGlyphName(None)
        with self.assertRaises(TypeError):
            XMLSimpleTypeSmuflCodaGlyphName(1)

        with self.assertRaises(ValueError):
            XMLSimpleTypeSmuflAccidentalGlyphName('something')
        with self.assertRaises(ValueError):
            XMLSimpleTypeSmuflAccidentalGlyphName('codaSomething Something')

    def test_smufl_lyrics_glyph_name(self):
        """
        <xs:simpleType name="smufl-lyrics-glyph-name">
            <xs:annotation>
                <xs:documentation>The smufl-lyrics-glyph-name type is used to reference a specific Standard Music Font Layout (SMuFL) lyrics elision character. The value is a SMuFL canonical glyph name that starts with lyrics.</xs:documentation>
            </xs:annotation>
            <xs:restriction base="smufl-glyph-name">
                <xs:pattern value="lyrics\c+"/>
            </xs:restriction>
        </xs:simpleType>
        """
        XMLSimpleTypeSmuflLyricsGlyphName('lyricsSomething')

        with self.assertRaises(TypeError):
            XMLSimpleTypeSmuflLyricsGlyphName(None)
        with self.assertRaises(TypeError):
            XMLSimpleTypeSmuflLyricsGlyphName(1)

        with self.assertRaises(ValueError):
            XMLSimpleTypeSmuflLyricsGlyphName('something')
        with self.assertRaises(ValueError):
            XMLSimpleTypeSmuflLyricsGlyphName('lyrics')
        with self.assertRaises(ValueError):
            XMLSimpleTypeSmuflLyricsGlyphName('lyrics Something')

    def test_smufl_wavy_line_glyph_name(self):
        """
        <xs:simpleType name="smufl-wavy-line-glyph-name">
            <xs:annotation>
                <xs:documentation>The smufl-wavy-line-glyph-name type is used to reference a specific Standard Music Font Layout (SMuFL) wavy line character. The value is a SMuFL canonical glyph name that either starts with wiggle, or begins with guitar and ends with VibratoStroke. This includes all the glyphs in the Multi-segment lines range, excluding the beam glyphs.</xs:documentation>
            </xs:annotation>
            <xs:restriction base="smufl-glyph-name">
                <xs:pattern value="(wiggle\c+)|(guitar\c*VibratoStroke)"/>
            </xs:restriction>
        </xs:simpleType>
        """
        XMLSimpleTypeSmuflWavyLineGlyphName('wiggleSomething')
        XMLSimpleTypeSmuflWavyLineGlyphName('guitarSomethingVibratoStroke')
        XMLSimpleTypeSmuflWavyLineGlyphName('guitarVibratoStroke')

        with self.assertRaises(TypeError):
            XMLSimpleTypeSmuflWavyLineGlyphName(None)
        with self.assertRaises(TypeError):
            XMLSimpleTypeSmuflWavyLineGlyphName(1)

        with self.assertRaises(ValueError):
            XMLSimpleTypeSmuflWavyLineGlyphName('something')
        with self.assertRaises(ValueError):
            XMLSimpleTypeSmuflWavyLineGlyphName('wiggle')
        with self.assertRaises(ValueError):
            XMLSimpleTypeSmuflWavyLineGlyphName('wiggle Something')
        with self.assertRaises(ValueError):
            XMLSimpleTypeSmuflWavyLineGlyphName('somethingVibratoStroke')
        with self.assertRaises(ValueError):
            XMLSimpleTypeSmuflWavyLineGlyphName('guitarSomething')
        with self.assertRaises(ValueError):
            XMLSimpleTypeSmuflWavyLineGlyphName('guitar')
        with self.assertRaises(ValueError):
            XMLSimpleTypeSmuflWavyLineGlyphName('VibratoStroke')

    def test_yyyy_mm_dd(self):
        """
        <xs:simpleType name="yyyy-mm-dd">
            <xs:annotation>
                <xs:documentation>Calendar dates are represented yyyy-mm-dd format, following ISO 8601. This is a W3C XML Schema date type,
                but without the optional timezone data.
            </xs:documentation>
            </xs:annotation>
            <xs:restriction base="xs:date">
                <xs:pattern value="[^:Z]*"/>
            </xs:restriction>
        </xs:simpleType>
        """
        a = XMLSimpleTypeYyyyMmDd('1982-11-23')
        # print(a.__class__.__mro__)
        with self.assertRaises(TypeError):
            XMLSimpleTypeYyyyMmDd(19821223)

        with self.assertRaises(ValueError):
            XMLSimpleTypeYyyyMmDd('1982-21-23')
        with self.assertRaises(ValueError):
            XMLSimpleTypeYyyyMmDd('19822123')
        with self.assertRaises(ValueError):
            XMLSimpleTypeYyyyMmDd('1982-11-23+07:00')
