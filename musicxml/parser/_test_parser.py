import datetime
import random
from pathlib import Path
from unittest import TestCase

from musicxml.parser.parser import parse_musicxml, _parse_node
from musicxml.xmlelement.xmlelement import XMLScorePartwise
import xml.etree.ElementTree as ET


class TestParseMusicXml(TestCase):
    def test_parse_hello_world(self):
        score = parse_musicxml(Path(__file__).parent / 'test_hello_world.xml')
        assert isinstance(score, XMLScorePartwise)
        attributes = score.get_children()[1].get_children()[0].get_children()[0].child_container_tree
        assert attributes.check_required_elements() is False
        score.write(Path(__file__).parent / 'test_hello_world_recreated.xml', intelligent_choice=True)

    def test_parse_bach_partita_3_reduced(self):
        start_reading = datetime.datetime.now()
        print("start reading score")
        score = parse_musicxml(Path(__file__).parent / 'test_bach_partita_3_reduced.xml')
        start_writing = datetime.datetime.now()
        print(f"start writing score :{start_writing - start_reading}")
        score.write(Path(__file__).parent / 'test_bach_partita_3_reduced_created.xml')
        end = datetime.datetime.now()
        print(f"end writing score :{end - start_writing}")
        """
        main.diff_files takes too long ...
        """
        # diff = main.diff_files('test_bach_partita_3_reduced.xml', 'test_bach_partita_3_reduced_created.xml')
        # assert diff == []

    def test_parse_bach_partita_3_reduced_reordered(self):
        def reordered_children(el, seed=None):
            output = ET.Element(el.tag, el.attrib)
            output.text = el.text
            children = list(el)
            if el.tag in ['note']:
                random.Random(seed).shuffle(children)
            for child in children:
                output.append(reordered_children(el=child, seed=seed))
            return output

        start_reading = datetime.datetime.now()
        with open(Path(__file__).parent / 'test_bach_partita_3_reduced.xml') as file:
            xml = ET.parse(file)
        reordered = reordered_children(xml.getroot(), seed=55)
        score = _parse_node(reordered)
        start_writing = datetime.datetime.now()
        print(f"start writing score :{start_writing - start_reading}")
        score.write(Path(__file__).parent / 'test_bach_partita_3_reordered_created.xml')
        end = datetime.datetime.now()
        print(f"end writing score :{end - start_writing}")
        # print("start reading score")

    def test_parse_bach_partita_3(self):
        start_reading = datetime.datetime.now()
        print("start reading score")
        score = parse_musicxml(Path(__file__).parent / 'test_bach_partita_3.xml')
        start_writing = datetime.datetime.now()
        print(f"start writing score :{start_writing - start_reading}")
        score.write(Path(__file__).parent / 'test_bach_partita_3_created.xml')
        end = datetime.datetime.now()
        print(f"end writing score :{end - start_writing}")
