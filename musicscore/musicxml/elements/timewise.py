from musicscore.dtd.dtd import Sequence, GroupReference, Element
from musicscore.musicxml.attributes.document_attributes import DocumentAttributes
from musicscore.musicxml.attributes.measure_attributes import MeasureAttributes
from musicscore.musicxml.attributes.part_attributes import PartAttributes
from musicscore.musicxml.groups.musicdata import MusicData
from musicscore.musicxml.elements.scoreheader import ScoreHeader
from musicscore.musicxml.elements.xml_element import XMLElement


class Part(XMLElement, PartAttributes):
    _DTD = Sequence(
        GroupReference(MusicData)
    )

    def __init__(self, id, *args, **kwargs):
        super().__init__(tag='part', id=id, *args, **kwargs)


class Measure(XMLElement, MeasureAttributes):
    _DTD = Sequence(
        Element(Part, max_occurrence=None)
    )

    def __init__(self, number, *args, **kwargs):
        super().__init__(tag='measure', number=number, *args, **kwargs)


class Score(XMLElement, DocumentAttributes):
    """
    The score-timewise element is the root element for a timewise MusicXML score. It includes a score-header group
    followed by a series of measures with parts inside. The document-attributes attribute group includes the version
    attribute.
    """
    _DTD = Sequence(
        GroupReference(ScoreHeader),
        Element(Measure, max_occurrence=None)
    )

    def __init__(self, *args, **kwargs):
        super().__init__(tag='score-timewise', *args, **kwargs)

    def write(self, path):
        xmlversion = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        doctype = '<!DOCTYPE score-timewise PUBLIC "-//Recordare//DTD MusicXML {} Timewise//EN" "http://www.musicxml.org/dtds/timewise.dtd">\n'.format(
            self.version)

        if path[-4:] != '.xml':
            path += '.xml'
        output_file = open(path, 'w')
        output_file.write(xmlversion)
        output_file.write(doctype)
        output_file.write(self.to_string())
        output_file.close()
