# from musicscore.musicxml.elements.xml_score_abstract import XMLMeasureAbstract, XMLPartAbstract, XMLScoreAbstract
# from musicscore.musicxml.elements.xml_music_data import XMLMusicData
# from musicscore.musicxml.elements.attributes import Attributes
#
#
# class PartTimewise(XMLPartAbstract):
#
#     _CHILDREN_TYPES = XMLPartAbstract._CHILDREN_TYPES
#     _CHILDREN_TYPES.extend([Attributes, XMLMusicData])
#
#     def __init__(self, id, *args, **kwargs):
#         super().__init__(id=id, *args, **kwargs)
#
#
# class MeasureTimewise(XMLMeasureAbstract):
#
#     _CHILDREN_TYPES = [PartTimewise]
#     _CHILDREN_TYPES.extend(XMLPartAbstract._CHILDREN_TYPES)
#
#     def __init__(self, number, *args, **kwargs):
#         super().__init__(number=number, *args, **kwargs)
#         self.multiple = True
#
#
# class ScoreTimewise(XMLScoreAbstract):
#
#     _CHILDREN_TYPES = XMLScoreAbstract._CHILDREN_TYPES
#     _CHILDREN_TYPES.append(MeasureTimewise)
#
#     def __init__(self, *args, **kwargs):
#         XMLScoreAbstract.__init__(self, tag='score-timewise', *args, **kwargs)
#
#     def write(self, path):
#         xmlversion = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
#         doctype = '<!DOCTYPE score-timewise PUBLIC "-//Recordare//DTD MusicXML 3.0 Timewise//EN" "http://www.musicxml.org/dtds/timewise.dtd">\n'
#
#         path += '.xml'
#         output_file = open(path, 'w')
#         output_file.write(xmlversion)
#         output_file.write(doctype)
#         output_file.write(self.to_string())
#         output_file.close()
#         print('writing finished')
#
#

"""
	<xs:element name="score-timewise" block="extension substitution" final="#all">
		<xs:complexType>

			<xs:sequence>

				<xs:group ref="score-header"/>

				<xs:element name="measure" maxOccurs="unbounded">

					<xs:complexType>
						<xs:sequence>
							<xs:element name="part" maxOccurs="unbounded">
								<xs:complexType>
									<xs:group ref="music-data"/>
									<xs:attributeGroup ref="part-attributes"/>
								</xs:complexType>
							</xs:element>
						</xs:sequence>
						<xs:attributeGroup ref="measure-attributes"/>
					</xs:complexType>

				</xs:element>

			</xs:sequence>

			<xs:attributeGroup ref="document-attributes"/>
		</xs:complexType>
	</xs:element>

</xs:schema>
"""
from musicscore.dtd.dtd import Sequence, GroupReference, Element
from musicscore.musicxml.attributes.document_attributes import DocumentAttributes
from musicscore.musicxml.attributes.measure_attributes import MeasureAttributes
from musicscore.musicxml.attributes.part_attributes import PartAttributes
from musicscore.musicxml.elements.music_data import MusicData
from musicscore.musicxml.elements.score_header import ScoreHeader
from musicscore.musicxml.elements.xml_element import XMLElement


class Part(XMLElement, PartAttributes):
    _DTD = GroupReference(MusicData)


class Measure(XMLElement, MeasureAttributes):
    _DTD = Sequence(
        Element(Part, max_occurrence=None)
    )

    def __init__(self, *args, **kwargs):
        super().__init__(tag='measure', *args, **kwargs)


class ScoreTimewise(XMLElement, DocumentAttributes):
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
