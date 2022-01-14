import datetime

from musicxml.util.core import convert_to_xml_class_name
import xml.etree.ElementTree as ET
from musicxml.xmlelement.xmlelement import *


def _et_xml_to_music_xml(node):
    output = eval(convert_to_xml_class_name(node.tag))()
    for k, v in node.attrib.items():
        try:
            setattr(output, k, v)
        except (TypeError, ValueError):
            try:
                setattr(output, k, int(v))
            except ValueError:
                setattr(output, k, float(v))

    if node.text:
        text = node.text.strip()
        if text:
            try:
                output.value = text
            except TypeError:
                try:
                    output.value = int(text)
                except ValueError:
                    output.value = float(text)
    return output


def _parse_node(xml_node):
    # print('parsing node:', xml_node.tag, xml_node.attrib)
    output = _et_xml_to_music_xml(xml_node)
    # print('output', output)
    for child in xml_node:
        output.add_child(_parse_node(child))
    return output


def parse_musicxml(file_path):
    # start_et = datetime.datetime.now()
    with open(file_path) as file:
        xml = ET.parse(file)
    end_et = datetime.datetime.now()
    # print(f'parse musicxml ET parsing: {end_et - start_et}')
    parsed = _parse_node(xml.getroot())
    # end_parsing = datetime.datetime.now()
    # print(f'parse musicxml parsing: {end_parsing - end_et}')
    return parsed
