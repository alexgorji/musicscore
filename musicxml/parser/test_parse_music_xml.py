from pathlib import Path
from unittest import TestCase

from musicxml.parser.parser import parse_musicxml
from musicxml.xmlelement.xmlelement import XMLScorePartwise
from xmldiff import main

source_path = Path(__file__).parent / 'test_hello_world.xml'


class TestParseMusicXml(TestCase):
    def setUp(self) -> None:
        self.score = parse_musicxml(source_path)

    def test_parse_hello_world(self):
        assert isinstance(self.score, XMLScorePartwise)
        attributes = self.score.get_children()[1].get_children()[0].get_children()[0].child_container_tree
        assert attributes.check_required_elements() is False
        self.score.write(Path(__file__).parent / 'test_hello_world_recreated.xml', intelligent_choice=True)
        diff = main.diff_files('test_hello_world.xml', 'test_hello_world_recreated.xml')
        assert diff == []
