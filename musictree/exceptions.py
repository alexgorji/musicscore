class MusicTreeException(Exception):
    pass


class NoteException(MusicTreeException):
    pass


class NoteHasNoParentChordError(NoteException):
    pass


class NoteTypeError(NoteException):
    pass


class ChordException(MusicTreeException):
    pass


class ChordAlreadySplitError(ChordException):
    pass


class ChordCannotSplitError(ChordException):
    pass


class ChordHasNoParentError(ChordException):
    pass


class ChordHasNoQuarterDurationError(ChordException):
    pass


class ChordNotesAreAlreadyCreatedError(ChordException):
    pass


class ChordQuarterDurationAlreadySetError(ChordException):
    pass


class ChordHasNoMidisError(ChordException):
    pass


class BeatException(MusicTreeException):
    pass


class BeatWrongDurationError(BeatException, ValueError):
    pass


class BeatIsFullError(BeatException):
    pass


class BeatHasNoParentError(BeatException):
    pass


class BeatHasWrongTupletError(BeatException):
    pass


class VoiceException(MusicTreeException):
    pass


class VoiceHasNoBeatsError(VoiceException):
    pass


class VoiceHasNoParentError(VoiceException):
    pass


class VoiceIsAlreadyFullError(VoiceException):
    pass


class StaffException(MusicTreeException):
    pass


class StaffHasNoParentError(StaffException):
    pass


class MeasureException(MusicTreeException):
    pass


class IdException(MusicTreeException):
    pass


class IdHasAlreadyParentOfSameTypeError(IdException):
    pass


class IdWithSameValueExistsError(IdException):
    pass

class QuantizationException(Exception):
    pass
class QuantizationBeatNotFullError(QuantizationException):
    pass