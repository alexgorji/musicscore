class MusicTreeException(Exception):
    pass


class NoteException(MusicTreeException):
    pass


class NoteTypeError(NoteException):
    pass


class BeatException(MusicTreeException):
    pass


class BeatWrongDurationError(BeatException, ValueError):
    pass


class BeatIsFullError(BeatException):
    pass


class BeatHasNoParentError(BeatException):
    pass


class VoiceException(MusicTreeException):
    pass


class VoiceHasNoBeatsError(VoiceException):
    pass


class ChordException(MusicTreeException):
    pass


class ChordAlreadySplitError(ChordException):
    pass


class ChordCannotSplitError(ChordException):
    pass
