"""
    <xs:attributeGroup name="printout">
        <xs:annotation>
            <xs:documentation>
            </xs:documentation>
        </xs:annotation>
        <xs:attributeGroup ref="print-object"/>
        <xs:attribute name="print-dot" type="yes-no"/>
        <xs:attributeGroup ref="print-spacing"/>
        <xs:attribute name="print-lyric" type="yes-no"/>
    </xs:attributeGroup>
"""

from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract
from musicscore.musicxml.attributes.printobject import PrintObject
from musicscore.musicxml.attributes.printspacing import PrintSpacing


class PrintDot(AttributeAbstract):
    """"""

    def __init__(self, print_dot=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('print-dot', print_dot, 'TypeYesNo')


class PrintLyric(AttributeAbstract):
    """"""

    def __init__(self, print_lyric=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('print-lyric', print_lyric, 'TypeYesNo')


class Printout(PrintObject, PrintDot, PrintSpacing, PrintLyric):
    """The printout attribute group collects the different controls over printing an object (e.g. a note or rest) and
    its parts, including augmentation dots and lyrics. This is especially useful for notes that overlap in different
    voices, or for chord sheets that contain lyrics and chords but no melody.

    By default, all these attributes are set to yes. If print-object is set to no, the print-dot and print-lyric
    attributes are interpreted to also be set to no if they are not present."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
