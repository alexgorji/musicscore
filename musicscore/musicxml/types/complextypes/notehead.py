from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract, TypeYesNo
from musicscore.musicxml.attributes.color import Color
from musicscore.musicxml.attributes.font import Font
from musicscore.musicxml.types.complextypes.complextype import ComplexType

from musicscore.musicxml.types.simple_type import TypeNoteheadValue


class Filled(AttributeAbstract):

    def __init__(self, filled=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('filled', filled, 'TypeYesNo')


# class Parentheses(AttributeAbstract):
#
#     def __init__(self, parentheses=None, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.generate_attribute('parentheses', parentheses, 'TypeYesNo')


# smulf
# < xs: attributeGroup ref = "smufl" / >
class ComplexTypeNotehead(ComplexType, TypeNoteheadValue, Filled, Font, Color):
    """
    The notehead type indicates shapes other than the open and closed ovals associated with note durations.

    The smufl attribute can be used to specify a particular notehead, allowing application interoperability without
    requiring every SMuFL glyph to have a MusicXML element equivalent. This attribute can be used either with the
    "other" value, or to refine a specific notehead value such as "cluster". Noteheads in the SMuFL "Note name
    noteheads" range (U+E150–U+E1AF) should not use the smufl attribute or the "other" value, but instead use the
    notehead-text elem For the enclosed shapes, the default is to be hollow for half notes and longer, and filled
    otherwise. The filled attribute can be set to change this if nee If the parentheses attribute is set to yes,
    the notehead is parenthesized. It is no by default.
    """

    def __init__(self, tag, value='normal', *args, **kwargs):
        super().__init__(tag=tag, value=value, *args, **kwargs)

    @property
    def parentheses(self):
        return self.get_attribute('parentheses')

    @parentheses.setter
    def parentheses(self, value):
        if value is None:
            self.remove_attribute('parentheses')
        else:
            TypeYesNo(value)
            self._ATTRIBUTES.insert(0, 'parentheses')
            self.set_attribute('parentheses', value)
