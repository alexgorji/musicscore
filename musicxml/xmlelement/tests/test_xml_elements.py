from unittest import TestCase

from musicxml.exceptions import XMLElementChildrenRequired, XMLElementValueRequiredError, XSDAttributeRequiredException, XSDWrongAttribute
from musicxml.xmlelement.xmlelement import *
from musicxml.xsd.xsdcomplextype import *
from musicxml.xsd.xsdsimpletype import *


class TestXMLElements(TestCase):

    def test_element_type(self):
        el = XMLOffset()
        assert el.type_ == XSDComplexTypeOffset

        el = XMLElevation()
        assert el.type_ == XSDSimpleTypeRotationDegrees

    def test_element_simple_content(self):
        """
        Test if complex types with a simple context (extension of a simple type) work properly in an XMLElement.
        A simple example is

        complexType@name=offset

        simpleContent
            extension@base=divisions
                attribute@name=sound@type=yes-no
        """
        el = XMLOffset(-2)
        assert el.to_string() == '<offset>-2</offset>\n'

        el = XMLOffset(-2, sound='yes')
        assert el.to_string() == '<offset sound="yes">-2</offset>\n'

        el = XMLOffset()
        with self.assertRaises(XMLElementValueRequiredError):
            el.to_string()

        with self.assertRaises(TypeError):
            XMLOffset('wrong', sound='yes')

        with self.assertRaises(TypeError):
            XMLOffset(-2, sound=3).to_string()

        with self.assertRaises(ValueError):
            XMLOffset(-2, sound='maybe').to_string()

    def test_element_name(self):
        el = XMLOffset(-2)
        assert el.name == 'offset'
        el = XMLElevation()
        assert el.name == 'elevation'

    def test_element_with_wrong_attribute(self):
        with self.assertRaises(XSDWrongAttribute):
            XMLPartName('Part 1', dummy='no')
        el = XMLPartName('Part 1')
        with self.assertRaises(XSDWrongAttribute):
            el.dummy = 'no'

    def test_element_attribute_with_hyphenated_name(self):
        el = XMLPartName('Part 1', default_x=10)
        assert el.to_string() == """<part-name default-x="10">Part 1</part-name>
"""
        el.print_object = 'no'
        assert el.to_string() == """<part-name default-x="10" print-object="no">Part 1</part-name>
"""
        el = XMLPartName('Part 1', print_object='no')
        assert el.to_string() == """<part-name print-object="no">Part 1</part-name>
"""

    def test_element_with_simple_type(self):
        """
        <xs:element name="elevation" type="rotation-degrees" minOccurs="0">
            <xs:annotation>
                <xs:documentation>The elevation and pan elements allow placing of sound in a 3-D space relative to the listener. Both are expressed in degrees ranging from -180 to 180. For elevation, 0 is level with the listener, 90 is directly above, and -90 is directly below.</xs:documentation>
            </xs:annotation>
        </xs:element>
        """
        el = XMLElevation()
        assert el.type_ == XSDSimpleTypeRotationDegrees
        with self.assertRaises(TypeError):
            el.value = 'something'
        with self.assertRaises(ValueError):
            el.value = 200
        with self.assertRaises(XMLElementValueRequiredError):
            el.to_string()

        el.value = 170
        assert el.to_string() == '<elevation>170</elevation>\n'
        assert el.__doc__ == 'The elevation and pan elements allow placing of sound in a 3-D space relative to the listener. Both are expressed in degrees ranging from -180 to 180. For elevation, 0 is level with the listener, 90 is directly above, and -90 is directly below.'

    def test_element_doc(self):
        """
        Test if an element with complex type returns its type's __doc__ as its __doc__
        Test if an element with simple type returns its xsd tree documentation as its __doc__
        """
        assert XMLOffset().__doc__ == """An offset is represented in terms of divisions, and indicates where the direction will appear relative to the current musical location. The current musical location is always within the current measure, even at the end of a measure.

The offset affects the visual appearance of the direction. If the sound attribute is "yes", then the offset affects playback and listening too. If the sound attribute is "no", then any sound or listening associated with the direction takes effect at the current location. The sound attribute is "no" by default for compatibility with earlier versions of the MusicXML format. If an element within a direction includes a default-x attribute, the offset value will be ignored when determining the appearance of that element."""

        assert XMLElevation().__doc__ == 'The elevation and pan elements allow placing of sound in a 3-D space relative to the listener. Both are expressed in degrees ranging from -180 to 180. For elevation, 0 is level with the listener, 90 is directly above, and -90 is directly below.'

    def test_element_empty(self):
        """
        Test that empty complex type is created properly
        """
        el = XMLChord()
        assert el.to_string() == '<chord />\n'

    def test_get_class_name(self):
        assert XMLPitch.get_class_name() == 'XMLPitch'
        assert XMLPitch().get_class_name() == 'XMLPitch'

    def test_sequence_indicator_children_required(self):
        """
        Test that a sequence indicator with only elements as children can verify the behavior of its corresponding element
        """
        """
        complexType@name=pitch
        sequence
            element@name=step@type=step
            element@name=alter@type=semitones@minOccurs=0
            element@name=octave@type=octave
        """

        """
        Element Pitch must have one and only one child element step and one and only one child element octave. It can have only one child 
        alter. The sequence order will be automatically set according to the sequence (step, alter, octave)
        """

        el = XMLPitch()
        with self.assertRaises(XMLElementChildrenRequired):
            el.to_string()

    def test_sequence_add_children_to_string(self):
        """
        Test that to_string function of an element with complex type and sequence works properly
        """
        el = XMLPitch()
        el.add_child(XMLStep('A'))
        el.add_child(XMLOctave(4))
        expected = """<pitch>
    <step>A</step>
    <octave>4</octave>
</pitch>
"""
        assert el.to_string() == expected

    def test_xml_element_part_list(self):
        el = XMLPartList()
        with self.assertRaises(XMLElementChildrenRequired) as err:
            el.to_string()

        assert err.exception.args[0] == 'XMLPartList requires at least following children: XMLScorePart'
        sp = el.add_child(XMLScorePart())

        with self.assertRaises(XMLElementChildrenRequired) as err:
            el.to_string()
        assert err.exception.args[0] == 'XMLScorePart requires at least following children: XMLPartName'

        pn = sp.add_child(XMLPartName())
        with self.assertRaises(XSDAttributeRequiredException) as err:
            el.to_string()
        assert err.exception.args[0] == 'XMLScorePart requires attribute: id'
        sp.id = 'p1'
        with self.assertRaises(XMLElementValueRequiredError) as err:
            el.to_string()

        assert err.exception.args[0] == 'XMLPartName requires a value.'
        pn.value = 'part name 1'
        expected = """<part-list>
    <score-part id="p1">
        <part-name>part name 1</part-name>
    </score-part>
</part-list>
"""
        assert el.to_string() == expected

    def test_order_of_children(self):
        el = XMLAttributes()
        t = el.add_child(XMLTime())
        t.add_child(XMLBeats('4'))
        t.add_child(XMLBeatType('4'))
        el.add_child(XMLDivisions(1))
        c = el.add_child(XMLClef())
        c.add_child(XMLSign('G'))
        c.add_child(XMLLine(2))
        k = el.add_child(XMLKey())
        k.add_child(XMLFifths(0))
        k.add_child(XMLMode('major'))

        expected = """<attributes>
    <divisions>1</divisions>
    <key>
        <fifths>0</fifths>
        <mode>major</mode>
    </key>
    <time>
        <beats>4</beats>
        <beat-type>4</beat-type>
    </time>
    <clef>
        <sign>G</sign>
        <line>2</line>
    </clef>
</attributes>
"""
        assert el.to_string() == expected

    def test_element_with_xs_simple_type(self):
        """
        Test if there is no conflict between simple and complex types with the same name such as:
        xs:string vs. string: xs:string is a simple type, string is a complex type.
        """
        string = XMLString()
        assert string.type_ == XSDComplexTypeString
        software = XMLSoftware()
        assert software.type_ == XSDSimpleTypeString

    def test_element_with_type_and_value_as_attributes(self):
        """
        Test if an element which has attributes name type and value can be initiated without conflicts
        """
        supports = XMLSupports()
        assert supports.type_ == XSDComplexTypeSupports
        supports.element = 'print'
        supports.type = 'yes'
        supports.value = 'yes'

    def test_xml_credit_words_attributes(self):
        """
        Test that XMLCreditWords can have attributes
        """
        cw = XMLCreditWords()
        assert [a.name for a in cw.type_.get_xsd_attributes()] == ['justify', 'default-x', 'default-y', 'relative-x', 'relative-y',
                                                                   'font-family', 'font-style', 'font-size', 'font-weight', 'color',
                                                                   'halign', 'valign', 'underline', 'overline', 'line-through', 'rotation',
                                                                   'letter-spacing', 'line-height', 'lang', 'space', 'dir', 'enclosure',
                                                                   'id']

    def test_xml_element_directive(self):
        d = XMLDirective('HU')
        d.lang = 'en'
        assert d.to_string() == '<directive lang="en">HU</directive>\n'

    def test_xml_note_with_tie(self):
        expected = """<note>
    <pitch>
        <step>F</step>
        <alter>1</alter>
        <octave>5</octave>
    </pitch>
    <duration>192</duration>
    <tie type="start" />
    <voice>1</voice>
    <type>half</type>
    <stem default-y="28">up</stem>
    <staff>1</staff>
    <notations>
        <tied orientation="over" type="start" />
    </notations>
</note>
"""
        n = XMLNote()
        p = n.add_child(XMLPitch())
        p.add_child(XMLStep('F'))
        p.add_child(XMLAlter(1))
        p.add_child(XMLOctave(5))
        n.add_child(XMLDuration(192))
        n.add_child(XMLTie(type='start'))
        n.add_child(XMLVoice('1'))
        n.add_child(XMLType('half'))
        n.add_child(XMLStem('up', default_y=28))
        n.add_child(XMLStaff(1))
        nn = n.add_child(XMLNotations())
        nn.add_child(XMLTied(orientation='over', type='start'))
        assert n.to_string() == expected

    def test_check_required_attributes(self):
        """
        Test if xml element's _check_required_attributes works properly.
        """
        br = XMLBeatRepeat()
        with self.assertRaises(XSDAttributeRequiredException):
            br._check_required_attributes()
        br.type = 'start'
        br._check_required_attributes()

    def test_font(self):
        expected = """<words default-y="-29" font-family="Arial" font-size="3" relative-x="-38">/</words>
"""
        w = XMLWords('/', default_y=-29, font_family="Arial", font_size=3, relative_x=-38)
        assert w.to_string() == expected
        expected = """<music-font font-family="Maestro,engraved" font-size="18.2" />
"""
        with self.assertRaises(ValueError):
            XMLMusicFont(font_family="Maestro,engraved", font_size="18.2")

        mf = XMLMusicFont(font_family="Maestro,engraved", font_size=18.2)
        assert mf.to_string() == expected
