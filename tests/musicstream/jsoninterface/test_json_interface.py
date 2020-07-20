import json
from pathlib import Path

from musicscore.musicstream.jsoninterface.jsoninterface import JsonInterface
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicxmlunittest import XMLTestCase

path = Path(__file__)


class TestJsonInterface(XMLTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()
        self.json_input = json.dumps([
            {
                'quarter_duration': 2,
                "midis": [60, 61]
            }, {
                "quarter_duration": 1,
                'midis': 70
            }, {
                "quarter_duration": 2.33,
                "midis": (71, 72, 73)
            }, {
                "quarter_duration": 1.5,
                "midis": (60, 61)
            }
        ])

    def test_json_object(self):
        json_object = self.json_input
        jason_inter = JsonInterface(json_object)
        expected = [{'quarter_duration': 2, 'midis': [60, 61]}, {'quarter_duration': 1, 'midis': 70},
                    {'quarter_duration': 2.33, 'midis': [71, 72, 73]}, {'quarter_duration': 1.5, 'midis': [60, 61]}]
        actual = jason_inter.json_object
        self.assertEqual(expected, actual)

    def test_get_simple_format(self):
        json_object = self.json_input
        sf = JsonInterface(json_object).get_simple_format()
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path.parent.joinpath(path.stem + '_get_simple_format.xml')
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)
