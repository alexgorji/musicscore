from unittest import skip

from musicscore.chord import Chord
from musicscore.exceptions import ScoreMultiMeasureRestError
from musicscore.layout import StaffLayout
from musicscore.measure import Measure
from musicscore.part import Part
from musicscore.score import Score, TITLE, SUBTITLE
from musicscore.tests.util import IdTestCase
from musicxml import XMLNote


class TestScore(IdTestCase):
    def test_score_version(self):
        s = Score(version=3.1)
        assert s.version == '3.1'
        s = Score()
        assert s.version == '4.0'

    def test_score_init(self):
        s = Score()
        p = s.add_child(Part('p1'))
        p.add_child(Measure(1))
        assert s.xml_part_list.find_child('XMLScorePart') == p.score_part.xml_object
        assert s.find_child('XMLPart') == p.xml_object
        assert s.xml_defaults is not None
        s.xml_object._final_checks()

    def test_get_chords(self):
        s = Score()
        p = s.add_child(Part('p1'))
        m = p.add_child(Measure(1))
        m._add_chord(Chord(midis=60, quarter_duration=1))
        m._add_chord(Chord(midis=60, quarter_duration=1))
        m._add_chord(Chord(midis=60, quarter_duration=1))
        m._add_chord(Chord(midis=60, quarter_duration=1))
        assert len(s.get_chords()) == 4
        assert type(s.get_chords()[0]) == Chord

    def test_score_title(self):
        s = Score(title='A Nice Piece of Music')
        credits_ = s.xml_object.find_children('XMLCredit')
        assert len(credits_) == 1
        assert credits_[0].page == 1
        assert credits_[0].xml_credit_type.value_ == 'title'
        title_words = credits_[0].xml_credit_words
        assert title_words.value_ == 'A Nice Piece of Music'
        assert title_words.font_size == TITLE['font_size']
        assert title_words.justify == 'center'
        assert title_words.valign == 'top'
        assert title_words.default_x == TITLE['default_x']['A4']['portrait']
        assert title_words.default_y == TITLE['default_y']['A4']['portrait']

        s.title = 'Some other Title'
        assert title_words.value_ == 'Some other Title'

        s.title = None
        assert len(s.xml_object.find_children('XMLCredit')) == 0

        s.title = 'New Title'
        assert len(s.xml_object.find_children('XMLCredit')) == 1

    def test_score_subtitle(self):
        s = Score(title='A Nice Piece of Music', subtitle='No. 2')
        credits_ = s.xml_object.find_children('XMLCredit')
        assert len(credits_) == 2
        assert credits_[1].page == 1
        assert credits_[1].xml_credit_type.value_ == 'subtitle'
        subtitle_words = credits_[1].xml_credit_words
        assert subtitle_words.value_ == 'No. 2'
        assert subtitle_words.font_size == SUBTITLE['font_size']
        assert subtitle_words.halign == 'center'
        assert subtitle_words.valign == 'top'
        assert subtitle_words.default_x == SUBTITLE['default_x']['A4']['portrait']
        assert subtitle_words.default_y == SUBTITLE['default_y']['A4']['portrait']

        s.subtitle = 'Some other Subtitle'
        assert subtitle_words.value_ == 'Some other Subtitle'

        s.subtitle = None
        assert len(s.xml_object.find_children('XMLCredit')) == 1

        s.subtitle = 'New Subtitle'
        assert len(s.xml_object.find_children('XMLCredit')) == 2

    @skip
    def test_score_composer(self):
        self.fail('Incomplete')

    @skip
    def test_score_add_other_credits(self):
        self.fail('Incomplete')

    def test_score_scaling(self):
        s = Score()
        assert s.scaling.score == s
        assert s.scaling.tenths == 40
        assert s.scaling.millimeters == 7.2319
        assert s.xml_object.xml_defaults.xml_scaling.xml_tenths.value_ == s.scaling.tenths
        assert s.xml_object.xml_defaults.xml_scaling.xml_millimeters.value_ == s.scaling.millimeters
        s.scaling.tenths = 50
        assert s.xml_object.xml_defaults.xml_scaling.xml_tenths.value_ == s.scaling.tenths
        assert s.xml_object.xml_defaults.xml_scaling.xml_millimeters.value_ == s.scaling.millimeters

    def test_score_page_layout(self):
        s = Score()
        assert s.page_layout.parent == s
        assert s.page_layout.scaling == s.scaling
        assert s.xml_object.xml_defaults.xml_page_layout.xml_page_height.value_ == 1643
        assert s.xml_object.xml_defaults.xml_page_layout.xml_page_margins.xml_left_margin.value_ == 140

        s.page_layout.orientation = 'landscape'
        assert s.xml_object.xml_defaults.xml_page_layout.xml_page_height.value_ == 1161
        assert s.xml_object.xml_defaults.xml_page_layout.xml_page_margins.xml_left_margin.value_ == 111

    def test_score_system_layout(self):
        s = Score()
        assert s.system_layout.parent == s
        assert s.xml_object.xml_defaults.xml_system_layout.xml_system_margins.xml_left_margin.value_ == 0
        assert s.xml_object.xml_defaults.xml_system_layout.xml_system_margins.xml_right_margin.value_ == 0
        assert s.xml_object.xml_defaults.xml_system_layout.xml_system_distance.value_ == 117
        assert s.xml_object.xml_defaults.xml_system_layout.xml_top_system_distance.value_ == 117
        s.system_layout.margins.left = 10
        assert s.xml_object.xml_defaults.xml_system_layout.xml_system_margins.xml_left_margin.value_ == 10
        s.system_layout.top_system_distance = 100
        assert s.xml_object.xml_defaults.xml_system_layout.xml_top_system_distance.value_ == 100

    def test_score_staff_layout(self):
        s = Score()
        assert s.staff_layout is None
        s.staff_layout = StaffLayout()
        assert s.xml_object.xml_defaults.xml_staff_layout.xml_staff_distance.value_ == 80
        s.staff_layout.staff_distance = 100
        assert s.xml_object.xml_defaults.xml_staff_layout.xml_staff_distance.value_ == 100

    def test_score_identification_and_new_system(self):
        s = Score()
        assert s.xml_object.xml_identification is not None
        assert s.xml_object.xml_identification.xml_encoding is not None
        all_supports = s.xml_object.xml_identification.xml_encoding.find_children('XMLSupports')
        assert len(all_supports) == 3
        expected = """<identification>
    <encoding>
      <supports element="accidental" type="yes" />
      <supports element="beam" type="yes" />
      <supports element="stem" type="yes" />
    </encoding>
  </identification>
"""
        assert s.xml_object.xml_identification.to_string() == expected
        s.new_system = True
        expected = """<identification>
    <encoding>
      <supports element="accidental" type="yes" />
      <supports element="beam" type="yes" />
      <supports element="stem" type="yes" />
      <supports attribute="new-system" element="print" type="yes" value="yes" />
    </encoding>
  </identification>
"""
        assert s.xml_object.xml_identification.to_string() == expected
        s.new_system = False
        expected = """<identification>
    <encoding>
      <supports element="accidental" type="yes" />
      <supports element="beam" type="yes" />
      <supports element="stem" type="yes" />
    </encoding>
  </identification>
"""
        assert s.xml_object.xml_identification.to_string() == expected
    def test_group_parts_wrong_number(self):
        score = Score()
        [score.add_part(f'p-{i}') for i in range(1, 3)]
        with self.assertRaises(ValueError):
            score.group_parts(1, 0, 1)
        with self.assertRaises(ValueError):
            score.group_parts(2, 1, 6)
        with self.assertRaises(ValueError):
            score.group_parts(3, 2, 1)

    def test_create_missing_measures(self):
        score = Score()
        parts = [score.add_part(f'p-{i}') for i in range(1, 4)]
        [parts[0].add_chord(Chord(60, 4)) for _ in range(5)]
        [parts[2].add_chord(Chord(60, 4)) for _ in range(3)]
        score.finalize()
        for p in parts:
            assert len(p.get_children()) == 5
        for m in parts[1].get_children():
            assert m.get_chords()[0].is_rest
        for m in parts[2].get_children()[3:]:
            assert m.get_chords()[0].is_rest

    def test_group_parts(self):
        score = Score()
        parts = [score.add_part(f'p-{i}') for i in range(1, 6)]
        for p in parts:
            p.add_chord(Chord(0, 4))

        score.group_parts(1, 2, 4, name='Group 1', symbol='square')
        score.group_parts(2, 3, 4, name='Group 2', symbol='bracket')

        expected = """<part-list>
    <score-part id="p-1">
      <part-name />
    </score-part>
    <part-group number="1" type="start">
      <group-name>Group 1</group-name>
      <group-symbol>square</group-symbol>
      <group-barline>yes</group-barline>
    </part-group>
    <score-part id="p-2">
      <part-name />
    </score-part>
    <part-group number="2" type="start">
      <group-name>Group 2</group-name>
      <group-symbol>bracket</group-symbol>
      <group-barline>yes</group-barline>
    </part-group>
    <score-part id="p-3">
      <part-name />
    </score-part>
    <score-part id="p-4">
      <part-name />
    </score-part>
    <part-group number="2" type="stop" />
    <part-group number="1" type="stop" />
    <score-part id="p-5">
      <part-name />
    </score-part>
  </part-list>
"""
        score.finalize()
        assert score.xml_part_list.to_string() == expected

    def test_set_multiple_measure_rests_one_part(self):
        score = Score()
        with self.assertRaises(ScoreMultiMeasureRestError):
            score.set_multi_measure_rest(1, 4)
        part = score.add_part('p1')
        assert len(part.get_children()) == 0
        # add 4 measures and set multiple rests in measure attributes
        score.set_multi_measure_rest(1, 4)
        assert len(part.get_children()) == 4
        assert part.get_measure(1).xml_attributes.xml_measure_style.xml_multiple_rest.value_ == 4

        # Trying to set multiple rest measures again throws error
        with self.assertRaises(ScoreMultiMeasureRestError):
            score.set_multi_measure_rest(2, 3)

        # add 4 measures manually
        [part.add_chord(Chord(0, 4)) for _ in range(4)]
        assert len(part.get_children()) == 8
        # set multiple measure rests for the last three measures
        score.set_multi_measure_rest(6, 8)
        assert part.get_measure(5).xml_attributes.xml_measure_style is None
        assert part.get_measure(6).xml_attributes.xml_measure_style.xml_multiple_rest.value_ == 3
        # Trying to set multiple rest measures on measures with pitches throws error
        [part.add_chord(Chord(60, 4)) for _ in range(4)]
        with self.assertRaises(ScoreMultiMeasureRestError):
            score.set_multi_measure_rest(9, 10)

        # Check if rest measure attribute is set to yes
        score.finalize()
        for measure in part.get_children():
            if int(measure.number) in [1, 2, 3, 4, 6, 7, 8]:
                assert measure.xml_object.get_children_of_type(XMLNote)[0].xml_rest.measure == 'yes'
            elif int(measure.number) == 5:
                assert measure.xml_object.get_children_of_type(XMLNote)[0].xml_rest.measure is None
            else:
                assert measure.xml_object.get_children_of_type(XMLNote)[0].xml_rest is None

    def test_set_multiple_measure_rests_multiple_parts(self):
        score = Score()
        parts = p1, p2 = score.add_part('p1'), score.add_part('p2')
        # add 4 measures and set multiple rests in measure attributes
        score.set_multi_measure_rest(1, 4)
        for p in parts:
            assert len(p.get_children()) == 4
            assert p.get_measure(1).xml_attributes.xml_measure_style.xml_multiple_rest.value_ == 4

        # add 4 measures manually
        [p1.add_chord(Chord(0, 4)) for _ in range(4)]
        assert len(p1.get_children()) == 8
        assert len(p2.get_children()) == 4
        # set multiple measure rests for the last three measures
        score.set_multi_measure_rest(6, 8)
        assert len(p2.get_children()) == 8
        for p in parts:
            assert p.get_measure(5).xml_attributes.xml_measure_style is None
            assert p.get_measure(6).xml_attributes.xml_measure_style.xml_multiple_rest.value_ == 3
        # Trying to set multiple rest measures on measures with pitches throws error
        [p1.add_chord(Chord(60, 4)) for _ in range(4)]
        with self.assertRaises(ScoreMultiMeasureRestError):
            score.set_multi_measure_rest(9, 10)
        # Check if rest measure attribute is set to yes
        score.finalize()
        for measure in p1.get_children():
            if int(measure.number) in [1, 2, 3, 4, 6, 7, 8]:
                assert measure.xml_object.get_children_of_type(XMLNote)[0].xml_rest.measure == 'yes'
            elif int(measure.number) in [5]:
                assert measure.xml_object.get_children_of_type(XMLNote)[0].xml_rest.measure is None
            else:
                assert measure.xml_object.get_children_of_type(XMLNote)[0].xml_rest is None

        for measure in p2.get_children():
            if int(measure.number) in [1, 2, 3, 4, 6, 7, 8]:
                assert measure.xml_object.get_children_of_type(XMLNote)[0].xml_rest.measure == 'yes'
            else:
                assert measure.xml_object.get_children_of_type(XMLNote)[0].xml_rest.measure is None

    def test_barline(self):
        score = Score()
        parts = [score.add_part(f'p-{i}') for i in range(1, 4)]
        [parts[0].add_chord(Chord(60, 4)) for _ in range(5)]
        [parts[2].add_chord(Chord(60, 4)) for _ in range(3)]
        parts[2].get_measure(2).set_barline(style='light-light')
        parts[0].get_measure(2).set_barline(style='light-heavy')
        parts[0].get_measure(4).set_barline(style='heavy-heavy')
        score.finalize()
        for p in parts:
            assert p.get_measure(2).get_barline().xml_bar_style.value_ == 'light-heavy'
            assert p.get_measure(4).get_barline().xml_bar_style.value_ == 'heavy-heavy'

    def test_last_measure_barline(self):
        score = Score()
        parts = [score.add_part(f'p-{i}') for i in range(1, 6)]
        for p in parts:
            for _ in range(3):
                p.add_chord(Chord(0, 4))
        score.finalize()
        for p in parts:
            assert p.get_children()[-1].xml_barline.location == 'right'
            assert p.get_children()[-1].xml_barline.xml_bar_style.value_ == 'light-heavy'

    def test_last_measure_barline_already_set(self):
        score = Score()
        parts = [score.add_part(f'p-{i}') for i in range(1, 6)]
        for p in parts:
            for _ in range(3):
                p.add_chord(Chord(0, 4))
        parts[0].get_children()[-1].set_barline(style='light-light')
        score.finalize()
        for p in parts:
            assert p.get_children()[-1].xml_barline.location == 'right'
            assert p.get_children()[-1].xml_barline.xml_bar_style.value_ == 'light-light'
