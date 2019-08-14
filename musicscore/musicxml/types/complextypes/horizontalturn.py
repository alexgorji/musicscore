from musicscore.musicxml.attributes.placement import Placement
from musicscore.musicxml.attributes.printstyle import PrintStyle
from musicscore.musicxml.attributes.trillsound import TrillSound
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeYesNo


class ComplexTypeHorizontalTurn(ComplexType, PrintStyle, Placement, TrillSound):
    """
    The horizontal-turn type represents turn elements that are horizontal rather than vertical. These are empty elements
    with print-style, placement, trill-sound, and slash attributes. If the slash attribute is yes, then a vertical line
    is used to slash the turn; it is no by default.
    """

    def __init__(self, tag, slash='no', *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.slash = slash

    @property
    def slash(self):
        return self.get_attribute('slash')

    @slash.setter
    def slash(self, value):
        if value is None:
            self.remove_attribute('slash')
        else:
            TypeYesNo(value)
            self._ATTRIBUTES.insert(0, 'slash')
            self.set_attribute('slash', value)
