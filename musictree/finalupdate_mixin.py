from musictree.exceptions import AlreadyFinalUpdated


class FinalUpdateMixin:
    _ATTRIBUTES = {'_final_updated'}

    def __init__(self, *args, **kwargs):
        self._final_updated = False
        super().__init__(*args, **kwargs)

    def final_updates(self) -> None:
        """
        final_updates can only be called once.

        It calls final_updates()` method of all  children.
        """
        if self._final_updated:
            raise AlreadyFinalUpdated(self)

        for b in self.get_children():
            b.final_updates()

        self._final_updated = True

    def to_string(self, *args, **kwargs):
        if not self._final_updated:
            self.final_updates()

        super().to_string(*args, **kwargs)
