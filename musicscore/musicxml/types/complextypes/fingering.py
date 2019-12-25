from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract
from musicscore.musicxml.attributes.placement import Placement
from musicscore.musicxml.attributes.printstyle import PrintStyle
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import String


class Substitution(AttributeAbstract):
    """"""

    def __init__(self, substitution=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('substitution', substitution, 'TypeYesNo')


class Alternate(AttributeAbstract):
    """"""

    def __init__(self, alternate=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('alternate', alternate, 'TypeYesNo')


class ComplexTypeFingering(ComplexType, String, Substitution, Alternate, PrintStyle, Placement):
    """
    Fingering is typically indicated 1,2,3,4,5. Multiple fingerings may be given, typically to substitute fingerings in
    the middle of a note. The substitution and alternate values are "no" if the attribute is not present. For guitar
    and other fretted instruments, the fingering element represents the fretting finger; the pluck element represents
    the plucking finger.
    """

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
