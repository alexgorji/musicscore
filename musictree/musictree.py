from tree.tree import Tree


class MusicTree(Tree):
    """
    MusicTree is the parent class of all music tree objects: Score (root), Part (first layer), Measure (second layer),
    Chord (third layer). An abstract grid-like layer of TreeBeats can be imagined as a quantity between Measure and
    Chord depending on measures time signature.
    """
    _ATTRIBUTES = {}

    def _check_child_to_be_added(self, child):
        if 'Score' in self.__mro__ and 'Part' not in child.__mro__:
            raise TypeError('Score accepts only children of type Part')
        if 'Part' in self.__mro__ and 'Measure' not in child.__mro__:
            raise TypeError('Part accepts only children of type Measure')
        if 'Measure' in self.__mro__ and 'Chord' not in child.__mro__:
            raise TypeError('Measure accepts only children of type Chord')

    @property
    def xml_object(self):
        return self._xml_object

    def _convert_attribute_to_child(self, name, value=None):
        setattr(self.xml_object, name, value)

    def to_string(self):
        if self.xml_object:
            return self.xml_object.to_string()
        else:
            raise ValueError(f'{self.__class__.__name__} has no xml object.')

    def __setattr__(self, key, value):
        if '_xml_object' in self.__dict__ and key not in self._ATTRIBUTES and key not in [f'_{attr}' for attr in self._ATTRIBUTES if not
        attr.startswith('_')] and key not in self.__dict__:
            setattr(self._xml_object, key, value)
        else:
            super().__setattr__(key, value)

    def __getattr__(self, item):
        if item == 'xml_object':
            return super().__getattribute__(item)
        try:
            return self._xml_object.__getattr__(item)
        except AttributeError:
            return super().__getattribute__(item)
