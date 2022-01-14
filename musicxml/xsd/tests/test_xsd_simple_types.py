import importlib
from musicxml.util.helperclasses import MusicXmlTestCase
# from musicxml.xsd.xsdsimpletype import XSDSimpleType, xml_simple_type_class_names
#
# from musicxml.xsd.xsdsimpletype import *
from musicxml.xsd.xsdsimpletype import *
from musicxml.xsd.xsdcomplextype import *


class TestSimpleTypes(MusicXmlTestCase):

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
        assert XSDSimpleTypeAboveBelow.get_xsd() == expected

    def test_generate_simple_type_is_descendent_of_simple_type(self):
        assert isinstance(XSDSimpleTypeAboveBelow('above'), XSDSimpleType)

    def test_generated_simple_type_doc_string_from_annotation(self):
        """
        Test that the instance of an in module musicxml.types.simpletype generated class has a documentation string
        matching its xsd annotation
        """

        assert XSDSimpleTypeAboveBelow.__doc__ == 'The above-below type is used to indicate whether one element appears ' \
                                                  'above or below another element.'

    # Test Basic XSDSimpleType classes which are created manually

    def test_xs_integer(self):
        XSDSimpleTypeInteger(0)
        XSDSimpleTypeInteger(-4)
        XSDSimpleTypeInteger(3)

        with self.assertRaises(TypeError):
            XSDSimpleTypeInteger(None)
        with self.assertRaises(TypeError):
            XSDSimpleTypeInteger('string')
        with self.assertRaises(TypeError):
            XSDSimpleTypeInteger(1.4)

    def test_xs_non_negative_integer(self):
        XSDSimpleTypeNonNegativeInteger(0)
        XSDSimpleTypeNonNegativeInteger(3)

        with self.assertRaises(TypeError):
            XSDSimpleTypeNonNegativeInteger(1.4)
        with self.assertRaises(TypeError):
            XSDSimpleTypeNonNegativeInteger(-1.4)

        with self.assertRaises(ValueError):
            XSDSimpleTypeNonNegativeInteger(-4)

    def test_xs_positive_integer(self):
        XSDSimpleTypePositiveInteger(3)

        with self.assertRaises(TypeError):
            XSDSimpleTypePositiveInteger(1.4)
        with self.assertRaises(TypeError):
            XSDSimpleTypePositiveInteger(-1.4)

        with self.assertRaises(ValueError):
            XSDSimpleTypePositiveInteger(-4)
        with self.assertRaises(ValueError):
            XSDSimpleTypePositiveInteger(0)

    def test_xs_decimal(self):
        XSDSimpleTypeDecimal(1.4)
        XSDSimpleTypeDecimal(0)
        XSDSimpleTypeDecimal(-4)

        with self.assertRaises(TypeError):
            XSDSimpleTypeDecimal(None)
        with self.assertRaises(TypeError):
            XSDSimpleTypeDecimal('string')

    def test_xs_string(self):
        XSDSimpleTypeString("")
        XSDSimpleTypeString("hello")

        with self.assertRaises(TypeError):
            XSDSimpleTypeString(None)
        with self.assertRaises(TypeError):
            XSDSimpleTypeString(1)
        with self.assertRaises(TypeError):
            XSDSimpleTypeString(1.5)

    def test_xs_token(self):
        with self.assertRaises(TypeError):
            XSDSimpleTypeToken(1)
        XSDSimpleTypeString("Hello Alfons")
        assert XSDSimpleTypeToken("Hello\tAlfons").value == "Hello Alfons"
        assert XSDSimpleTypeToken("Hello\rAlfons").value == "Hello Alfons"
        assert XSDSimpleTypeToken("Hello\nAlfons").value == "Hello Alfons"
        assert XSDSimpleTypeToken("Hello    Alfons").value == "Hello Alfons"
        assert XSDSimpleTypeToken("Hello\n  Alfons").value == "Hello Alfons"

    def test_xs_NMTOKEN(self):
        XSDSimpleTypeNMTOKEN("Hello_Alfons")
        XSDSimpleTypeNMTOKEN("HeL1.o")
        XSDSimpleTypeNMTOKEN("HeL1:._-o")
        XSDSimpleTypeNMTOKEN("ÖÜöüäÄ:._-o")

        with self.assertRaises(TypeError):
            XSDSimpleTypeNMTOKEN(1)

        with self.assertRaises(ValueError):
            XSDSimpleTypeNMTOKEN("Hello Alfons")
        with self.assertRaises(ValueError):
            XSDSimpleTypeNMTOKEN("Hello\tAlfons")
        with self.assertRaises(ValueError):
            XSDSimpleTypeNMTOKEN("Hello,Alfons")
        with self.assertRaises(ValueError):
            XSDSimpleTypeNMTOKEN("Hello;Alfons")
        with self.assertRaises(ValueError):
            XSDSimpleTypeNMTOKEN("Hello%Alfons")
        with self.assertRaises(ValueError):
            XSDSimpleTypeNMTOKEN("Hello|Alfons")
        with self.assertRaises(ValueError):
            XSDSimpleTypeNMTOKEN("Hello'Alfons")
        with self.assertRaises(ValueError):
            XSDSimpleTypeNMTOKEN("Hello?Alfons")
        with self.assertRaises(ValueError):
            XSDSimpleTypeNMTOKEN("HelloAlfons!")

    def test_xs_date(self):
        XSDSimpleTypeDate('1982-11-23+07:00')
        XSDSimpleTypeDate('1982-11-23')

        with self.assertRaises(TypeError):
            XSDSimpleTypeDate(19821223)

        with self.assertRaises(ValueError):
            XSDSimpleTypeDate('1982-21-23')
        with self.assertRaises(ValueError):
            XSDSimpleTypeDate('19822123')

    # Test XSDSimpleType classes with union restrictions
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
        XSDSimpleTypeNumberOrNormal(1)
        XSDSimpleTypeNumberOrNormal(1.5)
        XSDSimpleTypeNumberOrNormal(-1)
        XSDSimpleTypeNumberOrNormal(-1.5)
        XSDSimpleTypeNumberOrNormal(0)
        XSDSimpleTypeNumberOrNormal('normal')

        with self.assertRaises(TypeError):
            XSDSimpleTypeNumberOrNormal('something')

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
        XSDSimpleTypePositiveIntegerOrEmpty(1)
        XSDSimpleTypePositiveIntegerOrEmpty('')

        with self.assertRaises(TypeError):
            XSDSimpleTypePositiveIntegerOrEmpty('something')
        with self.assertRaises(TypeError):
            XSDSimpleTypePositiveIntegerOrEmpty(-1.5)
        with self.assertRaises(TypeError):
            XSDSimpleTypePositiveIntegerOrEmpty(1.5)

        with self.assertRaises(ValueError):
            XSDSimpleTypePositiveIntegerOrEmpty(-1)
        with self.assertRaises(ValueError):
            XSDSimpleTypePositiveIntegerOrEmpty(0)

    def test_simple_type_measure_text_min_length(self):
        """
        Test minLength
        """
        XSDSimpleTypeMeasureText('some text')

        with self.assertRaises(TypeError):
            XSDSimpleTypeMeasureText(1)

        with self.assertRaises(ValueError):
            XSDSimpleTypeMeasureText('')

    def test_simple_type_positive_decimal(self):
        """
        Test minExclusive
        """
        XSDSimpleTypePositiveDecimal(10)

        with self.assertRaises(TypeError):
            XSDSimpleTypePositiveDecimal('hello')

        with self.assertRaises(ValueError):
            XSDSimpleTypePositiveDecimal(0)
        with self.assertRaises(ValueError):
            XSDSimpleTypePositiveDecimal(-10)

    def test_non_negative_decimal(self):
        """
        Test minInclusive
        """
        XSDSimpleTypeNonNegativeDecimal(1.4)
        XSDSimpleTypeNonNegativeDecimal(0)

        with self.assertRaises(TypeError):
            XSDSimpleTypeNonNegativeDecimal(None)
        with self.assertRaises(TypeError):
            XSDSimpleTypeNonNegativeDecimal('string')

        with self.assertRaises(ValueError):
            XSDSimpleTypeNonNegativeDecimal(-4)
        with self.assertRaises(ValueError):
            XSDSimpleTypeNonNegativeDecimal(-1.4)

    def test_beam_level(self):
        """
        Test minInclusive and maxInclusive
        """
        for x in range(1, 9):
            XSDSimpleTypeBeamLevel(x)

        with self.assertRaises(TypeError):
            XSDSimpleTypeBeamLevel(None)
        with self.assertRaises(TypeError):
            XSDSimpleTypeBeamLevel('string')
        with self.assertRaises(TypeError):
            XSDSimpleTypeBeamLevel(1.4)

        with self.assertRaises(ValueError):
            XSDSimpleTypeBeamLevel(-4)
        with self.assertRaises(ValueError):
            XSDSimpleTypeBeamLevel(0)
        with self.assertRaises(ValueError):
            XSDSimpleTypeBeamLevel(9)

    def test_simple_type_validator_from_restriction(self):
        """
        Test that the instance of an in module musicxml.types.simpletype generated class has a validator corresponding to its xsd
        restriction
        """
        XSDSimpleTypeAboveBelow('above')
        XSDSimpleTypeAboveBelow('below')

        with self.assertRaises(TypeError):
            XSDSimpleTypeAboveBelow(None)
        with self.assertRaises(TypeError):
            XSDSimpleTypeAboveBelow(1)

        with self.assertRaises(ValueError):
            XSDSimpleTypeAboveBelow('side')

    # Test XSDSimpleType classes with pattern restrictions
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
        XSDSimpleTypeColor('#40800080')

        with self.assertRaises(TypeError):
            XSDSimpleTypeColor(None)
        with self.assertRaises(TypeError):
            XSDSimpleTypeColor(1)

        with self.assertRaises(ValueError):
            XSDSimpleTypeColor('40800080')

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
        XSDSimpleTypeCommaSeparatedText('arial,times')

        with self.assertRaises(TypeError):
            XSDSimpleTypeCommaSeparatedText(None)
        with self.assertRaises(TypeError):
            XSDSimpleTypeCommaSeparatedText(1)

        with self.assertRaises(ValueError):
            XSDSimpleTypeCommaSeparatedText('arial,,times')
        with self.assertRaises(ValueError):
            XSDSimpleTypeCommaSeparatedText(',arial,times')
        with self.assertRaises(ValueError):
            XSDSimpleTypeCommaSeparatedText('arial,times,')

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
        XSDSimpleTypeSmuflAccidentalGlyphName('accSomething')
        XSDSimpleTypeSmuflAccidentalGlyphName('kievanAccidentalSomething')

        with self.assertRaises(TypeError):
            XSDSimpleTypeSmuflAccidentalGlyphName(None)
        with self.assertRaises(TypeError):
            XSDSimpleTypeSmuflAccidentalGlyphName(1)

        with self.assertRaises(ValueError):
            XSDSimpleTypeSmuflAccidentalGlyphName('something')
        with self.assertRaises(ValueError):
            XSDSimpleTypeSmuflAccidentalGlyphName('kievanAccidental')
        with self.assertRaises(ValueError):
            XSDSimpleTypeSmuflAccidentalGlyphName('kievanAccidental Something')

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
        XSDSimpleTypeSmuflCodaGlyphName('codaSomething')
        XSDSimpleTypeSmuflCodaGlyphName('coda')

        with self.assertRaises(TypeError):
            XSDSimpleTypeSmuflCodaGlyphName(None)
        with self.assertRaises(TypeError):
            XSDSimpleTypeSmuflCodaGlyphName(1)

        with self.assertRaises(ValueError):
            XSDSimpleTypeSmuflAccidentalGlyphName('something')
        with self.assertRaises(ValueError):
            XSDSimpleTypeSmuflAccidentalGlyphName('codaSomething Something')

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
        XSDSimpleTypeSmuflLyricsGlyphName('lyricsSomething')

        with self.assertRaises(TypeError):
            XSDSimpleTypeSmuflLyricsGlyphName(None)
        with self.assertRaises(TypeError):
            XSDSimpleTypeSmuflLyricsGlyphName(1)

        with self.assertRaises(ValueError):
            XSDSimpleTypeSmuflLyricsGlyphName('something')
        with self.assertRaises(ValueError):
            XSDSimpleTypeSmuflLyricsGlyphName('lyrics')
        with self.assertRaises(ValueError):
            XSDSimpleTypeSmuflLyricsGlyphName('lyrics Something')

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
        XSDSimpleTypeSmuflWavyLineGlyphName('wiggleSomething')
        XSDSimpleTypeSmuflWavyLineGlyphName('guitarSomethingVibratoStroke')
        XSDSimpleTypeSmuflWavyLineGlyphName('guitarVibratoStroke')

        with self.assertRaises(TypeError):
            XSDSimpleTypeSmuflWavyLineGlyphName(None)
        with self.assertRaises(TypeError):
            XSDSimpleTypeSmuflWavyLineGlyphName(1)

        with self.assertRaises(ValueError):
            XSDSimpleTypeSmuflWavyLineGlyphName('something')
        with self.assertRaises(ValueError):
            XSDSimpleTypeSmuflWavyLineGlyphName('wiggle')
        with self.assertRaises(ValueError):
            XSDSimpleTypeSmuflWavyLineGlyphName('wiggle Something')
        with self.assertRaises(ValueError):
            XSDSimpleTypeSmuflWavyLineGlyphName('somethingVibratoStroke')
        with self.assertRaises(ValueError):
            XSDSimpleTypeSmuflWavyLineGlyphName('guitarSomething')
        with self.assertRaises(ValueError):
            XSDSimpleTypeSmuflWavyLineGlyphName('guitar')
        with self.assertRaises(ValueError):
            XSDSimpleTypeSmuflWavyLineGlyphName('VibratoStroke')

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
        a = XSDSimpleTypeYyyyMmDd('1982-11-23')
        # print(a.__class__.__mro__)
        with self.assertRaises(TypeError):
            XSDSimpleTypeYyyyMmDd(19821223)

        with self.assertRaises(ValueError):
            XSDSimpleTypeYyyyMmDd('1982-21-23')
        with self.assertRaises(ValueError):
            XSDSimpleTypeYyyyMmDd('19822123')
        with self.assertRaises(ValueError):
            XSDSimpleTypeYyyyMmDd('1982-11-23+07:00')

    def test_tenths(self):
        XSDSimpleTypeDecimal(10)
        XSDSimpleTypeTenths(10)
        with self.assertRaises(TypeError):
            XSDSimpleTypeTenths('10')

    def test_yes_no(self):
        XSDSimpleTypeYesNo('yes')
        XSDSimpleTypeYesNo('no')
        with self.assertRaises(ValueError):
            XSDSimpleTypeYesNo('maybe')

    def test_yes_no_number(self):
        XSDSimpleTypeYesNoNumber('yes')
        XSDSimpleTypeYesNoNumber('no')
        with self.assertRaises(ValueError):
            XSDSimpleTypeYesNoNumber('maybe')
        XSDSimpleTypeYesNoNumber(10)
        with self.assertRaises(TypeError):
            XSDSimpleTypeYesNoNumber([123])

    def test_font_size(self):
        XSDSimpleTypeFontSize(12)
        for size in ['xx-small', 'x-small', 'small', 'large', 'x-large', 'xx-large']:
            XSDSimpleTypeFontSize(size)
        XSDSimpleTypeFontSize(12)
        with self.assertRaises(TypeError) as err:
            XSDSimpleTypeFontSize([12, 3])
        with self.assertRaises(ValueError):
            XSDSimpleTypeFontSize('xxxx-large')

    def test_number_or_normal(self):
        XSDSimpleTypeNumberOrNormal(12)
        XSDSimpleTypeNumberOrNormal('normal')
        with self.assertRaises(TypeError):
            XSDSimpleTypeNumberOrNormal('12')
        with self.assertRaises(TypeError):
            XSDSimpleTypeNumberOrNormal([1, 2, 3])

    def test_positive_integer_empty(self):
        XSDSimpleTypePositiveIntegerOrEmpty(12)
        XSDSimpleTypePositiveIntegerOrEmpty()
        with self.assertRaises(ValueError):
            XSDSimpleTypePositiveIntegerOrEmpty(-12)
        with self.assertRaises(TypeError):
            XSDSimpleTypePositiveIntegerOrEmpty(10.2)
        with self.assertRaises(ValueError):
            XSDSimpleTypePositiveIntegerOrEmpty(0)
        with self.assertRaises(TypeError):
            XSDSimpleTypePositiveIntegerOrEmpty('0')

    def test_name(self):
        """
        <xs:simpleType name="Name" id="Name">
            <xs:restriction base="xs:token">
                <xs:pattern value="\i\c*"/>
            </xs:restriction>
        </xs:simpleType>
        """
        XSDSimpleTypeName('_1950-10-04_10-00')

    def test_nc_name(self):
        """
        <xs:simpleType name="NCName" id="NCName">
            <xs:restriction base="xs:Name">
                <xs:pattern value="[\i-[:]][\c-[:]]*"/>
            </xs:restriction>
<       /xs:simpleType>
        """
        XSDSimpleTypeNCName('_1950-10-04_10-00')
        with self.assertRaises(ValueError):
            XSDSimpleTypeNCName('_1950-10:04_10-00')

    def test_id(self):
        """
        <xs:simpleType name="ID" id="ID">
            <xs:restriction base="xs:NCName"/>
        </xs:simpleType>
        """
        id_ = XSDSimpleTypeID('_1950-10-04_10-00')
        assert isinstance(id_, XSDSimpleTypeNCName)
        with self.assertRaises(ValueError):
            XSDSimpleTypeID('_1950-10:04_10-00')

    def test_idref(self):
        """
        <xs:simpleType name="IDREF" id="IDREF">
            <xs:restriction base="xs:NCName"/>
        </xs:simpleType>
        """
        XSDSimpleTypeIDREF('_1950-10-04_10-00')
        with self.assertRaises(ValueError):
            XSDSimpleTypeIDREF('1')

    def test_language(self):
        """
        <xs:simpleType name="language" id="language">
        <xs:restriction base="xs:token">
            <xs:pattern
                    value="([a-zA-Z]{2}|[iI]-[a-zA-Z]+|[xX]-[a-zA-Z]{1,8})(-[a-zA-Z]{1,8})*"
                    />
            </xs:restriction>
        </xs:simpleType>
        """
        XSDSimpleTypeLanguage('fr')
        XSDSimpleTypeLanguage('fr-FR')
        XSDSimpleTypeLanguage('en')
        XSDSimpleTypeLanguage('en-US')
        with self.assertRaises(ValueError):
            XSDSimpleTypeLanguage('blabla')
