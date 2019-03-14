"""
	<xs:attributeGroup name="part-name-text">
		<xs:annotation>
			<xs:documentation>.</xs:documentation>
		</xs:annotation>
		<xs:attributeGroup ref="print-style"/>
		<xs:attributeGroup ref="print-object"/>
		<xs:attributeGroup ref="justify"/>
	</xs:attributeGroup>
"""
from musicscore.musicxml.attributes.justify import Justify
from musicscore.musicxml.attributes.print_object import PrintObject
from musicscore.musicxml.attributes.print_style import PrintStyle


class PartNameText(PrintStyle, PrintObject, Justify):
    """
    The part-name-text attribute group is used by the part-name and part-abbreviation elements. The print-style and
    justify attribute groups are deprecated in MusicXML 2.0 in favor of the new part-name-display and
    part-abbreviation-display elements
    """

    def __init__(self, default_x=None, default_y=None, relative_x=None, relative_y=None, font_weight=None,
                 font_size=None, font_style=None, font_family=None, color=None, print_object=None, *args, **kwargs):
        super().__init__(default_x=default_x, default_y=default_y, relative_x=relative_x,
                         relative_y=relative_y, font_weight=font_weight, font_size=font_size, font_style=font_style,
                         font_family=font_family, color=color, print_object=print_object, *args, **kwargs)