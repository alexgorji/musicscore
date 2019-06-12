from musicscore.dtd.dtd import GroupReference, Sequence
from musicscore.musicxml.groups.margins import AllMargins
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeMarginType


class ComplexTypePageMargins(ComplexType):
    """Page margins are specified either for both even and odd pages, or via separate odd and even page number values.
    The type attribute is not needed when used as part of a print element. If omitted when the page-margins type is
    used in the defaults element, "both" is the default value."""

    _DTD = Sequence(
        GroupReference(AllMargins)
    )

    def __init__(self, tag, type_=None, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.type = type_

    @property
    def type(self):
        return self.get_attribute('type')

    @type.setter
    def type(self, value):
        if value is None:
            self.remove_attribute('type')
        else:
            TypeMarginType(value)
            self._ATTRIBUTES = ['type']
            self.set_attribute('type', value)
