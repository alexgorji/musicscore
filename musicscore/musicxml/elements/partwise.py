from musicscore.dtd.dtd import Sequence, GroupReference, Element
from musicscore.musicxml.attributes.document_attributes import DocumentAttributes
from musicscore.musicxml.attributes.measure_attributes import MeasureAttributes
from musicscore.musicxml.attributes.part_attributes import PartAttributes
from musicscore.musicxml.groups.musicdata import MusicData, Attributes
from musicscore.musicxml.elements.scoreheader import ScoreHeader
from musicscore.musicxml.elements.xml_element import XMLElement

"""
	<xs:element name="score-partwise" block="extension substitution" final="#all">
		<xs:complexType>
			<xs:sequence>
				<xs:group ref="score-header"/>
				<xs:element name="part" maxOccurs="unbounded">
					<xs:complexType>
						<xs:sequence>
							<xs:element name="measure" maxOccurs="unbounded">
								<xs:complexType>
									<xs:group ref="music-data"/>
									<xs:attributeGroup ref="measure-attributes"/>
								</xs:complexType>
							</xs:element>
						</xs:sequence>
						<xs:attributeGroup ref="part-attributes"/>
					</xs:complexType>
				</xs:element>
			</xs:sequence>
			<xs:attributeGroup ref="document-attributes"/>
		</xs:complexType>
	</xs:element>
"""


class Measure(XMLElement, MeasureAttributes):
    _DTD = Sequence(
        GroupReference(MusicData)
    )

    def __init__(self, number=None, *args, **kwargs):
        super().__init__(tag='measure', number=number, *args, **kwargs)


class Part(XMLElement, PartAttributes):
    _DTD = Sequence(
        Element(Measure, max_occurrence=None)
    )

    def __init__(self, id, *args, **kwargs):
        super().__init__(tag='part', id=id, *args, **kwargs)


class Score(XMLElement, DocumentAttributes):
    """The score-partwise element is the root element for a partwise MusicXML score. It includes a score-header group
    followed by a series of parts with measures inside. The document-attributes attribute group includes the version
    attribute.
    """
    _DTD = Sequence(
        GroupReference(ScoreHeader),
        Element(Part, max_occurrence=None)
    )

    def __init__(self, *args, **kwargs):
        super().__init__(tag='score-partwise', *args, **kwargs)

    def write(self, path):
        xmlversion = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        doctype = '<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML {} Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">\n'.format(
            self.version)

        if path[-4:] != '.xml':
            path += '.xml'
        output_file = open(path, 'w')
        output_file.write(xmlversion)
        output_file.write(doctype)
        output_file.write(self.to_string())
        output_file.close()