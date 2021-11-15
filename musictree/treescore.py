from common.helpers import _check_type
from musictree.treepart import TreePart


class TreeScore(object):
    """
    This class represents a partwise score as the root of musical score's tree structure.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parts = []

    @property
    def parts(self):
        """
        Property returns all TreeParts added to score. To add a part use methode add_part
        :return: *TreePart
        """
        return self._parts

    def add_part(self, part=None):
        """
        Add a TreePart object to the score

        :param part: None or TreePart
        :return: TreePart
        """
        _check_type('measure', part, TreePart)
        if part is None:
            part = TreePart()
        self.parts.append(part)
        return part

    def export_xml(self, xml_path, version='3.1'):
        pass
