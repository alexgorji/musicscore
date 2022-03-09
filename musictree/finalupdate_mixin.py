from musictree.exceptions import AlreadyFinalUpdated


class FinalUpdateMixin:

    def __init__(self):
        self._final_updated = False

    def final_updates(self) -> None:
        """
        final_updates can only be called once.

        It calls final_updates()` method of all  children.
        """
        if self._final_updated:
            raise AlreadyFinalUpdated(self)

        for child in self.get_children():
            child.final_updates()

        self._final_updated = True

    def to_string(self, *args, **kwargs):
        if not self._final_updated:
            self.final_updates()

        return super().to_string(*args, **kwargs)
