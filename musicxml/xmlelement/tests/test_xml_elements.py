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
        assert err.exception.args[0] == 'XSDComplexTypeScorePart requires attribute: id'
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
        t.add_child(XMLBeats(4))
        t.add_child(XMLBeatType(4))
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