from musicscore.musicxml.attributes.leveldisplay import LevelDisplay
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.placement import Placement
from musicscore.musicxml.attributes.printstyle import PrintStyle
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeSmulfAccidentalGlyphName, TypeAccidentalValue


class ComplexTypeAccidentalMark(ComplexType, TypeAccidentalValue, LevelDisplay, PrintStyle, Placement,
                                OptionalUniqueId):
    """
    An accidental-mark can be used as a separate notation or as part of an ornament. When used in an ornament, position 
    and placement are relative to the ornament, not relative to the note.
    """

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        # self.smufl = smufl

    # @property
    # def smulf(self):
    #     return self.get_attribute('smulf')
    #
    # @smulf.setter
    # def smulf(self, value):
    #     if value is None:
    #         self.remove_attribute('smulf')
    #     else:
    #         TypeSmulfAccidentalGlyphName(value)
    #         self._ATTRIBUTES.insert(0, 'smulf')
    #         self.set_attribute('smulf', value)
