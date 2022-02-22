from musicxml.util.core import convert_to_xsd_class_name
from musicxml.xsd.xsdattribute import XSDAttribute
from musicxml.xsd.xsdtree import XSDTree, XSDTreeElement
from musicxml.xsd.xsdsimpletype import *
import xml.etree.ElementTree as ET


class XSDAttributeGroup(XSDTreeElement):

    @classmethod
    def get_xsd_attributes(cls):
        output = []
        for child in cls.XSD_TREE.get_children():
            if child.tag == 'attribute':
                output.append(XSDAttribute(child))
            if child.tag == 'attributeGroup':
                output.extend(eval(child.xsd_element_class_name).get_xsd_attributes())
        return output

# -----------------------------------------------------
# AUTOMATICALLY GENERATED WITH generate_attributes.py
# -----------------------------------------------------


class XSDAttributeGroupBendSound(XSDAttributeGroup):
    """
    The bend-sound type is used for bend and slide elements, and is similar to the trill-sound attribute group. Here the beats element refers to the number of discrete elements (like MIDI pitch bends) used to represent a continuous bend or slide. The first-beat indicates the percentage of the duration for starting a bend; the last-beat the percentage for ending it. The default choices are:

	accelerate = "no"
	beats = "4"
	first-beat = "25"
	last-beat = "75"
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="bend-sound">
    <xs:annotation>
        <xs:documentation>The bend-sound type is used for bend and slide elements, and is similar to the trill-sound attribute group. Here the beats element refers to the number of discrete elements (like MIDI pitch bends) used to represent a continuous bend or slide. The first-beat indicates the percentage of the duration for starting a bend; the last-beat the percentage for ending it. The default choices are:

	accelerate = "no"
	beats = "4"
	first-beat = "25"
	last-beat = "75"</xs:documentation>
    </xs:annotation>
    <xs:attribute name="accelerate" type="yes-no" />
    <xs:attribute name="beats" type="trill-beats" />
    <xs:attribute name="first-beat" type="percent" />
    <xs:attribute name="last-beat" type="percent" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupBezier(XSDAttributeGroup):
    """
    The bezier attribute group is used to indicate the curvature of slurs and ties, representing the control points for a cubic bezier curve. For ties, the bezier attribute group is used with the tied element.

Normal slurs, S-shaped slurs, and ties need only two bezier points: one associated with the start of the slur or tie, the other with the stop. Complex slurs and slurs divided over system breaks can specify additional bezier data at slur elements with a continue type.

The bezier-x, bezier-y, and bezier-offset attributes describe the outgoing bezier point for slurs and ties with a start type, and the incoming bezier point for slurs and ties with types of stop or continue. The bezier-x2, bezier-y2, and bezier-offset2 attributes are only valid with slurs of type continue, and describe the outgoing bezier point.

The bezier-x, bezier-y, bezier-x2, and bezier-y2 attributes are specified in tenths, relative to any position settings associated with the slur or tied element. The bezier-offset and bezier-offset2 attributes are measured in terms of musical divisions, like the offset element. 

The bezier-offset and bezier-offset2 attributes are deprecated as of MusicXML 3.1. If both the bezier-x and bezier-offset attributes are present, the bezier-x attribute takes priority. Similarly, the bezier-x2 attribute takes priority over the bezier-offset2 attribute. The two types of bezier attributes are not additive.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="bezier">
    <xs:annotation>
        <xs:documentation>The bezier attribute group is used to indicate the curvature of slurs and ties, representing the control points for a cubic bezier curve. For ties, the bezier attribute group is used with the tied element.

Normal slurs, S-shaped slurs, and ties need only two bezier points: one associated with the start of the slur or tie, the other with the stop. Complex slurs and slurs divided over system breaks can specify additional bezier data at slur elements with a continue type.

The bezier-x, bezier-y, and bezier-offset attributes describe the outgoing bezier point for slurs and ties with a start type, and the incoming bezier point for slurs and ties with types of stop or continue. The bezier-x2, bezier-y2, and bezier-offset2 attributes are only valid with slurs of type continue, and describe the outgoing bezier point.

The bezier-x, bezier-y, bezier-x2, and bezier-y2 attributes are specified in tenths, relative to any position settings associated with the slur or tied element. The bezier-offset and bezier-offset2 attributes are measured in terms of musical divisions, like the offset element. 

The bezier-offset and bezier-offset2 attributes are deprecated as of MusicXML 3.1. If both the bezier-x and bezier-offset attributes are present, the bezier-x attribute takes priority. Similarly, the bezier-x2 attribute takes priority over the bezier-offset2 attribute. The two types of bezier attributes are not additive.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="bezier-x" type="tenths" />
    <xs:attribute name="bezier-y" type="tenths" />
    <xs:attribute name="bezier-x2" type="tenths" />
    <xs:attribute name="bezier-y2" type="tenths" />
    <xs:attribute name="bezier-offset" type="divisions" />
    <xs:attribute name="bezier-offset2" type="divisions" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupColor(XSDAttributeGroup):
    """
    The color attribute group indicates the color of an element.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="color">
    <xs:annotation>
        <xs:documentation>The color attribute group indicates the color of an element.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="color" type="color" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupDashedFormatting(XSDAttributeGroup):
    """
    The dashed-formatting entity represents the length of dashes and spaces in a dashed line. Both the dash-length and space-length attributes are represented in tenths. These attributes are ignored if the corresponding line-type attribute is not dashed.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="dashed-formatting">
    <xs:annotation>
        <xs:documentation>The dashed-formatting entity represents the length of dashes and spaces in a dashed line. Both the dash-length and space-length attributes are represented in tenths. These attributes are ignored if the corresponding line-type attribute is not dashed.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="dash-length" type="tenths" />
    <xs:attribute name="space-length" type="tenths" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupDirective(XSDAttributeGroup):
    """
    The directive attribute changes the default-x position of a direction. It indicates that the left-hand side of the direction is aligned with the left-hand side of the time signature. If no time signature is present, it is aligned with the left-hand side of the first music notational element in the measure. If a default-x, justify, or halign attribute is present, it overrides the directive attribute.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="directive">
    <xs:annotation>
        <xs:documentation>The directive attribute changes the default-x position of a direction. It indicates that the left-hand side of the direction is aligned with the left-hand side of the time signature. If no time signature is present, it is aligned with the left-hand side of the first music notational element in the measure. If a default-x, justify, or halign attribute is present, it overrides the directive attribute.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="directive" type="yes-no" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupDocumentAttributes(XSDAttributeGroup):
    """
    The document-attributes attribute group is used to specify the attributes for an entire MusicXML document. Currently this is used for the version attribute.

The version attribute was added in Version 1.1 for the score-partwise and score-timewise documents. It provides an easier way to get version information than through the MusicXML public ID. The default value is 1.0 to make it possible for programs that handle later versions to distinguish earlier version files reliably. Programs that write MusicXML 1.1 or later files should set this attribute.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="document-attributes">
    <xs:annotation>
        <xs:documentation>The document-attributes attribute group is used to specify the attributes for an entire MusicXML document. Currently this is used for the version attribute.

The version attribute was added in Version 1.1 for the score-partwise and score-timewise documents. It provides an easier way to get version information than through the MusicXML public ID. The default value is 1.0 to make it possible for programs that handle later versions to distinguish earlier version files reliably. Programs that write MusicXML 1.1 or later files should set this attribute.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="version" type="xs:token" default="1.0" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupEnclosure(XSDAttributeGroup):
    """
    The enclosure attribute group is used to specify the formatting of an enclosure around text or symbols.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="enclosure">
    <xs:annotation>
        <xs:documentation>The enclosure attribute group is used to specify the formatting of an enclosure around text or symbols.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="enclosure" type="enclosure-shape" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupFont(XSDAttributeGroup):
    """
    The font attribute group gathers together attributes for determining the font within a credit or direction. They are based on the text styles for Cascading Style Sheets. The font-family is a comma-separated list of font names.The font-style can be normal or italic. The font-size can be one of the CSS sizes or a numeric point size. The font-weight can be normal or bold. The default is application-dependent, but is a text font vs. a music font.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="font">
    <xs:annotation>
        <xs:documentation>The font attribute group gathers together attributes for determining the font within a credit or direction. They are based on the text styles for Cascading Style Sheets. The font-family is a comma-separated list of font names.The font-style can be normal or italic. The font-size can be one of the CSS sizes or a numeric point size. The font-weight can be normal or bold. The default is application-dependent, but is a text font vs. a music font.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="font-family" type="font-family" />
    <xs:attribute name="font-style" type="font-style" />
    <xs:attribute name="font-size" type="font-size" />
    <xs:attribute name="font-weight" type="font-weight" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupHalign(XSDAttributeGroup):
    """
    In cases where text extends over more than one line, horizontal alignment and justify values can be different. The most typical case is for credits, such as:

	Words and music by
	  Pat Songwriter

Typically this type of credit is aligned to the right, so that the position information refers to the right-most part of the text. But in this example, the text is center-justified, not right-justified.

The halign attribute is used in these situations. If it is not present, its value is the same as for the justify attribute. For elements where a justify attribute is not allowed, the default is implementation-dependent.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="halign">
    <xs:annotation>
        <xs:documentation>In cases where text extends over more than one line, horizontal alignment and justify values can be different. The most typical case is for credits, such as:

	Words and music by
	  Pat Songwriter

Typically this type of credit is aligned to the right, so that the position information refers to the right-most part of the text. But in this example, the text is center-justified, not right-justified.

The halign attribute is used in these situations. If it is not present, its value is the same as for the justify attribute. For elements where a justify attribute is not allowed, the default is implementation-dependent.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="halign" type="left-center-right" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupJustify(XSDAttributeGroup):
    """
    The justify attribute is used to indicate left, center, or right justification. The default value varies for different elements. For elements where the justify attribute is present but the halign attribute is not, the justify attribute indicates horizontal alignment as well as justification.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="justify">
    <xs:annotation>
        <xs:documentation>The justify attribute is used to indicate left, center, or right justification. The default value varies for different elements. For elements where the justify attribute is present but the halign attribute is not, the justify attribute indicates horizontal alignment as well as justification.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="justify" type="left-center-right" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupLetterSpacing(XSDAttributeGroup):
    """
    The letter-spacing attribute specifies text tracking. Values are either "normal" or a number representing the number of ems to add between each letter. The number may be negative in order to subtract space. The default is normal, which allows flexibility of letter-spacing for purposes of text justification.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="letter-spacing">
    <xs:annotation>
        <xs:documentation>The letter-spacing attribute specifies text tracking. Values are either "normal" or a number representing the number of ems to add between each letter. The number may be negative in order to subtract space. The default is normal, which allows flexibility of letter-spacing for purposes of text justification.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="letter-spacing" type="number-or-normal" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupLevelDisplay(XSDAttributeGroup):
    """
    The level-display attribute group specifies three common ways to indicate editorial indications: putting parentheses or square brackets around a symbol, or making the symbol a different size. If not specified, they are left to application defaults. It is used by the level and accidental elements.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="level-display">
    <xs:annotation>
        <xs:documentation>The level-display attribute group specifies three common ways to indicate editorial indications: putting parentheses or square brackets around a symbol, or making the symbol a different size. If not specified, they are left to application defaults. It is used by the level and accidental elements.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="parentheses" type="yes-no" />
    <xs:attribute name="bracket" type="yes-no" />
    <xs:attribute name="size" type="symbol-size" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupLineHeight(XSDAttributeGroup):
    """
    The line-height attribute specifies text leading. Values are either "normal" or a number representing the percentage of the current font height to use for leading. The default is "normal". The exact normal value is implementation-dependent, but values between 100 and 120 are recommended.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="line-height">
    <xs:annotation>
        <xs:documentation>The line-height attribute specifies text leading. Values are either "normal" or a number representing the percentage of the current font height to use for leading. The default is "normal". The exact normal value is implementation-dependent, but values between 100 and 120 are recommended.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="line-height" type="number-or-normal" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupLineLength(XSDAttributeGroup):
    """
    The line-length attribute distinguishes between different line lengths for doit, falloff, plop, and scoop articulations.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="line-length">
    <xs:annotation>
        <xs:documentation>The line-length attribute distinguishes between different line lengths for doit, falloff, plop, and scoop articulations.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="line-length" type="line-length" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupLineShape(XSDAttributeGroup):
    """
    The line-shape attribute distinguishes between straight and curved lines.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="line-shape">
    <xs:annotation>
        <xs:documentation>The line-shape attribute distinguishes between straight and curved lines.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="line-shape" type="line-shape" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupLineType(XSDAttributeGroup):
    """
    The line-type attribute distinguishes between solid, dashed, dotted, and wavy lines.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="line-type">
    <xs:annotation>
        <xs:documentation>The line-type attribute distinguishes between solid, dashed, dotted, and wavy lines.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="line-type" type="line-type" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupOptionalUniqueId(XSDAttributeGroup):
    """
    The optional-unique-id attribute group allows an element to optionally specify an ID that is unique to the entire document. This attribute group is not used for a required id attribute, or for an id attribute that specifies an id reference.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="optional-unique-id">
    <xs:annotation>
        <xs:documentation>The optional-unique-id attribute group allows an element to optionally specify an ID that is unique to the entire document. This attribute group is not used for a required id attribute, or for an id attribute that specifies an id reference.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="id" type="xs:ID" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupOrientation(XSDAttributeGroup):
    """
    The orientation attribute indicates whether slurs and ties are overhand (tips down) or underhand (tips up). This is distinct from the placement attribute used by any notation type.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="orientation">
    <xs:annotation>
        <xs:documentation>The orientation attribute indicates whether slurs and ties are overhand (tips down) or underhand (tips up). This is distinct from the placement attribute used by any notation type.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="orientation" type="over-under" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupPlacement(XSDAttributeGroup):
    """
    The placement attribute indicates whether something is above or below another element, such as a note or a notation.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="placement">
    <xs:annotation>
        <xs:documentation>The placement attribute indicates whether something is above or below another element, such as a note or a notation.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="placement" type="above-below" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupPosition(XSDAttributeGroup):
    """
    For most elements, any program will compute a default x and y position. The position attributes let this be changed two ways.

The default-x and default-y attributes change the computation of the default position. For most elements, the origin is changed relative to the left-hand side of the note or the musical position within the bar (x) and the top line of the staff (y).

For the following elements, the default-x value changes the origin relative to the start of the current measure:

	- note
	- figured-bass
	- harmony
	- link
	- directive
	- measure-numbering
	- all descendants of the part-list element
	- all children of the direction-type element

This origin is from the start of the entire measure, at either the left barline or the start of the system.

When the default-x attribute is used within a child element of the part-name-display, part-abbreviation-display, group-name-display, or group-abbreviation-display elements, it changes the origin relative to the start of the first measure on the system. These values are used when the current measure or a succeeding measure starts a new system. The same change of origin is used for the group-symbol element.

For the note, figured-bass, and harmony elements, the default-x value is considered to have adjusted the musical position within the bar for its descendant elements.

Since the credit-words and credit-image elements are not related to a measure, in these cases the default-x and default-y attributes adjust the origin relative to the bottom left-hand corner of the specified page.

The relative-x and relative-y attributes change the position relative to the default position, either as computed by the individual program, or as overridden by the default-x and default-y attributes.

Positive x is right, negative x is left; positive y is up, negative y is down. All units are in tenths of interline space. For stems, positive relative-y lengthens a stem while negative relative-y shortens it.

The default-x and default-y position attributes provide higher-resolution positioning data than related features such as the placement attribute and the offset element. Applications reading a MusicXML file that can understand both features should generally rely on the default-x and default-y attributes for their greater accuracy. For the relative-x and relative-y attributes, the offset element, placement attribute, and directive attribute provide context for the relative position information, so the two features should be interpreted together.

As elsewhere in the MusicXML format, tenths are the global tenths defined by the scaling element, not the local tenths of a staff resized by the staff-size element.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="position">
    <xs:annotation>
        <xs:documentation>For most elements, any program will compute a default x and y position. The position attributes let this be changed two ways.

The default-x and default-y attributes change the computation of the default position. For most elements, the origin is changed relative to the left-hand side of the note or the musical position within the bar (x) and the top line of the staff (y).

For the following elements, the default-x value changes the origin relative to the start of the current measure:

	- note
	- figured-bass
	- harmony
	- link
	- directive
	- measure-numbering
	- all descendants of the part-list element
	- all children of the direction-type element

This origin is from the start of the entire measure, at either the left barline or the start of the system.

When the default-x attribute is used within a child element of the part-name-display, part-abbreviation-display, group-name-display, or group-abbreviation-display elements, it changes the origin relative to the start of the first measure on the system. These values are used when the current measure or a succeeding measure starts a new system. The same change of origin is used for the group-symbol element.

For the note, figured-bass, and harmony elements, the default-x value is considered to have adjusted the musical position within the bar for its descendant elements.

Since the credit-words and credit-image elements are not related to a measure, in these cases the default-x and default-y attributes adjust the origin relative to the bottom left-hand corner of the specified page.

The relative-x and relative-y attributes change the position relative to the default position, either as computed by the individual program, or as overridden by the default-x and default-y attributes.

Positive x is right, negative x is left; positive y is up, negative y is down. All units are in tenths of interline space. For stems, positive relative-y lengthens a stem while negative relative-y shortens it.

The default-x and default-y position attributes provide higher-resolution positioning data than related features such as the placement attribute and the offset element. Applications reading a MusicXML file that can understand both features should generally rely on the default-x and default-y attributes for their greater accuracy. For the relative-x and relative-y attributes, the offset element, placement attribute, and directive attribute provide context for the relative position information, so the two features should be interpreted together.

As elsewhere in the MusicXML format, tenths are the global tenths defined by the scaling element, not the local tenths of a staff resized by the staff-size element.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="default-x" type="tenths" />
    <xs:attribute name="default-y" type="tenths" />
    <xs:attribute name="relative-x" type="tenths" />
    <xs:attribute name="relative-y" type="tenths" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupPrintObject(XSDAttributeGroup):
    """
    The print-object attribute specifies whether or not to print an object (e.g. a note or a rest). It is yes by default.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="print-object">
    <xs:annotation>
        <xs:documentation>The print-object attribute specifies whether or not to print an object (e.g. a note or a rest). It is yes by default.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="print-object" type="yes-no" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupPrintSpacing(XSDAttributeGroup):
    """
    The print-spacing attribute controls whether or not spacing is left for an invisible note or object. It is used only if no note, dot, or lyric is being printed. The value is yes (leave spacing) by default.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="print-spacing">
    <xs:annotation>
        <xs:documentation>The print-spacing attribute controls whether or not spacing is left for an invisible note or object. It is used only if no note, dot, or lyric is being printed. The value is yes (leave spacing) by default.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="print-spacing" type="yes-no" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupPrintStyle(XSDAttributeGroup):
    """
    The print-style attribute group collects the most popular combination of printing attributes: position, font, and color.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="print-style">
    <xs:annotation>
        <xs:documentation>The print-style attribute group collects the most popular combination of printing attributes: position, font, and color.</xs:documentation>
    </xs:annotation>
    <xs:attributeGroup ref="position" />
    <xs:attributeGroup ref="font" />
    <xs:attributeGroup ref="color" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupPrintStyleAlign(XSDAttributeGroup):
    """
    The print-style-align attribute group adds the halign and valign attributes to the position, font, and color attributes.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="print-style-align">
    <xs:annotation>
        <xs:documentation>The print-style-align attribute group adds the halign and valign attributes to the position, font, and color attributes.</xs:documentation>
    </xs:annotation>
    <xs:attributeGroup ref="print-style" />
    <xs:attributeGroup ref="halign" />
    <xs:attributeGroup ref="valign" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupPrintout(XSDAttributeGroup):
    """
    The printout attribute group collects the different controls over printing an object (e.g. a note or rest) and its parts, including augmentation dots and lyrics. This is especially useful for notes that overlap in different voices, or for chord sheets that contain lyrics and chords but no melody.

By default, all these attributes are set to yes. If print-object is set to no, the print-dot and print-lyric attributes are interpreted to also be set to no if they are not present.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="printout">
    <xs:annotation>
        <xs:documentation>The printout attribute group collects the different controls over printing an object (e.g. a note or rest) and its parts, including augmentation dots and lyrics. This is especially useful for notes that overlap in different voices, or for chord sheets that contain lyrics and chords but no melody.

By default, all these attributes are set to yes. If print-object is set to no, the print-dot and print-lyric attributes are interpreted to also be set to no if they are not present.</xs:documentation>
    </xs:annotation>
    <xs:attributeGroup ref="print-object" />
    <xs:attribute name="print-dot" type="yes-no" />
    <xs:attributeGroup ref="print-spacing" />
    <xs:attribute name="print-lyric" type="yes-no" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupSmufl(XSDAttributeGroup):
    """
    The smufl attribute group is used to indicate a particular Standard Music Font Layout (SMuFL) character. Sometimes this is a formatting choice, and sometimes this is a refinement of the semantic meaning of an element.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="smufl">
    <xs:annotation>
        <xs:documentation>The smufl attribute group is used to indicate a particular Standard Music Font Layout (SMuFL) character. Sometimes this is a formatting choice, and sometimes this is a refinement of the semantic meaning of an element.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="smufl" type="smufl-glyph-name" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupSystemRelation(XSDAttributeGroup):
    """
    The system-relation attribute group distinguishes elements that are associated with a system rather than the particular part where the element appears.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="system-relation">
    <xs:annotation>
        <xs:documentation>The system-relation attribute group distinguishes elements that are associated with a system rather than the particular part where the element appears.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="system" type="system-relation" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupSymbolFormatting(XSDAttributeGroup):
    """
    The symbol-formatting attribute group collects the common formatting attributes for musical symbols. Default values may differ across the elements that use this group.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="symbol-formatting">
    <xs:annotation>
        <xs:documentation>The symbol-formatting attribute group collects the common formatting attributes for musical symbols. Default values may differ across the elements that use this group.</xs:documentation>
    </xs:annotation>
    <xs:attributeGroup ref="justify" />
    <xs:attributeGroup ref="print-style-align" />
    <xs:attributeGroup ref="text-decoration" />
    <xs:attributeGroup ref="text-rotation" />
    <xs:attributeGroup ref="letter-spacing" />
    <xs:attributeGroup ref="line-height" />
    <xs:attributeGroup ref="text-direction" />
    <xs:attributeGroup ref="enclosure" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupTextDecoration(XSDAttributeGroup):
    """
    The text-decoration attribute group is based on the similar feature in XHTML and CSS. It allows for text to be underlined, overlined, or struck-through. It extends the CSS version by allow double or triple lines instead of just being on or off.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="text-decoration">
    <xs:annotation>
        <xs:documentation>The text-decoration attribute group is based on the similar feature in XHTML and CSS. It allows for text to be underlined, overlined, or struck-through. It extends the CSS version by allow double or triple lines instead of just being on or off.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="underline" type="number-of-lines" />
    <xs:attribute name="overline" type="number-of-lines" />
    <xs:attribute name="line-through" type="number-of-lines" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupTextDirection(XSDAttributeGroup):
    """
    The text-direction attribute is used to adjust and override the Unicode bidirectional text algorithm, similar to the Directionality data category in the W3C Internationalization Tag Set recommendation.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="text-direction">
    <xs:annotation>
        <xs:documentation>The text-direction attribute is used to adjust and override the Unicode bidirectional text algorithm, similar to the Directionality data category in the W3C Internationalization Tag Set recommendation.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="dir" type="text-direction" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupTextFormatting(XSDAttributeGroup):
    """
    The text-formatting attribute group collects the common formatting attributes for text elements. Default values may differ across the elements that use this group.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="text-formatting">
    <xs:annotation>
        <xs:documentation>The text-formatting attribute group collects the common formatting attributes for text elements. Default values may differ across the elements that use this group.</xs:documentation>
    </xs:annotation>
    <xs:attributeGroup ref="justify" />
    <xs:attributeGroup ref="print-style-align" />
    <xs:attributeGroup ref="text-decoration" />
    <xs:attributeGroup ref="text-rotation" />
    <xs:attributeGroup ref="letter-spacing" />
    <xs:attributeGroup ref="line-height" />
    <xs:attribute ref="xml:lang" />
    <xs:attribute ref="xml:space" />
    <xs:attributeGroup ref="text-direction" />
    <xs:attributeGroup ref="enclosure" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupTextRotation(XSDAttributeGroup):
    """
    The rotation attribute is used to rotate text around the alignment point specified by the halign and valign attributes. Positive values are clockwise rotations, while negative values are counter-clockwise rotations.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="text-rotation">
    <xs:annotation>
        <xs:documentation>The rotation attribute is used to rotate text around the alignment point specified by the halign and valign attributes. Positive values are clockwise rotations, while negative values are counter-clockwise rotations.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="rotation" type="rotation-degrees" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupTrillSound(XSDAttributeGroup):
    """
    The trill-sound attribute group includes attributes used to guide the sound of trills, mordents, turns, shakes, and wavy lines. The default choices are:

	start-note = "upper"
	trill-step = "whole"
	two-note-turn = "none"
	accelerate = "no"
	beats = "4".

Second-beat and last-beat are percentages for landing on the indicated beat, with defaults of 25 and 75 respectively.

For mordent and inverted-mordent elements, the defaults are different:

	The default start-note is "main", not "upper".
	The default for beats is "3", not "4".
	The default for second-beat is "12", not "25".
	The default for last-beat is "24", not "75".
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="trill-sound">
    <xs:annotation>
        <xs:documentation>The trill-sound attribute group includes attributes used to guide the sound of trills, mordents, turns, shakes, and wavy lines. The default choices are:

	start-note = "upper"
	trill-step = "whole"
	two-note-turn = "none"
	accelerate = "no"
	beats = "4".

Second-beat and last-beat are percentages for landing on the indicated beat, with defaults of 25 and 75 respectively.

For mordent and inverted-mordent elements, the defaults are different:

	The default start-note is "main", not "upper".
	The default for beats is "3", not "4".
	The default for second-beat is "12", not "25".
	The default for last-beat is "24", not "75".</xs:documentation>
    </xs:annotation>
    <xs:attribute name="start-note" type="start-note" />
    <xs:attribute name="trill-step" type="trill-step" />
    <xs:attribute name="two-note-turn" type="two-note-turn" />
    <xs:attribute name="accelerate" type="yes-no" />
    <xs:attribute name="beats" type="trill-beats" />
    <xs:attribute name="second-beat" type="percent" />
    <xs:attribute name="last-beat" type="percent" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupValign(XSDAttributeGroup):
    """
    The valign attribute is used to indicate vertical alignment to the top, middle, bottom, or baseline of the text. Defaults are implementation-dependent.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="valign">
    <xs:annotation>
        <xs:documentation>The valign attribute is used to indicate vertical alignment to the top, middle, bottom, or baseline of the text. Defaults are implementation-dependent.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="valign" type="valign" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupValignImage(XSDAttributeGroup):
    """
    The valign-image attribute is used to indicate vertical alignment for images and graphics, so it removes the baseline value. Defaults are implementation-dependent.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="valign-image">
    <xs:annotation>
        <xs:documentation>The valign-image attribute is used to indicate vertical alignment for images and graphics, so it removes the baseline value. Defaults are implementation-dependent.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="valign" type="valign-image" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupXPosition(XSDAttributeGroup):
    """
    The x-position attribute group is used for elements like notes where specifying x position is common, but specifying y position is rare.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="x-position">
    <xs:annotation>
        <xs:documentation>The x-position attribute group is used for elements like notes where specifying x position is common, but specifying y position is rare.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="default-x" type="tenths" />
    <xs:attribute name="default-y" type="tenths" />
    <xs:attribute name="relative-x" type="tenths" />
    <xs:attribute name="relative-y" type="tenths" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupYPosition(XSDAttributeGroup):
    """
    The y-position attribute group is used for elements like stems where specifying y position is common, but specifying x position is rare.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="y-position">
    <xs:annotation>
        <xs:documentation>The y-position attribute group is used for elements like stems where specifying y position is common, but specifying x position is rare.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="default-x" type="tenths" />
    <xs:attribute name="default-y" type="tenths" />
    <xs:attribute name="relative-x" type="tenths" />
    <xs:attribute name="relative-y" type="tenths" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupImageAttributes(XSDAttributeGroup):
    """
    The image-attributes group is used to include graphical images in a score. The required source attribute is the URL for the image file. The required type attribute is the MIME type for the image file format. Typical choices include application/postscript, image/gif, image/jpeg, image/png, and image/tiff. The optional height and width attributes are used to size and scale an image. The image should be scaled independently in X and Y if both height and width are specified. If only one attribute is specified, the image should be scaled proportionally to fit in the specified dimension.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="image-attributes">
    <xs:annotation>
        <xs:documentation>The image-attributes group is used to include graphical images in a score. The required source attribute is the URL for the image file. The required type attribute is the MIME type for the image file format. Typical choices include application/postscript, image/gif, image/jpeg, image/png, and image/tiff. The optional height and width attributes are used to size and scale an image. The image should be scaled independently in X and Y if both height and width are specified. If only one attribute is specified, the image should be scaled proportionally to fit in the specified dimension.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="source" type="xs:anyURI" use="required" />
    <xs:attribute name="type" type="xs:token" use="required" />
    <xs:attribute name="height" type="tenths" />
    <xs:attribute name="width" type="tenths" />
    <xs:attributeGroup ref="position" />
    <xs:attributeGroup ref="halign" />
    <xs:attributeGroup ref="valign-image" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupPrintAttributes(XSDAttributeGroup):
    """
    The print-attributes group is used by the print element. The new-system and new-page attributes indicate whether to force a system or page break, or to force the current music onto the same system or page as the preceding music. Normally this is the first music data within a measure. If used in multi-part music, they should be placed in the same positions within each part, or the results are undefined. The page-number attribute sets the number of a new page; it is ignored if new-page is not "yes". Version 2.0 adds a blank-page attribute. This is a positive integer value that specifies the number of blank pages to insert before the current measure. It is ignored if new-page is not "yes". These blank pages have no music, but may have text or images specified by the credit element. This is used to allow a combination of pages that are all text, or all text and images, together with pages of music.

The staff-spacing attribute specifies spacing between multiple staves in tenths of staff space. This is deprecated as of Version 1.1; the staff-layout element should be used instead. If both are present, the staff-layout values take priority.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="print-attributes">
    <xs:annotation>
        <xs:documentation>The print-attributes group is used by the print element. The new-system and new-page attributes indicate whether to force a system or page break, or to force the current music onto the same system or page as the preceding music. Normally this is the first music data within a measure. If used in multi-part music, they should be placed in the same positions within each part, or the results are undefined. The page-number attribute sets the number of a new page; it is ignored if new-page is not "yes". Version 2.0 adds a blank-page attribute. This is a positive integer value that specifies the number of blank pages to insert before the current measure. It is ignored if new-page is not "yes". These blank pages have no music, but may have text or images specified by the credit element. This is used to allow a combination of pages that are all text, or all text and images, together with pages of music.

The staff-spacing attribute specifies spacing between multiple staves in tenths of staff space. This is deprecated as of Version 1.1; the staff-layout element should be used instead. If both are present, the staff-layout values take priority.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="staff-spacing" type="tenths" />
    <xs:attribute name="new-system" type="yes-no" />
    <xs:attribute name="new-page" type="yes-no" />
    <xs:attribute name="blank-page" type="xs:positiveInteger" />
    <xs:attribute name="page-number" type="xs:token" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupElementPosition(XSDAttributeGroup):
    """
    The element and position attributes are new as of Version 2.0. They allow for bookmarks and links to be positioned at higher resolution than the level of music-data elements. When no element and position attributes are present, the bookmark or link element refers to the next sibling element in the MusicXML file. The element attribute specifies an element type for a descendant of the next sibling element that is not a link or bookmark. The position attribute specifies the position of this descendant element, where the first position is 1. The position attribute is ignored if the element attribute is not present. For instance, an element value of "beam" and a position value of "2" defines the link or bookmark to refer to the second beam descendant of the next sibling element that is not a link or bookmark. This is equivalent to an XPath test of [.//beam[2]] done in the context of the sibling element.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="element-position">
    <xs:annotation>
        <xs:documentation>The element and position attributes are new as of Version 2.0. They allow for bookmarks and links to be positioned at higher resolution than the level of music-data elements. When no element and position attributes are present, the bookmark or link element refers to the next sibling element in the MusicXML file. The element attribute specifies an element type for a descendant of the next sibling element that is not a link or bookmark. The position attribute specifies the position of this descendant element, where the first position is 1. The position attribute is ignored if the element attribute is not present. For instance, an element value of "beam" and a position value of "2" defines the link or bookmark to refer to the second beam descendant of the next sibling element that is not a link or bookmark. This is equivalent to an XPath test of [.//beam[2]] done in the context of the sibling element.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="element" type="xs:NMTOKEN" />
    <xs:attribute name="position" type="xs:positiveInteger" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupLinkAttributes(XSDAttributeGroup):
    """
    The link-attributes group includes all the simple XLink attributes supported in the MusicXML format. It is also used to connect a MusicXML score with MusicXML parts or a MusicXML opus.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="link-attributes">
    <xs:annotation>
        <xs:documentation>The link-attributes group includes all the simple XLink attributes supported in the MusicXML format. It is also used to connect a MusicXML score with MusicXML parts or a MusicXML opus.</xs:documentation>
    </xs:annotation>
    <xs:attribute ref="xlink:href" use="required" />
    <xs:attribute ref="xlink:type" fixed="simple" />
    <xs:attribute ref="xlink:role" />
    <xs:attribute ref="xlink:title" />
    <xs:attribute ref="xlink:show" default="replace" />
    <xs:attribute ref="xlink:actuate" default="onRequest" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupGroupNameText(XSDAttributeGroup):
    """
    The group-name-text attribute group is used by the group-name and group-abbreviation elements. The print-style and justify attribute groups are deprecated in MusicXML 2.0 in favor of the new group-name-display and group-abbreviation-display elements.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="group-name-text">
    <xs:annotation>
        <xs:documentation>The group-name-text attribute group is used by the group-name and group-abbreviation elements. The print-style and justify attribute groups are deprecated in MusicXML 2.0 in favor of the new group-name-display and group-abbreviation-display elements.</xs:documentation>
    </xs:annotation>
    <xs:attributeGroup ref="print-style" />
    <xs:attributeGroup ref="justify" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupMeasureAttributes(XSDAttributeGroup):
    """
    The measure-attributes group is used by the measure element. Measures have a required number attribute (going from partwise to timewise, measures are grouped via the number).

The implicit attribute is set to "yes" for measures where the measure number should never appear, such as pickup measures and the last half of mid-measure repeats. The value is "no" if not specified.

The non-controlling attribute is intended for use in multimetric music like the Don Giovanni minuet. If set to "yes", the left barline in this measure does not coincide with the left barline of measures in other parts. The value is "no" if not specified.

In partwise files, the number attribute should be the same for measures in different parts that share the same left barline. While the number attribute is often numeric, it does not have to be. Non-numeric values are typically used together with the implicit or non-controlling attributes being set to "yes". For a pickup measure, the number attribute is typically set to "0" and the implicit attribute is typically set to "yes". 

If measure numbers are not unique within a part, this can cause problems for conversions between partwise and timewise formats. The text attribute allows specification of displayed measure numbers that are different than what is used in the number attribute. This attribute is ignored for measures where the implicit attribute is set to "yes". Further details about measure numbering can be specified using the measure-numbering element.

Measure width is specified in tenths. These are the global tenths specified in the scaling element, not local tenths as modified by the staff-size element.	The width covers the entire measure from barline or system start to barline or system end.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="measure-attributes">
    <xs:annotation>
        <xs:documentation>The measure-attributes group is used by the measure element. Measures have a required number attribute (going from partwise to timewise, measures are grouped via the number).

The implicit attribute is set to "yes" for measures where the measure number should never appear, such as pickup measures and the last half of mid-measure repeats. The value is "no" if not specified.

The non-controlling attribute is intended for use in multimetric music like the Don Giovanni minuet. If set to "yes", the left barline in this measure does not coincide with the left barline of measures in other parts. The value is "no" if not specified.

In partwise files, the number attribute should be the same for measures in different parts that share the same left barline. While the number attribute is often numeric, it does not have to be. Non-numeric values are typically used together with the implicit or non-controlling attributes being set to "yes". For a pickup measure, the number attribute is typically set to "0" and the implicit attribute is typically set to "yes". 

If measure numbers are not unique within a part, this can cause problems for conversions between partwise and timewise formats. The text attribute allows specification of displayed measure numbers that are different than what is used in the number attribute. This attribute is ignored for measures where the implicit attribute is set to "yes". Further details about measure numbering can be specified using the measure-numbering element.

Measure width is specified in tenths. These are the global tenths specified in the scaling element, not local tenths as modified by the staff-size element.	The width covers the entire measure from barline or system start to barline or system end.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="number" type="xs:token" use="required" />
    <xs:attribute name="text" type="measure-text" />
    <xs:attribute name="implicit" type="yes-no" />
    <xs:attribute name="non-controlling" type="yes-no" />
    <xs:attribute name="width" type="tenths" />
    <xs:attributeGroup ref="optional-unique-id" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupPartAttributes(XSDAttributeGroup):
    """
    In either partwise or timewise format, the part element has an id attribute that is an IDREF back to a score-part in the part-list.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="part-attributes">
    <xs:annotation>
        <xs:documentation>In either partwise or timewise format, the part element has an id attribute that is an IDREF back to a score-part in the part-list.</xs:documentation>
    </xs:annotation>
    <xs:attribute name="id" type="xs:IDREF" use="required" />
</xs:attributeGroup>
"""
                                     ))


class XSDAttributeGroupPartNameText(XSDAttributeGroup):
    """
    The part-name-text attribute group is used by the part-name and part-abbreviation elements. The print-style and justify attribute groups are deprecated in MusicXML 2.0 in favor of the new part-name-display and part-abbreviation-display elements.
    """
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:attributeGroup xmlns:xs="http://www.w3.org/2001/XMLSchema" name="part-name-text">
    <xs:annotation>
        <xs:documentation>The part-name-text attribute group is used by the part-name and part-abbreviation elements. The print-style and justify attribute groups are deprecated in MusicXML 2.0 in favor of the new part-name-display and part-abbreviation-display elements.</xs:documentation>
    </xs:annotation>
    <xs:attributeGroup ref="print-style" />
    <xs:attributeGroup ref="print-object" />
    <xs:attributeGroup ref="justify" />
</xs:attributeGroup>
"""
                                     ))

__all__=['XSDAttribute', 'XSDAttributeGroup', 'XSDAttributeGroupBendSound', 'XSDAttributeGroupBezier', 'XSDAttributeGroupColor', 'XSDAttributeGroupDashedFormatting', 'XSDAttributeGroupDirective', 'XSDAttributeGroupDocumentAttributes', 'XSDAttributeGroupEnclosure', 'XSDAttributeGroupFont', 'XSDAttributeGroupHalign', 'XSDAttributeGroupJustify', 'XSDAttributeGroupLetterSpacing', 'XSDAttributeGroupLevelDisplay', 'XSDAttributeGroupLineHeight', 'XSDAttributeGroupLineLength', 'XSDAttributeGroupLineShape', 'XSDAttributeGroupLineType', 'XSDAttributeGroupOptionalUniqueId', 'XSDAttributeGroupOrientation', 'XSDAttributeGroupPlacement', 'XSDAttributeGroupPosition', 'XSDAttributeGroupPrintObject', 'XSDAttributeGroupPrintSpacing', 'XSDAttributeGroupPrintStyle', 'XSDAttributeGroupPrintStyleAlign', 'XSDAttributeGroupPrintout', 'XSDAttributeGroupSmufl', 'XSDAttributeGroupSystemRelation', 'XSDAttributeGroupSymbolFormatting', 'XSDAttributeGroupTextDecoration', 'XSDAttributeGroupTextDirection', 'XSDAttributeGroupTextFormatting', 'XSDAttributeGroupTextRotation', 'XSDAttributeGroupTrillSound', 'XSDAttributeGroupValign', 'XSDAttributeGroupValignImage', 'XSDAttributeGroupXPosition', 'XSDAttributeGroupYPosition', 'XSDAttributeGroupImageAttributes', 'XSDAttributeGroupPrintAttributes', 'XSDAttributeGroupElementPosition', 'XSDAttributeGroupLinkAttributes', 'XSDAttributeGroupGroupNameText', 'XSDAttributeGroupMeasureAttributes', 'XSDAttributeGroupPartAttributes', 'XSDAttributeGroupPartNameText']
