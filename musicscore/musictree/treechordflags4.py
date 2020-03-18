class TreeChordFlag4(object):
    """
    These flags would be processed as last action before finishing the score
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __deepcopy__(self, memodict={}):
        return self.__class__()


class HideAccidental4(TreeChordFlag4):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def implement(self, chord):
        for note in chord.notes:
            note.accidental.show = False
        return [chord]
