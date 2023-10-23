from musicscore.exceptions import AlreadyFinalizedError, ClassHasNoMusicXMLEquivalentError


class FinalizeMixin:
    """
    FinalizeMixin is a mixin for finalizable classes: Score, Part, Measure, Staff, Voice, Beat and Chord
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._finalized = False

    def finalize(self) -> None:
        """
        :obj:`~musicscore.finalize.FinalizeMixin` method

        finalize can only be called once.

        It calls finalize method of all children.
        """
        if self._finalized:
            raise AlreadyFinalizedError(self)

        for child in self.get_children():
            if not child._finalized:
                child.finalize()

        self._finalized = True

    def to_string(self, *args, **kwargs):
        """
        :obj:`~musicscore.finalize.FinalizeMixin` method

        It triggers :obj:`~finalize()` first before calling parent's ``xml_object.to_string()`` method. If no xml_object exists (it means there is no direct MusicXML equavalent of this class) a
        :obj:`~musicscore.exceptions.ClassHasNoMusicXMLEquivalentError` is thrown.
        """

        if not self._finalized:
            self.finalize()

        try:
            return super().to_string(*args, **kwargs)
        except AttributeError:
            raise ClassHasNoMusicXMLEquivalentError(
                f'{self.__class__} has no direct equivalent in MusicXML and cannot be converted to string.')
