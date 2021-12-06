import importlib
from musicxml.util.helperclasses import MusicXmlTestCase
from musicxml.types.simpletype import XMLSimpleType, XMLSimpleTypeAboveBelow, XMLSimpleTypeNumberOrNormal, \
    XMLSimpleTypePositiveIntegerOrEmpty, XMLSimpleTypeNonNegativeDecimal, XMLSimpleTypeDecimal, XMLSimpleTypeInteger, \
    XMLSimpleTypeNonNegativeInteger, XMLSimpleTypePositiveInteger, XMLSimpleTypeString, XMLSimpleTypeToken, \
    XMLSimpleTypeNMTOKEN, XMLSimpleTypeDate, XMLSimpleTypeMeasureText, XMLSimpleTypePositiveDecimal, \
    XMLSimpleTypeBeamLevel, XMLSimpleTypeColor, XMLSimpleTypeCommaSeparatedText, XMLSimpleTypeSmuflAccidentalGlyphName, \
    XMLSimpleTypeSmuflCodaGlyphName, XMLSimpleTypeSmuflLyricsGlyphName, XMLSimpleTypeSmuflWavyLineGlyphName, \
    XMLSimpleTypeYyyyMmDd


class TestSimpleTypes(MusicXmlTestCase):

    def test_simple_type_XMLElement_generator_xsd_snippet(self):
        """
        Test that the instance of with XMLElementGenerator generated class can show corresponding xsd snippet and
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

    def test_simple_type_XMLElement_generator_doc_string_from_annotation(self):
        """
        Test that the instance of with with XMLElementGenerator generated class has a documentation string
        matching its xsd annotation
        """
        assert isinstance(XMLSimpleTypeAboveBelow, type(XMLSimpleType))
        assert XMLSimpleTypeAboveBelow.__doc__ == 'The above-below type is used to indicate whether one element appears ' \
                                                  'above or below another element.'

    def test_simple_type_xsd_is_converted_to_classes(self):
        for simple_type in self.all_simple_type_elements:
            module = importlib.import_module('musicxml.types.simpletype')
            simple_type_class = getattr(module, simple_type.music_xml_class_name)
            assert simple_type.music_xml_class_name == simple_type_class.__name__

    def test_base_classes_are_implemented(self):
        for simple_type in self.all_simple_type_elements:
            module = importlib.import_module('musicxml.types.simpletype')
            simpletype_class = getattr(module, simple_type.music_xml_class_name)
            mro = simpletype_class.__mro__
            for base_class_name in simple_type.music_xml_base_class_names:
                base_class = getattr(module, base_class_name)
                assert base_class in mro

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

    def test_simple_type_number_or_normal(self):
        """
        Test if the intern simple format of restriction is applied
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
        Test that the instance of with XMLElementGenerator generated class has a validator corresponding to its xsd
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

    # patterns
    def test_simple_type_color(self):
        XMLSimpleTypeColor('#40800080')

        with self.assertRaises(TypeError):
            XMLSimpleTypeColor(None)
        with self.assertRaises(TypeError):
            XMLSimpleTypeColor(1)

        with self.assertRaises(ValueError):
            XMLSimpleTypeColor('40800080')

    def test_comma_separated_text(self):
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
        a = XMLSimpleTypeYyyyMmDd('1982-11-23')
        print(a.__class__.__mro__)
        with self.assertRaises(TypeError):
            XMLSimpleTypeYyyyMmDd(19821223)

        with self.assertRaises(ValueError):
            XMLSimpleTypeYyyyMmDd('1982-21-23')
        with self.assertRaises(ValueError):
            XMLSimpleTypeYyyyMmDd('19822123')
        with self.assertRaises(ValueError):
            XMLSimpleTypeYyyyMmDd('1982-11-23+07:00')
