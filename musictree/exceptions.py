class MusicTreeException(Exception):
    pass


class NoteException(MusicTreeException):
    pass


class NotationException(NoteException):
    pass


class NoteHasNoParentChordError(NoteException):
    pass


class NoteTypeError(NoteException):
    pass


class ChordException(MusicTreeException):
    pass


class ChordAddXException(ChordException):
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


class VoiceIsFullError(VoiceException):
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


class AlreadyFinalized(MusicTreeException):
    def __init__(self, object_, method_=None):
        msg = f"{object_.__class__.__name__} is already finalized."
        if method_:
            msg += f' Method {object_.__class__.__name__}.{method_}() cannot be called after finalization.'
        super().__init__(msg)


class DeepCopyException(MusicTreeException):
    pass


class MidiHasNoParentChordError(NoteException):
    pass


class AddChordException(MusicTreeException):
    def __init__(self):
        msg = f"Use Part.add_chord() instead!"
        super().__init__(msg)


class SimpleFormatException(MusicTreeException):
    pass
