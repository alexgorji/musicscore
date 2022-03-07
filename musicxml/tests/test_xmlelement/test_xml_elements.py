from unittest import TestCase

from musicxml.exceptions import XMLElementChildrenRequired, XSDAttributeRequiredException, XSDWrongAttribute
from musicxml.xmlelement.xmlelement import *
from musicxml.xsd.xsdcomplextype import *
from musicxml.xsd.xsdsimpletype import *


class TestXMLElements(TestCase):

    def test_element_type(self):
        el = XMLOffset(2)
        assert el.TYPE == XSDComplexTypeOffset

        el = XMLElevation(2)
        assert el.TYPE == XSDSimpleTypeRotationDegrees

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

        el = XMLOffset(2)
        # with self.assertRaises(XMLElementValueRequiredError):
        #     el.to_string()

        with self.assertRaises(TypeError):
            XMLOffset('wrong', sound='yes')

        with self.assertRaises(TypeError):
            XMLOffset(-2, sound=3).to_string()

        with self.assertRaises(ValueError):
            XMLOffset(-2, sound='maybe').to_string()

    def test_element_name(self):
        el = XMLOffset(-2)
        assert el.name == 'offset'
        el = XMLElevation(10)
        assert el.name == 'elevation'

    def test_element_with_wrong_attribute(self):
        with self.assertRaises(XSDWrongAttribute):
            XMLPartName('Part 1', dummy='no')
        el = XMLPartName('Part 1')
        with self.assertRaises(AttributeError):
            el.dummy = 'no'

    def test_xml_measure_attributes(self):
        m = XMLMeasure(number='2')
        m.text = 'hello'
        m.width = 150
        assert (m.number, m.text, m.width) == ('2', 'hello', 150)

    def test_xml_accidental_attributes(self):
        """
            complexType@name=accidental
        annotation
            documentation
        simpleContent
            extension@base=accidental-value
                attribute@name=cautionary@type=yes-no
                attribute@name=editorial@type=yes-no
                attributeGroup@ref=level-display
                attributeGroup@ref=print-style
                attribute@name=smufl@type=smufl-accidental-glyph-name
        :return:
        """
        a = XMLAccidental('sharp')
        a.cautionary = 'yes'
        assert a.cautionary == 'yes'

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
        el = XMLElevation(10)
        assert el.TYPE == XSDSimpleTypeRotationDegrees
        with self.assertRaises(TypeError):
            el.value_ = 'something'
        with self.assertRaises(ValueError):
            el.value_ = 200

        el.value_ = 170
        assert el.to_string() == '<elevation>170</elevation>\n'

    def test_element_empty(self):
        """
        Test that empty complex type is created properly
        """
        el = XMLChord()
        assert el.to_string() == '<chord />\n'

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

        pn = sp.add_child(XMLPartName('part name 1'))
        with self.assertRaises(XSDAttributeRequiredException) as err:
            el.to_string()
        assert err.exception.args[0] == 'XMLScorePart requires attribute: id'
        sp.id = 'p1'
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
        string = XMLString(2)
        assert string.TYPE == XSDComplexTypeString
        software = XMLSoftware('gaga')
        assert software.TYPE == XSDSimpleTypeString

    def test_element_with_type_and_value_as_attributes(self):
        """
        Test if an element which has attributes name type and value can be initiated without conflicts
        """
        supports = XMLSupports()
        assert supports.TYPE == XSDComplexTypeSupports
        supports.element = 'print'
        supports.type = 'yes'
        supports.value = 'yes'

    def test_xml_credit_words_attributes(self):
        """
        Test that XMLCreditWords can have attributes
        """
        cw = XMLCreditWords('something')
        assert [a.name for a in cw.TYPE.get_xsd_attributes()] == ['justify', 'default-x', 'default-y', 'relative-x', 'relative-y',
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

    def test_xml_credit(self):
        expected = """<credit page="1">
  <credit-words default-x="651" default-y="88" font-size="10" justify="center" valign="bottom">#</credit-words>
</credit>
"""
        c = XMLCredit(page=1)
        c.child_container_tree.check_requirements()
        c.add_child(XMLCreditWords('#', default_x=651, default_y=88, font_size=10, justify='center', valign='bottom'))
        assert c.to_string() == expected

    def test_xml_time_modification(self):
        expected = """<time-modification>
  <actual-notes>3</actual-notes>
  <normal-notes>2</normal-notes>
</time-modification>
"""
        tm = XMLTimeModification()
        tm.add_child(XMLActualNotes(3))
        tm.add_child(XMLNormalNotes(2))
        assert tm.to_string() == expected

    def test_xml_ending(self):
        expected = """<ending default-y="40" end-length="30" font-size="7.6" number="1" print-object="yes" type="start" />
"""
        e = XMLEnding(default_y=40, end_length=30, font_size=7.6, number='1', print_object='yes', type='start', value_="")
        assert e.to_string() == expected

    def test_get_unordered_children(self):
        """
        Test XMLElement.get_children(ordered=False) which returns a list of elements in order of their addition
        """
        n = XMLNote()
        n.add_child(XMLType('half'))
        n.add_child(XMLDuration(192))
        p = n.add_child(XMLPitch())
        p.add_child(XMLStep('F'))
        p.add_child(XMLAlter(1))
        p.add_child(XMLOctave(5))
        n.add_child(XMLTie(type='start'))
        n.add_child(XMLVoice('1'))

        n.add_child(XMLStem('up', default_y=28))
        n.add_child(XMLStaff(1))
        nn = n.add_child(XMLNotations())
        nn.add_child(XMLTied(orientation='over', type='start'))

        assert [el.__class__.__name__ for el in n.get_children(ordered=False)] == ['XMLType', 'XMLDuration', 'XMLPitch', 'XMLTie',
                                                                                   'XMLVoice',
                                                                                   'XMLStem', 'XMLStaff', 'XMLNotations']

    def test_find_children(self):
        """
        Test XMLElement.find_child or find_children (ordered=False)
        """
        """
        complexType@name=appearance
            annotation
                documentation
            sequence
                element@name=line-width@type=line-width@minOccurs=0@maxOccurs=unbounded
                element@name=note-size@type=note-size@minOccurs=0@maxOccurs=unbounded
                element@name=distance@type=distance@minOccurs=0@maxOccurs=unbounded
                element@name=glyph@type=glyph@minOccurs=0@maxOccurs=unbounded
                element@name=other-appearance@type=other-appearance@minOccurs=0@maxOccurs=unbounded
        """
        n = XMLAppearance()
        ns1 = n.add_child(XMLNoteSize(10))
        lw = n.add_child(XMLLineWidth(10))
        ns2 = n.add_child(XMLNoteSize(10))
        assert n.find_child(XMLLineWidth) == lw
        assert n.find_child('XMLLineWidth') == lw
        assert n.find_children(XMLNoteSize) == [ns1, ns2]
        assert n.find_children('XMLNoteSize') == [ns1, ns2]

    def test_barline(self):
        b = XMLBarline()
        b.add_child(XMLBarStyle('light-light'))
        expected = """<barline>
  <bar-style>light-light</bar-style>
</barline>
"""
        assert b.to_string() == expected

    def test_possible_children_names(self):
        n = XMLNote()
        assert n.possible_children_names == {'beam', 'footnote', 'accidental', 'rest', 'unpitched', 'dot', 'time-modification', 'tie',
                                             'instrument', 'level', 'notehead', 'duration', 'voice', 'stem', 'chord', 'grace',
                                             'pitch', 'lyric', 'staff', 'listen', 'notations', 'type', 'cue', 'play', 'notehead-text'}

    def test_convert_attribute_to_child(self):
        """
        Tests if a dot operator can create and add child if necessary
        """
        b = XMLBarline()
        assert b.xml_bar_style is None
        b.xml_bar_style = 'light-light'
        expected = """<barline>
  <bar-style>light-light</bar-style>
</barline>
"""
        assert b.to_string() == expected
        assert isinstance(b.xml_bar_style, XMLBarStyle)
        assert b.xml_bar_style.value_ == 'light-light'
        current_xml_bar_style = b.xml_bar_style

        b.xml_bar_style = 'light-heavy'
        assert b.xml_bar_style == current_xml_bar_style
        assert b.xml_bar_style.value_ == 'light-heavy'
        b.xml_bar_style = XMLBarStyle('regular')
        assert b.xml_bar_style.value_ == 'regular'
        assert b.xml_bar_style != current_xml_bar_style
        m = XMLMeasure()
        assert m.attributes == {}

        m = XMLMeasure(number='1')
        m.xml_barline = XMLBarline()

        m.xml_attributes = XMLAttributes()
        assert m.attributes == {'number': '1'}
        with self.assertRaises(AttributeError):
            m.barline
        m.xml_attributes.xml_divisions = 12
        m.xml_barline.xml_bar_style = 'light-light'

        expected = """<measure number="1">
  <barline>
    <bar-style>light-light</bar-style>
  </barline>
  <attributes>
    <divisions>12</divisions>
  </attributes>
</measure>
"""
        assert m.to_string() == expected

    def test_remove_child(self):
        """
        Test if element's can be removed
        """
        b = XMLBarline()
        b.xml_bar_style = 'light-light'
        expected = """<barline>
  <bar-style>light-light</bar-style>
</barline>
"""
        assert b.to_string() == expected
        b.remove(b.xml_bar_style)
        expected = """<barline />
"""
        assert b.to_string() == expected
        assert b.xml_bar_style is None
        b.xml_bar_style = 'light-light'
        assert b.xml_bar_style is not None
        b.xml_bar_style = None
        assert b.xml_bar_style is None
        assert b.get_children() == []
        expected = """<barline />
"""
        assert b.to_string() == expected

    def test_change_children(self):
        """
        Test if changing children directly influences parent's et_xml_element
        """
        n = XMLNote()
        n.xml_duration = 2
        p = n.xml_pitch = XMLPitch()
        p.xml_step = 'G'
        p.xml_alter = -1
        p.xml_octave = 4
        expected = """<note>
  <pitch>
    <step>G</step>
    <alter>-1</alter>
    <octave>4</octave>
  </pitch>
  <duration>2</duration>
</note>
"""
        assert n.to_string() == expected
        p.xml_alter = None
        expected = """<note>
  <pitch>
    <step>G</step>
    <octave>4</octave>
  </pitch>
  <duration>2</duration>
</note>
"""
        assert n.to_string() == expected

    def test_remove_choices_chosen_element(self):
        n = XMLNote()
        n.xml_duration = 2
        p = n.xml_pitch = XMLPitch()
        p.xml_step = 'G'
        p.xml_alter = -1
        p.xml_octave = 4
        choice_container = p.parent_xsd_element.parent_container.get_parent()
        assert choice_container.chosen_child == p.parent_xsd_element.parent_container
        n.remove(n.xml_pitch)
        assert choice_container.chosen_child is None

    def test_remove_pitch_add_rest(self):
        n = XMLNote()
        n.xml_duration = 2
        p = n.xml_pitch = XMLPitch()
        p.xml_step = 'G'
        p.xml_alter = -1
        p.xml_octave = 4
        n.remove(n.xml_pitch)
        n.add_child(XMLRest())
        expected = """<note>
  <rest />
  <duration>2</duration>
</note>
"""
        assert n.to_string() == expected

    def test_remove_element_and_check_child_container(self):
        """
        Test if after removing an element roots container is checked again.
        """
        n = XMLNote()
        n.xml_duration = 1
        with self.assertRaises(XMLElementChildrenRequired):
            n.to_string()
        n.xml_rest = XMLRest()
        n.to_string()
        n.remove(n.xml_rest)
        with self.assertRaises(XMLElementChildrenRequired):
            n.to_string()

    def test_attributes_underline(self):
        """
        Test if note can set and get attributes via dot operator
        """
        n = XMLNote()
        n.xml_rest = XMLRest()
        n.xml_duration = 2

        assert n.attack is None
        n.attack = 10
        assert n.attack == 10
        assert n.print_leger is None
        n.print_leger = 'yes'
        assert n.print_leger == 'yes'
        n.relative_x = 10
        assert n.relative_x == 10
        expected = """<note attack="10" print-leger="yes" relative-x="10">
  <rest />
  <duration>2</duration>
</note>
"""
        assert n.to_string() == expected

    def test_attributes_none(self):
        n = XMLNote(relative_x=10)
        n.xml_rest = XMLRest()
        n.xml_duration = 2
        n.print_leger = 'yes'
        n.relative_x = 10
        n.print_leger = None
        expected = """<note relative-x="10">
  <rest />
  <duration>2</duration>
</note>
"""
        assert n.to_string() == expected

    def test_xml_type_restrictions(self):
        with self.assertRaises(ValueError):
            XSDSimpleTypeNoteTypeValue('bla')
        with self.assertRaises(ValueError):
            XSDComplexTypeNoteType('bla')
        with self.assertRaises(ValueError):
            XMLType('bla')
        t = XMLType('whole')
        expected = """<type>whole</type>
"""
        assert t.to_string() == expected

    def test_xml_with_complex_content(self):
        """
        Test if value of a complex type is checked according to the core complex content
        """
        mt = XMLMetronomeTuplet()
        with self.assertRaises(XMLElementChildrenRequired):
            mt.to_string()
        mt.xml_actual_notes = 3
        mt.xml_normal_notes = 2
        with self.assertRaises(XSDAttributeRequiredException):
            mt.to_string()
        mt.type = 'start'
        expected = """<metronome-tuplet type="start">
  <actual-notes>3</actual-notes>
  <normal-notes>2</normal-notes>
</metronome-tuplet>
"""
        assert mt.to_string() == expected

    def test_xml_child_get_parent(self):
        mt = XMLMetronomeTuplet()
        an = mt.add_child(XMLActualNotes(3))
        mt.xml_normal_notes = 2
        assert an.get_parent() == mt
        assert mt.xml_normal_notes.get_parent() == mt
        assert mt.xml_normal_notes.up == mt

    def test_xml_remove_one_child_of_multiple_occurs(self):
        t = XMLTime()
        t.add_child(XMLBeats('3'))
        t.add_child(XMLBeatType('4'))
        t.add_child(XMLBeats('2'))
        t.add_child(XMLBeatType('4'))
        expected = """<time>
  <beats>3</beats>
  <beat-type>4</beat-type>
  <beats>2</beats>
  <beat-type>4</beat-type>
</time>
"""
        assert t.to_string() == expected
        t.remove(t.find_children("XMLBeats")[1])
        t.remove(t.find_children("XMLBeatType")[1])
        expected = """<time>
  <beats>3</beats>
  <beat-type>4</beat-type>
</time>
"""
        assert t.to_string() == expected
        t.add_child(XMLBeats('2'))
        t.add_child(XMLBeatType('4'))
        t.remove(t.find_children("XMLBeats")[0])
        t.remove(t.find_children("XMLBeatType")[0])
        expected = """<time>
  <beats>2</beats>
  <beat-type>4</beat-type>
</time>
"""
        assert t.to_string() == expected

    def test_set_value_to_None(self):
        st = XMLStaff(1)
        assert st.value_ == 1
        st.value_ = 2
        assert st.value_ == 2
        st.value_ = 3
        assert st.value_ == 3
        expected = """<staff>3</staff>
"""
        assert st.to_string() == expected

    def test_xml_notations(self):
        n = XMLNotations()
        t1 = n.add_child(XMLTied(type='stop'))
        t2 = n.add_child(XMLTied(type='start'))
        expected = """<notations>
  <tied type="stop" />
  <tied type="start" />
</notations>
"""
        assert n.to_string() == expected
        t1.up.remove(t1)
        expected = """<notations>
  <tied type="start" />
</notations>
"""
        assert n.to_string() == expected

    def test_xml_articulations(self):
        n = XMLNotations()
        a = n.add_child(XMLArticulations())
        a.add_child(XMLAccent())
        a.add_child(XMLStaccato())
        expected = """<notations>
  <articulations>
    <accent />
    <staccato />
  </articulations>
</notations>
"""
        assert n.to_string() == expected

    def test_xml_fret(self):
        """
        Test if a value is required
        """
        with self.assertRaises(TypeError):
            f = XMLFret()
        f = XMLFret(value_=2)
        expected = """<fret>2</fret>
"""
        assert f.to_string() == expected

    def test_xml_xsd_check_false(self):
        """
        Test if xsd checking can be turned off.
        """
        p = XMLPart(id='p1', xsd_check=False)
        p.add_child(XMLTie())
        p.add_child(XMLKey())
        expected = """<part id="p1">
  <tie />
  <key />
</part>
"""
        assert p.to_string() == expected

    def test_xml_xsd_check_false_remove_child(self):
        """
        Test if removing child can take place if xsd checking is False.
        """
        p = XMLPart(id='p1', xsd_check=False)
        t = p.add_child(XMLTie())
        p.add_child(XMLKey())
        p.remove(t)
        expected = """<part id="p1">
  <key />
</part>
"""
        assert p.to_string() == expected

    def test_xml_xsd_check_false_replace_child(self):
        """
        Test if replacing child can take place if xsd checking is False.
        """
        p = XMLPart(id='p1', xsd_check=False)
        t = p.add_child(XMLTie())
        p.add_child(XMLKey())
        time = p.replace_child(t, XMLTime())
        time.add_child(XMLSenzaMisura())
        expected = """<part id="p1">
  <time>
    <senza-misura />
  </time>
  <key />
</part>
"""
        assert p.to_string() == expected
