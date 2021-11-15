from common.helpers import _check_type
from musictree.treemeasure import TreeMeasure


class TreePart(object):
    """
    This class represents a partwise part as the first layer of musical score's tree structure.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._measures = []

    @property
    def measures(self):
        """
        Property returns all TreeMeasures added to part. To add a measure use methode add_measure
        :return: *TreeMeasure
        """
        return self._measures

    def add_measure(self, measure=None):
        """
        Add a TreeMeasure object to part

        :param measure: None or TreeMeasure
        :return: TreeMeasure
        """
        _check_type('measure', measure, TreeMeasure)
        if measure is None:
            measure = TreeMeasure()
        self.measures.append(measure)
        return measure
