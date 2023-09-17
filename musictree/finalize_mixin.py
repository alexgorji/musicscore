from musictree.exceptions import AlreadyFinalizedError, MusicTreeException


class FinalizeMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._finalized = False

    def finalize(self) -> None:
        """
        finalize can only be called once.

        It calls finalize()` method of all children.
        """
        if self._finalized:
            raise AlreadyFinalizedError(self)

        for child in self.get_children():
            if not child._finalized:
                child.finalize()

        self._finalized = True

    def to_string(self, *args, **kwargs):
        if not self._finalized:
            self.finalize()

        try:
            return super().to_string(*args, **kwargs)
        except AttributeError:
            raise MusicTreeException(
                f'{self.__class__} has no direct equivalent in MusicXML and cannot be converted to string.')
