from pathlib import Path

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicxmlunittest import XMLTestCase

path = Path(__file__)


class Test(XMLTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    #
    # def test_(self):
    #
    #     c = self.score.add_child(Credit(page=1))
    #     c.add_child(CreditType('title'))
    #     c.add_child(CreditWords('TEST', default_x=598, default_y=1600, font_size=24, justify='center', valign='top'))
    #
    #     c = self.score.add_child(Credit(page=1))
    #     c.add_child(CreditType('composer'))
    #     c.add_child(CreditWords('me', default_x=1089, default_y=1550, font_size=12, justify='right', valign='top'))
    #
    #     c = self.score.add_child(Credit(page=1))
    #     c.add_child(CreditType('arranger'))
    #     c.add_child(CreditWords('TEST', default_x=1089, default_y=1500, font_size=12, justify='right', valign='top'))
    #
    #     c = self.score.add_child(Credit(page=1))
    #     c.add_child(CreditType('subtitle'))
    #     c.add_child(CreditWords('BLA', default_x=598, default_y=1550, font_size=18, justify='center', valign='top'))
    #
    #     result_path = path + '_test_1'
    #
    #     self.score.write(path=result_path)
    #     TestScore().assert_template(result_path=result_path)

    def test_title_subtitle_composer(self):
        self.score.add_measure()
        self.score.add_part()
        xml_path = path.parent.joinpath(path.stem + '_title_subtitle_composer.xml')
        self.score.add_title("TITLE")
        self.score.add_subtitle("SUBTITLE")
        self.score.add_composer("blablabla 2019")
        self.score.write(path=xml_path)
        self.assertCompareFiles(xml_path)

    def test_page_number(self):
        sf = SimpleFormat(quarter_durations=[1000])
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path.parent.joinpath(path.stem + '_page_number.xml')
        self.score.add_page_number(2)
        self.score.add_page_number(3)
        self.score.write(path=xml_path)
        self.assertCompareFiles(xml_path)
