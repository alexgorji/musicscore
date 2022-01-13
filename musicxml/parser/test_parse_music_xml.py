from pathlib import Path
from unittest import TestCase

from musicxml.parser.parser import parse_musicxml
from musicxml.xmlelement.xmlelement import XMLScorePartwise
from xmldiff import main


class TestParseMusicXml(TestCase):

    def test_parse_hello_world(self):
        score = parse_musicxml(Path(__file__).parent / 'test_hello_world.xml')
        assert isinstance(score, XMLScorePartwise)
        attributes = score.get_children()[1].get_children()[0].get_children()[0].child_container_tree
        assert attributes.check_required_elements() is False
        score.write(Path(__file__).parent / 'test_hello_world_recreated.xml', intelligent_choice=True)
        diff = main.diff_files('test_hello_world.xml', 'test_hello_world_recreated.xml')
        assert diff == []

    def test_parse_bach_partita_3(self):
        score = parse_musicxml(Path(__file__).parent / 'test_bach_partita_3_reduced.xml')
        score.write(Path(__file__).parent / 'test_bach_partita_3_reduced_created.xml', intelligent_choice=True)

