from musicxml.xmlelement.xmlelement import XMLStaff

from musictree.musictree import MusicTree
from musictree.xmlwrapper import XMLWrapper


class Staff(MusicTree, XMLWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._xml_object = XMLStaff(*args, **kwargs)

    def add_child(self, child):
        if child.value is not None and child.value != len(self.get_children()) + 1:
            raise ValueError(f'Voice number must be None or {len(self.get_children()) + 1}')
        if child.value is None:
            child.value = len(self.get_children()) + 1
        else:
            child.value = len(self.get_children()) + 1

        super().add_child(child)
        child.update_beats()
        return child
