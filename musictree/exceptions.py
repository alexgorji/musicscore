class MusicTreeException(Exception):
    pass


class MusicTreeDurationError(MusicTreeException):
    pass


class NoteException(MusicTreeException):
    pass


class NoteTypeError(NoteException):
    pass
