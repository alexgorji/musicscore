from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeNoteTypeValue, TypeSymbolSize


class ComplexTypeNoteType(ComplexType, TypeNoteTypeValue):
    """The note-type type indicates the graphic note type. Values range from 1024th to maxima. The size attribute
    indicates full, cue, grace-cue, or large size. The default is full for regular notes, grace-cue for notes that
    contain both grace and cue elements, and cue for notes that contain either a cue or a grace element, but not both.
    """
    _ATTRIBUTES = []

    def __init__(self, tag, size=None, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.size = size

    @property
    def size(self):
        return self.get_attribute('size')

    @size.setter
    def size(self, value):
        if value is None:
            self.remove_attribute('size')
        else:
            TypeSymbolSize(value)
            self._ATTRIBUTES.insert(0, 'size')
            self.set_attribute('size', value)
