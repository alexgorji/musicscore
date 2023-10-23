class XMLWrapper:
    """
    XMLWrapper contains an xml object at its core. It is the place where all the intuitive stuff is translated to attributes and children of
    xml objects.

    All attributes and properties which are not listed in _ATTRIBUTES will be set to or get from core xml object.
    """
    _ATTRIBUTES = {}

    XMLClass = None

    @property
    def xml_object(self) -> 'XMLElement':
        """
        :obj:`~musicscore.xmlwrapper.XMLWrapper` method

        This musicscore class has an equivalent ``MusicXML`` class which can be reached via this property.

        If an attribute is not found directly in the main class, it wll be passed on to ``__get_attribute__`` or ``__set__attribute__`` methods of ``self.xml_object``.
        It can also use the short cut attributes of :obj:`~musicxml.xmlelement.xmlelement.XMLElement` to get or set the first child.

        :return: wrapped MusicXML element of type :obj:`~XMLClass`
        """
        return self._xml_object

    def to_string(self, *args, **kwargs) -> str:
        """
        :obj:`~musicscore.xmlwrapper.XMLWrapper` method

        Calls :obj:`~musicxml.xmlelement.xmlelement.XMLElement.to_string` method of self.xml_object

        :return: musicxml snippet
        """
        if self.xml_object:
            return self.xml_object.to_string(*args, **kwargs)
        else:
            raise ValueError(f'{self.__class__.__name__} has no xml object.')

    def __setattr__(self, key, value):
        attributes = self._ATTRIBUTES
        try:
            if self._TREE_ATTRIBUTES:
                attributes.union(self._TREE_ATTRIBUTES)
        except AttributeError:
            pass
        if key[0] != '_' and ('_xml_object' in self.__dict__ and key not in attributes and key not in self.__dict__):
            setattr(self._xml_object, key, value)
        else:
            super().__setattr__(key, value)

    def __getattr__(self, item):
        if item == '_TREE_ATTRIBUTES':
            raise AttributeError
        if item == 'xml_object':
            return super().__getattribute__(item)
        try:
            return self._xml_object.__getattribute__(item)
        except AttributeError:
            try:
                return self._xml_object.__getattr__(item)
            except AttributeError:
                return super().__getattribute__(item)
