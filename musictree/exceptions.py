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


class BeatNotFullError(BeatException):
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


class PartException(MusicTreeException):
    pass


class ScoreException(MusicTreeException):
    pass


class IdException(MusicTreeException):
    pass


class IdHasAlreadyParentOfSameTypeError(IdException):
    pass


class IdWithSameValueExistsError(IdException):
    pass



class AlreadyFinalUpdated(MusicTreeException):
    def __init__(self, object_):
        msg = f"final_updates method of {object_.__class__.__name__} can only be called once."
        super().__init__(msg)
