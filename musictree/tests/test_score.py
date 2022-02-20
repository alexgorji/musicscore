from musictree.chord import Chord
from musictree.measure import Measure
from musictree.part import Part
from musictree.score import Score, TITLE, SUBTITLE
from musictree.tests.util import IdTestCase


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
        m.add_chord(Chord(midis=60, quarter_duration=1))
        m.add_chord(Chord(midis=60, quarter_duration=1))
        m.add_chord(Chord(midis=60, quarter_duration=1))
        m.add_chord(Chord(midis=60, quarter_duration=1))
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

    def test_score_composer(self):
        self.fail('Incomplete')

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
        assert s.page_layout.scaling == s.scaling
        assert s.xml_object.xml_defaults.xml_page_layout.xml_page_height.value_ == 1643
        assert s.xml_object.xml_defaults.xml_page_layout.xml_page_margins.xml_left_margin.value_ == 140

        s.page_layout.orientation = 'landscape'
        assert s.xml_object.xml_defaults.xml_page_layout.xml_page_height.value_ == 1161
        assert s.xml_object.xml_defaults.xml_page_layout.xml_page_margins.xml_left_margin.value_ == 111

    def test_score_system_layout(self):
        pass