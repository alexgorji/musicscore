from musicscore.musictree.treepart import TreePart
from musicscore.musicxml.types.complextypes.partlist import ScorePart


class TreeScorePart(ScorePart):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._max_division = None
        self._forbidden_divisions = None
        self._parts = []
        self.parent_score = None

    @property
    def max_division(self):
        if self._max_division is None:
            self._max_division = self.parent_score.max_division
        return self._max_division

    @max_division.setter
    def max_division(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError('max_division.value must be None or of type int not {}'.format(type(value)))

        self._max_division = value

    @property
    def forbidden_divisions(self):
        if self._forbidden_divisions is None:
            self._forbidden_divisions = self.parent_score.forbidden_divisions

        return self._forbidden_divisions

    @forbidden_divisions.setter
    def forbidden_divisions(self, value):
        if value is not None:
            for x in value:
                if not isinstance(x, int):
                    raise TypeError('forbidden_division must be of type int not{}'.format(type(value)))

        self._forbidden_divisions = value

    def get_parts(self):
        return self._parts

    def add_part(self):
        part = TreePart(id=self.id)
        part.parent_score_part = self
        self._parts.append(part)
        return part
