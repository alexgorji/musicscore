import os
from unittest import TestCase

from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicscore.musicxml.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class TestTreeTimewise(TestCase):
    def setUp(self):
        self.score = TreeScoreTimewise()
        self.score.add_measure()
        self.score.add_part('one')

    def test_score(self):
        result_path = path+'_test_score'
        self.score.write(result_path)
        TestScore().assert_template(result_path=result_path)

    def test_add_note(self):
        self.score.add_chord(1, 1, TreeChord(0, 1))
        self.score.add_chord(1, 1, TreeChord(0, quarter_duration=1))
        self.score.add_chord(1, 1, TreeChord(61, quarter_duration=2))
        self.score.finish()
        result_path = path + '_test_add_note'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_quantize_beats(self):
        self.score.add_chord(1, 1, TreeChord(60, 1))
        self.score.add_chord(1, 1, TreeChord(60, 1.2))
        self.score.add_chord(1, 1, TreeChord(60, 0.3))
        self.score.add_chord(1, 1, TreeChord(60, 0.2))
        self.score.add_chord(1, 1, TreeChord(60, 1.3))
        # self.score.finish()
#         result = '''<score-timewise version="3.0">
#   <part-list>
#     <score-part id="p1">
#       <part-name print-object="no">one</part-name>
#     </score-part>
#   </part-list>
#   <measure number="1">
#     <part id="p1">
#       <attributes>
#         <divisions>6</divisions>
#         <time>
#           <beats>4</beats>
#           <beat-type>4</beat-type>
#         </time>
#       </attributes>
#       <note>
#         <pitch>
#           <step>C</step>
#           <octave>4</octave>
#         </pitch>
#         <duration>6</duration>
#         <type>quarter</type>
#       </note>
#       <note>
#         <pitch>
#           <step>C</step>
#           <octave>4</octave>
#         </pitch>
#         <duration>6</duration>
#         <tie/>
#         <type>quarter</type>
#       </note>
#       <note>
#         <pitch>
#           <step>C</step>
#           <octave>4</octave>
#         </pitch>
#         <duration>1</duration>
#         <type>16th</type>
#         <beam number="1">begin</beam>
#       </note>
#       <note>
#         <pitch>
#           <step>C</step>
#           <octave>4</octave>
#         </pitch>
#         <duration>2</duration>
#         <type>eighth</type>
#         <beam number="1">continue</beam>
#       </note>
#       <note>
#         <pitch>
#           <step>C</step>
#           <octave>4</octave>
#         </pitch>
#         <duration>1</duration>
#         <type>16th</type>
#         <beam number="1">continue</beam>
#       </note>
#       <note>
#         <pitch>
#           <step>C</step>
#           <octave>4</octave>
#         </pitch>
#         <duration>2</duration>
#         <tie/>
#         <type>eighth</type>
#         <beam number="1">end</beam>
#       </note>
#       <note>
#         <pitch>
#           <step>C</step>
#           <octave>4</octave>
#         </pitch>
#         <duration>6</duration>
#         <type>quarter</type>
#       </note>
#     </part>
#   </measure>
# </score-timewise>
# '''
#         self.assertEqual(self.score.to_string(), result)
#         self.score.write(path=path)

    def test_add_chord(self):
        self.score.add_chord(1, 1, TreeChord((60, 61), quarter_duration=4))
        self.score.finish()
        # print(self.score.to_string())
        # self.score.write(path=path)