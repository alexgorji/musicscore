class TreeChordFlag3(object):
    """
    These flags would be processed after updating type, dots and grouping beams (before creating notes)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __deepcopy__(self, memodict={}):
        return self.__class__()
