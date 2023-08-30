from musictree.exceptions import AlreadyFinalized


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
            raise AlreadyFinalized(self)

        for child in self.get_children():
            child.finalize()

        self._finalized = True

    def to_string(self, *args, **kwargs):
        if not self._finalized:
            self.finalize()

        return super().to_string(*args, **kwargs)
