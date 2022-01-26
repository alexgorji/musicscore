from unittest import TestCase

from musicxml.exceptions import XSDWrongAttribute
from musicxml.xmlelement.xmlelement import *

from musictree.midi import Midi
from musictree.accidental import Accidental
from musictree.musictree import MusicTree
from musictree.chord import Chord
from musictree.measure import Measure
from musictree.part import Part


# class TestMeasure(TestCase):
#     def test_add_child(self):
#         """
#         Test that only a MusicTree element of type Chord can be added as child.
#         """
#         m = Measure()
#         c = m.add_child(Chord())
#         assert m.get_children() == [c]
#         with self.assertRaises(TypeError):
#             m.add_child(Measure())
#         with self.assertRaises(TypeError):
#             m.add_child(MusicTree())
#         with self.assertRaises(TypeError):
#             m.add_child(Part())
#
#     def test_dot_operator(self):
#         """
#         Test that measures xml_object children can be attained with dot operator
#         """
#         m = Measure()
#         assert isinstance(m.xml_attributes, XMLAttributes)
#         assert isinstance(m.xml_attributes.xml_divisions, XMLDivisions)
#         assert m.xml_attributes.xml_divisions.value == 1
#
#     def test_attributes(self):
#         """
#         Test that a dot operator can directly reach the xml_object
#         """
#         m = Measure()
#         m.xml_object.width = 5
#         assert m.width == 5
#
#         m.width = 7
#         assert m.xml_object.width == 7
#
#         with self.assertRaises(AttributeError):
#             m.hello = 'bbb'
#         m.xml_object.width = 10
#         assert m.xml_object.width == 10
#         assert m.width == 10
#
#         m = Measure()
#         m.width = 10
#         assert m.width == 10
#         assert m.xml_object.width == 10
#
#     def test_create_child(self):
#         """
#         Test that a dot operator can create and add child if necessary
#         """
#         m = Measure(number='1')
#         assert m.xml_barline is None
#         m.xml_barline = XMLBarline()
#         m.xml_barline.xml_bar_style = 'light-light'
#         expected = """<measure number="1">
#     <attributes>
#         <divisions>1</divisions>
#     </attributes>
#     <barline>
#         <bar-style>light-light</bar-style>
#     </barline>
# </measure>
# """
#         assert m.xml_object.to_string() == expected
#
#         def test_measure_chord_one_note(self):
#             m = Measure(number='1')
#             c = Chord(70, 4, relative_x=10)
#             m.add_child(c)
#             expected = """<measure number="1">
#         <attributes>
#             <divisions>1</divisions>
#         </attributes>
#         <note relative-x="10">
#             <pitch>
#                 <step>B</step>
#                 <alter>-1</alter>
#                 <octave>4</octave>
#             </pitch>
#             <duration>4</duration>
#             <voice>1</voice>
#         </note>
#     </measure>
#     """
#             assert m.to_string() == expected
#             # change quarter_duration
#             xml_note = m.xml_object.find_children('XMLNote')[0]
#             c.quarter_duration = 3
#             assert xml_note.xml_duration.value == 3
#             # change notes midi value
#             c.notes[0].midi.value = 72
#             expected = """<measure number="1">
#         <attributes>
#             <divisions>1</divisions>
#         </attributes>
#         <note relative-x="10">
#             <pitch>
#                 <step>C</step>
#                 <octave>5</octave>
#             </pitch>
#             <duration>3</duration>
#             <voice>1</voice>
#         </note>
#     </measure>
#     """
#             assert m.to_string() == expected
#             # change notes midi accidental mode
#             c.notes[0].midi.value = 73
#             c.notes[0].midi.accidental.mode = 'flat'
#             expected = """<measure number="1">
#         <attributes>
#             <divisions>1</divisions>
#         </attributes>
#         <note relative-x="10">
#             <pitch>
#                 <step>D</step>
#                 <alter>-1</alter>
#                 <octave>5</octave>
#             </pitch>
#             <duration>3</duration>
#             <voice>1</voice>
#         </note>
#     </measure>
#     """
#             assert m.to_string() == expected
#
#     def test_measure_with_chord_multiple_notes(self):
#         m = Measure(number='1')
#         m.divisions = 2
#         c = Chord([70, Midi(73, accidental=Accidental(mode='enharmonic_1')), 65], 3, voice=2, relative_x=10)
#         m.add_child(c)
#         c.xml_staff = 1
#         expected = """<measure number="1">
#     <attributes>
#         <divisions>2</divisions>
#     </attributes>
#     <note relative-x="10">
#         <pitch>
#             <step>B</step>
#             <alter>-1</alter>
#             <octave>4</octave>
#         </pitch>
#         <duration>6</duration>
#         <voice>2</voice>
#         <staff>1</staff>
#     </note>
#     <note relative-x="10">
#         <pitch>
#             <step>D</step>
#             <alter>-1</alter>
#             <octave>5</octave>
#         </pitch>
#         <duration>6</duration>
#         <voice>2</voice>
#         <staff>1</staff>
#     </note>
#     <note relative-x="10">
#         <pitch>
#             <step>F</step>
#             <octave>4</octave>
#         </pitch>
#         <duration>6</duration>
#         <voice>2</voice>
#         <staff>1</staff>
#     </note>
# </measure>
# """
#         c.xml_staff = 1
#         assert m.to_string() == expected
