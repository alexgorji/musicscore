from musicscore.musicxml.types.complextypes.complextype import ComplexType


class ComplexTypeBend(ComplexType):
    """"""

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        raise NotImplementedError()